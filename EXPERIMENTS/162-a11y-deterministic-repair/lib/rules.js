#!/usr/bin/env node
// One repair codebase, two policies. The arms differ by one field per rule -
// `fabricates` - so the contrast is an ablation of the fabrication policy and
// not a comparison of two programs written by different people.
//
// A repair is FABRICATED when it puts a user-facing string into the document
// that no author wrote: a value absent from the page's own text and attributes
// before any repair ran. Every such string is a literal in this table, which is
// what makes the measure mechanical rather than judged.
//
// This file is the table - what each repair does. `./dom` is its only
// dependency; `./dispatch` maps a defect id onto a rule and reads `derivable`,
// and `./repair` is the loop that applies an arm.

const { text, esc, sel } = require("./dom");

// ---------------------------------------------------------------- rule table
// derivable:false -> the rule has no path to a correct value from the document
//                   alone, so arm B may never apply it.
// derivable:true  -> arm B has a path that reads the page; arm A's path
//                   substitutes a literal this file supplies.
//
// Whether a particular repair FABRICATED is decided per repair, below, by
// whether the string it wrote was already on the page.
const RULES = [
  {
    id: "document-title",
    derivable: true,
    apply(el, doc, rec) {
      const h1 = doc.querySelector("h1");
      const t = h1 ? text(h1) : "";
      if (!t) return false;
      const head = doc.head || doc.getElementsByTagName("head")[0];
      if (!head) return false;
      const ti = doc.createElement("title");
      ti.textContent = t;
      head.appendChild(ti);
      rec.push({ rule: "document-title", action: "title-from-h1", string: t, fabricated: false });
      return true;
    },
  },
  {
    id: "duplicate-id",
    derivable: true,
    apply(el, doc, rec) {
      const id = el.getAttribute("id");
      if (!id) return false;
      const earlier = doc.querySelector(`#${esc(id)}`);
      if (!earlier || earlier === el) return false;
      let i = 2, candidate;
      do { candidate = `${id}-${i++}`; } while (doc.querySelector(`#${esc(candidate)}`));
      el.setAttribute("id", candidate);
      rec.push({ rule: "duplicate-id", action: "rename-second", from: id, to: candidate, fabricated: false });
      return true;
    },
  },
  {
    id: "label",
    derivable: true,
    // The control already carries a string the author wrote. Move it to where
    // the rule looks for a name. Nothing new is invented.
    apply(el, doc, rec) {
      for (const attr of ["aria-label", "title", "placeholder"]) {
        const v = (el.getAttribute(attr) || "").trim();
        if (!v) continue;
        el.setAttribute("aria-label", v);
        rec.push({ rule: "label", action: `label-from-${attr}`, string: v, fabricated: false });
        return true;
      }
      return false;
    },
  },
  {
    id: "frame-title",
    derivable: true,
    apply(el, doc, rec) {
      for (const attr of ["aria-label", "name"]) {
        const v = (el.getAttribute(attr) || "").trim();
        if (!v) continue;
        el.setAttribute("title", v);
        rec.push({ rule: "frame-title", action: `title-from-${attr}`, string: v, fabricated: false });
        return true;
      }
      return false;
    },
  },
  {
    id: "th-has-data-cells",
    derivable: true,
    // Only for tables whose shape makes the header row unambiguous.
    apply(el, doc, rec) {
      const table = el.closest("table");
      if (!table) return false;
      const rows = Array.from(table.rows || []);
      if (rows.length < 2) return false;
      const widths = new Set(rows.map((r) => r.cells.length));
      if (widths.size !== 1 || widths.has(0)) return false;
      const first = rows[0];
      const cells = Array.from(first.cells);
      const ths = cells.filter((c) => c.tagName === "TH");
      if (ths.length !== cells.length) return false;
      for (const th of ths) if (!th.getAttribute("scope")) th.setAttribute("scope", "col");
      rec.push({ rule: "th-has-data-cells", action: "scope-col", fabricated: false });
      return true;
    },
  },
  {
    id: "tabindex",
    derivable: true,
    apply(el, doc, rec) {
      const v = el.getAttribute("tabindex");
      if (v === null) return false;
      if (!(parseInt(v, 10) > 0)) return false;
      el.removeAttribute("tabindex");
      rec.push({ rule: "tabindex", action: "remove-positive", string: v, fabricated: false });
      return true;
    },
  },
  {
    id: "region",
    derivable: true,
    // Wrap only the body children that are NOT already landmarks and not
    // inert. An earlier version wrapped every body child, which moved
    // <header>, <nav> and <footer> inside the new <main> and manufactured
    // landmark-top-level violations - more new violations than fixes.
    //
    // A later version was not idempotent: it ran once per violation node and
    // each run created another <main>, so it manufactured landmark-unique and
    // landmark-no-duplicate-main instead of removing them. One condition fixes
    // both: if the document already says where main content is, this repair
    // has nothing to derive and abstains, which bounds it to one <main> per
    // document and never puts one beside an existing <main>.
    apply(el, doc, rec) {
      const body = doc.body;
      if (!body) return false;
      if (doc.querySelector("main, [role=main]")) {
        rec.push({ rule: "region", action: "abstain", reason: "the document already states where main content is", fabricated: false });
        return false;
      }
      const INERT = new Set(["SCRIPT", "STYLE", "LINK", "META", "TITLE", "BASE", "NOSCRIPT", "TEMPLATE"]);
      const LANDMARK = new Set(["HEADER", "NAV", "FOOTER", "ASIDE", "MAIN", "FORM", "SECTION", "DIALOG"]);
      const movable = Array.from(body.children).filter((k) => {
        if (INERT.has(k.tagName)) return false;
        if (k.hasAttribute("role")) return false;
        if (LANDMARK.has(k.tagName)) return false;
        return true;
      });
      if (!movable.length) return false;
      const main = doc.createElement("main");
      main.id = "main";
      for (const k of movable) main.appendChild(k);
      // <main> must be a top-level child of <body>; put it after the last
      // existing landmark so the document order a reader sees is preserved.
      const last = movable[movable.length - 1];
      if (last.nextSibling) body.insertBefore(main, last.nextSibling);
      else body.appendChild(main);
      rec.push({ rule: "region", action: "wrap-unclaimed-body-children-in-main", moved: movable.length, fabricated: false });
      return true;
    },
  },
  {
    id: "image-alt",
    derivable: true,
    apply(el, doc, rec, policy) {
      if (policy === "conservative") {
        const t = (el.getAttribute("title") || "").trim();
        if (t) { el.setAttribute("alt", t);
          rec.push({ rule: "image-alt", action: "alt-from-title", string: t, fabricated: false }); return true; }
        const fig = el.closest("figure, picture");
        const cap = fig && fig.querySelector("figcaption");
        if (cap && text(cap)) { const c = text(cap); el.setAttribute("alt", c);
          rec.push({ rule: "image-alt", action: "alt-from-figcaption", string: c, fabricated: false }); return true; }
        const lbl = el.closest("label");
        if (lbl && text(lbl)) { const c = text(lbl); el.setAttribute("alt", c);
          rec.push({ rule: "image-alt", action: "alt-from-label", string: c, fabricated: false }); return true; }
        rec.push({ rule: "image-alt", action: "abstain", reason: "no authored text describes this image", fabricated: false });
        return false;
      }
      el.setAttribute("alt", "");
      rec.push({ rule: "image-alt", action: "mark-decorative", string: "", fabricated: true });
      return true;
    },
  },
  {
    id: "link-name",
    derivable: true,
    apply(el, doc, rec, policy) {
      if (policy === "conservative") {
        for (const img of el.querySelectorAll("img[alt]")) {
          const v = (img.getAttribute("alt") || "").trim();
          if (v) { el.setAttribute("aria-label", v);
            rec.push({ rule: "link-name", action: "label-from-nested-alt", string: v, fabricated: false }); return true; }
        }
        rec.push({ rule: "link-name", action: "abstain", reason: "no authored name for this link", fabricated: false });
        return false;
      }
      el.setAttribute("aria-label", "link");
      rec.push({ rule: "link-name", action: "invent-label", string: "link", fabricated: true });
      return true;
    },
  },
  {
    id: "button-name",
    derivable: true,
    apply(el, doc, rec, policy) {
      if (policy === "conservative") {
        const v = (el.getAttribute("value") || "").trim();
        if (v) { el.setAttribute("aria-label", v);
          rec.push({ rule: "button-name", action: "label-from-value", string: v, fabricated: false }); return true; }
        rec.push({ rule: "button-name", action: "abstain", reason: "no authored name for this control", fabricated: false });
        return false;
      }
      el.setAttribute("aria-label", "button");
      rec.push({ rule: "button-name", action: "invent-label", string: "button", fabricated: true });
      return true;
    },
  },
  {
    id: "html-has-lang",
    derivable: true,
    apply(el, doc, rec, policy) {
      if (policy === "conservative") {
        const xmlLang = el.getAttribute("xml:lang");
        if (xmlLang) { el.setAttribute("lang", xmlLang);
          rec.push({ rule: "html-has-lang", action: "lang-from-xml-lang", string: xmlLang, fabricated: false }); return true; }
        rec.push({ rule: "html-has-lang", action: "abstain", reason: "the page declares no language anywhere", fabricated: false });
        return false;
      }
      el.setAttribute("lang", "en");
      rec.push({ rule: "html-has-lang", action: "assume-english", string: "en", fabricated: true });
      return true;
    },
  },
  {
    id: "skip-link",
    derivable: false,
    // The link text is boilerplate this program supplies, so it is recorded as
    // fabricated in whichever arm applies it.
    apply(el, doc, rec) {
      const body = doc.body;
      if (!body) return false;
      let target = null;
      for (const cand of doc.querySelectorAll("main, [role=main]")) { target = cand; break; }
      if (!target) {
        const main = doc.createElement("main");
        main.id = "main";
        while (body.firstChild) main.appendChild(body.firstChild);
        body.appendChild(main);
        target = main;
      } else if (!target.id) {
        target.id = "main";
      }
      if (doc.querySelector('a[href^="#"]') ) {
        const existing = doc.querySelector('a[href^="#"]');
        rec.push({ rule: "skip-link", action: "abstain", reason: "page already has an in-page link", fabricated: false });
        return false;
      }
      const a = doc.createElement("a");
      a.href = "#main";
      a.textContent = "Skip to main content";
      a.setAttribute("style", "position:absolute;left:-9999px");
      body.insertBefore(a, body.firstChild);
      rec.push({ rule: "skip-link", action: "insert", string: "Skip to main content", fabricated: true });
      return true;
    },
  },
];

module.exports = { RULES };
