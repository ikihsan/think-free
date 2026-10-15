#!/usr/bin/env node
// Run 1's driver: the canonical loop bound to run 1's rule table. One line,
// because the driver is identical - only the table differed.

const { makeRepair } = require("./repair");
const T = require("./dispatch-run1");

module.exports = { repair: makeRepair(T), ruleFor: T.ruleFor, permitted: T.permitted };
