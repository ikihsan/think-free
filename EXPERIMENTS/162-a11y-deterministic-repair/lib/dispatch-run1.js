#!/usr/bin/env node
// Run 1's defect-id lookup. Split from `./rules-run1` at the 300-line cap,
// exactly as `./dispatch` was split from `./rules`.

const { RULES } = require("./rules-run1");

const BY_ID = {};
for (const r of RULES) BY_ID[r.id] = r;

// axe reports the same defect under more than one id depending on which
// impact path fired. Both map to one repair, so the arm comparison is on
// defects rather than on axe's internal naming.
//
// Two groups are deliberately NOT aliased, because the repair they were
// first given was wrong in a way the oracle caught:
//   * `landmark-unique`, `landmark-no-duplicate-*`, `landmark-*-is-top-level`
//     were mapped to `region` (wrap in another <main>), which manufactures
//     the duplicate-landmark defect it was meant to remove.
//   * `aria-required-attr` fires on a missing *state* attribute
//     (`role="checkbox"` with no `aria-checked`), a different defect from a
//     missing name.
// They stay outside the table and are counted as skipped, not repaired.
const ALIAS = {
  "duplicate-id-active": "duplicate-id",
  "duplicate-id-aria": "duplicate-id",
  "input-image-alt": "image-alt",
  "role-img-alt": "image-alt",
  "select-name": "link-name",
  "aria-input-field-name": "link-name",
  "aria-toggle-field-name": "button-name",
  "aria-dialog-name": "link-name",
  "aria-progressbar-name": "link-name",
  "landmark-one-main": "region",
  "bypass": "skip-link",
  "td-headers-attr": "th-has-data-cells",
};

function ruleFor(id) {
  return BY_ID[id] || (ALIAS[id] ? BY_ID[ALIAS[id]] : null);
}

// Which rules each policy may apply. This single function, plus the branch
// inside each rule, is the whole difference between arm A and arm B:
// arm A takes the literal path, arm B takes the path that reads the page.
function permitted(policy, rule) {
  return policy === "blanket" ? true : rule.derivable === true;
}

module.exports = { ruleFor, permitted };
