#!/usr/bin/env node
// DOM readers shared by both rule tables. Split out of lib/repair.js at
// the 300-line cap: these are the only three functions that read a node.

function text(el) {
  return (el.textContent || "").replace(/\s+/g, " ").trim();
}

function esc(s) {
  return String(s).replace(/([^\w-])/g, "\\$1");
}

function sel(doc, target) {
  const s = Array.isArray(target) ? target.join(" ") : String(target || "");
  if (!s) return null;
  try { return doc.querySelector(s); } catch (e) { return null; }
}

module.exports = { text, esc, sel };
