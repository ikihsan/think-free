#!/usr/bin/env node
// Tests for the repair module. The expectations are the behaviours the
// protocol declares, not the current output: the conservative arm must never
// put a string on the page that the page did not contain, and must abstain
// where nothing can be derived.
const assert = require("assert");
const { JSDOM } = require("jsdom");
const R = require("../lib/repair");

function dom(html) {
  return new JSDOM(html, { url: "https://example.org/" }).window.document;
}

// The harness's violation shape: one flat entry per axe node, each carrying
// the rule id and its target. repair() regroups by rule internally.
const v = (id, ...targets) => targets.map((t) => ({ id, target: [t] }));

const tests = [];
const test = (name, fn) => tests.push([name, fn]);

test("conservative arm abstains on image-alt when nothing describes the image", () => {
  const d = dom(`<body><img src="a.png"></body>`);
  const out = R.repair(d, v("image-alt", "img"), "conservative");
  assert.strictEqual(out.applied_count, 0);
  assert.strictEqual(d.querySelector("img").getAttribute("alt"), null);
  assert.ok(out.log.some((r) => r.action === "abstain"));
});

test("conservative arm derives image-alt from a figcaption", () => {
  const d = dom(`<body><figure><img src="a.png"><figcaption>A dog asleep</figcaption></figure></body>`);
  const out = R.repair(d, v("image-alt", "img"), "conservative");
  assert.strictEqual(d.querySelector("img").getAttribute("alt"), "A dog asleep");
  assert.strictEqual(out.fabricated_count, 0);
});

test("blanket arm marks an undescribed image decorative, and says so", () => {
  const d = dom(`<body><img src="a.png"></body>`);
  const out = R.repair(d, v("image-alt", "img"), "blanket");
  assert.strictEqual(d.querySelector("img").getAttribute("alt"), "");
  assert.strictEqual(out.fabricated_count, 1);
  assert.strictEqual(out.applied_count, 1);
});

test("blanket arm invents a link name; conservative arm abstains", () => {
  const b = R.repair(dom(`<body><a href="/x"><svg></svg></a></body>`), v("link-name", "a"), "blanket");
  assert.strictEqual(b.fabricated_count, 1);
  assert.strictEqual(b.applied[0].string, "link");
  const c = R.repair(dom(`<body><a href="/x"><svg></svg></a></body>`), v("link-name", "a"), "conservative");
  assert.strictEqual(c.applied_count, 0);
  assert.ok(c.log.some((r) => r.action === "abstain"));
});

test("conservative arm derives a link name from a nested image alt", () => {
  const d = dom(`<body><a href="/x"><img src="a.png" alt="Our annual report"></a></body>`);
  const out = R.repair(d, v("link-name", "a"), "conservative");
  assert.strictEqual(d.querySelector("a").getAttribute("aria-label"), "Our annual report");
  assert.strictEqual(out.fabricated_count, 0);
});

test("skip-link is never derivable, so arm B may not apply it", () => {
  assert.strictEqual(R.permitted("conservative", R.ruleFor("skip-link")), false);
  assert.strictEqual(R.permitted("blanket", R.ruleFor("skip-link")), true);
});

test("label repair moves an authored attribute and never invents one", () => {
  const d = dom(`<body><input type="text" placeholder="Your email"></body>`);
  const out = R.repair(d, v("label", "input"), "conservative");
  assert.strictEqual(d.querySelector("input").getAttribute("aria-label"), "Your email");
  assert.strictEqual(out.fabricated_count, 0);
});

test("label repair abstains when the control carries no string", () => {
  const d = dom(`<body><input type="text"></body>`);
  const out = R.repair(d, v("label", "input"), "conservative");
  assert.strictEqual(out.applied_count, 0);
});

test("duplicate-id renames the second occurrence and keeps the first", () => {
  const d = dom(`<body><div id="dup">a</div><div id="dup">b</div></body>`);
  const out = R.repair(d, v("duplicate-id", "body > div:nth-child(2)"), "conservative");
  const ids = Array.from(d.querySelectorAll("div")).map((e) => e.getAttribute("id"));
  assert.deepStrictEqual(ids, ["dup", "dup-2"]);
  assert.strictEqual(out.fabricated_count, 0);
});

test("html-has-lang is a fabrication in the blanket arm and an abstention otherwise", () => {
  const mk = () => dom(`<html><body><p>hello</p></body></html>`);
  const b = R.repair(mk(), v("html-has-lang", "html"), "blanket");
  assert.strictEqual(b.fabricated_count, 1);
  const c = R.repair(mk(), v("html-has-lang", "html"), "conservative");
  assert.strictEqual(c.applied_count, 0);
});

test("region wraps body children in main and invents no string", () => {
  const d = dom(`<body><p>one</p><p>two</p></body>`);
  const out = R.repair(d, v("region", "p"), "conservative");
  assert.ok(d.querySelector("main"));
  assert.strictEqual(d.querySelector("main").children.length, 2);
  assert.strictEqual(out.fabricated_count, 0);
});

test("one (rule, target) pair is repaired at most once", () => {
  const d = dom(`<body><img src="a.png"><img src="a.png"></body>`);
  const out = R.repair(d, v("image-alt", "img", "img"), "blanket");
  assert.strictEqual(out.applied_count, 1);
});

test("a rule outside the table is reported, never silently dropped", () => {
  const d = dom(`<body><div id="x"></div></body>`);
  const out = R.repair(d, v("color-contrast", "#x"), "conservative");
  assert.strictEqual(out.applied_count, 0);
  assert.strictEqual(out.by_rule["color-contrast"].not_in_table, 1);
});

test("skip-link records its boilerplate as fabricated in whichever arm", () => {
  const d = dom(`<body><p>content</p></body>`);
  const out = R.repair(d, v("skip-link", "body"), "conservative");
  // conservative may not use a fabricating rule at all
  assert.strictEqual(out.applied_count, 0);
  const b = R.repair(dom(`<body><p>content</p></body>`), v("skip-link", "body"), "blanket");
  assert.strictEqual(b.applied_count, 1);
  assert.strictEqual(b.fabricated_count, 1);
});

let failed = 0;
for (const [name, fn] of tests) {
  try { fn(); process.stdout.write(`ok   ${name}\n`); }
  catch (e) { failed += 1; process.stdout.write(`FAIL ${name}\n     ${e.message}\n`); }
}
process.stdout.write(`\n${tests.length - failed}/${tests.length} passed\n`);
process.exit(failed ? 1 : 0);