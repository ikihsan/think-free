#!/usr/bin/env python3
"""
Actual Budget's `findSchedules()`, ported to Python 3.8, standard library only.

Source of truth (read 2026-10-09):
  actualbudget/actual @ master
  packages/loot-core/src/server/schedules/find-schedules.ts   (391 lines)
  packages/loot-core/src/shared/rules.ts  (getApproxNumberThreshold)

Why this file exists: E065 compared itself against "merchant appears >= 3
times". That is a strawman. Actual Budget ships an automatic recurring-payment
detector in a personal-finance application, so it is the strongest
alternative a user could actually install. This port is what E072 measures
against.

Fidelity notes, all deliberate and all checkable against the TypeScript:

  * `getApproxNumberThreshold` -> `round(abs(amount) * 0.075)`, verbatim.
  * The occurrence window is `d.subDays(date, 2) .. d.addDays(date, 2)`,
    verbatim.
  * `matchSchedules` uses `Array.find`: the FIRST transaction in the window
    whose amount is within the threshold is taken, and if that one's payee
    differs the match is dropped. It does NOT keep searching for a
    same-payee transaction. Ported exactly, because that quirk makes Actual
    *stricter* on noisy data and loosening it would flatter us.
  * All six patterns are ported: weekly, every-2-weeks, monthly (day <= 28),
    monthly-last-day, monthly 1st-or-3rd-of-weekday, monthly
    2nd-or-4th-of-weekday.
  * `monthly1stor3rd` and `monthly2ndor4th` derive the weekday from
    `new Date()` at scan time in the original. We pin "today" to
    `TODAY` (the corpus max date) so the port is deterministic, and record
    it in results.json. This is a change from the original and is the only
    one.
  * `findStartDate` walks a found schedule's start date backwards while
    transactions keep matching. It cannot change HOW MANY schedules are found
    -- dedup by payee happens before it -- so it is not ported. Recorded as
    a read-and-omitted decision, not an oversight.
  * `schedule: null` and `payee.transfer_acct: null` are Actual-internal
    bookkeeping for a populated database. Here every row is an unscheduled,
    non-transfer transaction, so those filters are vacuously satisfied.
"""

import calendar
from collections import defaultdict
from datetime import date, timedelta

MATCH_WINDOW_DAYS = 2
THRESHOLD_FRACTION = 0.075


def approx_number_threshold(amount):
    """packages/loot-core/src/shared/rules.ts:234 -- JS Math.round semantics."""
    import math
    x = abs(amount) * THRESHOLD_FRACTION
    return math.floor(x + 0.5)


def _day_repr(d):
    return d.isoformat()


def _parse_day(s):
    return date(int(s[0:4]), int(s[5:7]), int(s[8:10]))


def _add_months(d, n):
    """date-fns addMonths: clamp the day to the target month's length."""
    y = d.year + (d.month - 1 + n) // 12
    m = (d.month - 1 + n) % 12 + 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def _last_day_of(d):
    return date(d.year, d.month, calendar.monthrange(d.year, d.month)[1])


def _weekday(d):
    return d.isoweekday()  # 1=Mon .. 7=Sun, matches rrule's MO..SU order


def _nth_weekday_in_month(d, weekday, n):
    """`{type: weekday, value: n}` -> the n-th `weekday` of d's month."""
    first = date(d.year, d.month, 1)
    offset = (weekday - first.isoweekday()) % 7
    return first + timedelta(days=offset + 7 * (n - 1))


# --------------------------------------------------------------------------
# rrule.js `occurrences({take: 3})` for the six config shapes we need.
# --------------------------------------------------------------------------

def take_dates(config):
    """Return the first three occurrence dates of `config`, inclusive of start."""
    start = _parse_day(config["start"]) if isinstance(config["start"], str) else config["start"]
    freq = config.get("frequency")
    interval = config.get("interval", 1)
    patterns = config.get("patterns")

    if freq == "weekly":
        step = timedelta(weeks=interval)
        return [start + step * k for k in range(3)]

    if freq == "monthly":
        if patterns and patterns[0].get("type") == "day" and patterns[0].get("value") == -1:
            return [_last_day_of(_add_months(start, k)) for k in range(3)]
        if patterns and patterns[0].get("type") in ("MO", "TU", "WE", "TH", "FR", "SA", "SU"):
            wd = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"].index(patterns[0]["type"]) + 1
            ns = sorted({p["value"] for p in patterns})
            out = []
            probe = _add_months(start, -1)
            while len(out) < 3:
                for n in ns:
                    cand = _nth_weekday_in_month(probe, wd, n)
                    if cand >= start:
                        out.append(cand)
                        if len(out) == 3:
                            break
                probe = _add_months(probe, 1)
            return out[:3]
        # plain monthly: rrule.js keeps DTSTART's day of month
        return [_clamp_day(start, _add_months(start, k)) for k in range(3)]

    raise ValueError("unsupported frequency: %r" % (freq,))


def _clamp_day(anchor, target):
    return date(target.year, target.month, min(anchor.day, calendar.monthrange(target.year, target.month)[1]))


def _add_occurrence(pattern_date, kind, k):
    """Occurrence k (1-based) after `pattern_date` for a monthly pattern."""
    wd = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"].index(kind) + 1
    probe = pattern_date
    n = 0
    while n < k:
        probe = _add_months(probe, 1)
        n += 1
    # rrule.js keeps the BYDAY set fixed per month; take the first month that
    # has all of them, which the `_nth_weekday_in_month` search above mirrors.
    return _nth_weekday_in_month(probe, wd, 1)


# --------------------------------------------------------------------------

def _rank(day1, day2):
    # Accepts either a day string or a date; the TypeScript compares Date
    # objects while our occurrence list carries both forms in different arms.
    if not isinstance(day1, date):
        day1 = _parse_day(day1)
    if not isinstance(day2, date):
        day2 = _parse_day(day2)
    day_diff = abs((day1 - day2).days)
    return 1.0 / (day_diff + 1)


def _window_transactions(by_date, day_repr):
    d = day_repr if isinstance(day_repr, date) else _parse_day(day_repr)
    lo, hi = d - timedelta(days=MATCH_WINDOW_DAYS), d + timedelta(days=MATCH_WINDOW_DAYS)
    out = []
    k = lo
    while k <= hi:
        out.extend(by_date.get(_day_repr(k), ()))
        k += timedelta(days=1)
    return out


def _match_schedules(all_occurs, config, by_date):
    base_occur, occurs = all_occurs[0], all_occurs[1:]
    schedules = []
    for trans in base_occur["transactions"]:
        threshold = approx_number_threshold(trans["amount"])
        payee = trans["payee"]
        found = []
        for occur in occurs:
            matched = None
            for t in occur["transactions"]:
                if t["amount"] >= trans["amount"] - threshold and t["amount"] <= trans["amount"] + threshold:
                    matched = t
                    break
            if matched is not None and matched["payee"] != payee:
                matched = None  # Array.find semantics: first-in-window wins, then payee must match
            if matched is None:
                found.append(None)
            else:
                found.append({"trans": matched, "rank": _rank(occur["date"], matched["date"])})
        if any(f is None for f in found):
            continue
        rank = sum(f["rank"] for f in found) + _rank(base_occur["date"], trans["date"])
        exact_amount = all(f["trans"]["amount"] == trans["amount"] for f in found)
        schedules.append({
            "rank": rank, "amount": trans["amount"], "account": trans.get("account"),
            "payee": payee, "date": config, "exact_date": rank == len(all_occurs),
            "exact_amount": exact_amount,
        })
    return schedules


def _schedules_for_pattern(base_start, num_days, base_config, account, by_date):
    out = []
    for i in range(num_days):
        start = base_start + timedelta(days=i)
        if callable(base_config):
            config = base_config(start)
            if config is False:
                continue
        else:
            config = dict(base_config)
            config["start"] = start
        config["start"] = _day_repr(start) if "start" in config else _day_repr(start)
        data = [{"date": _day_repr(dt), "transactions": _window_transactions(by_date, _day_repr(dt))}
                for dt in take_dates(config)]
        out.extend(_match_schedules(data, config, by_date))
    return out


def _weekly(latest, account, by_date):
    return _schedules_for_pattern(latest - timedelta(weeks=4), 7 * 2, {"frequency": "weekly"}, account, by_date)


def _every_2_weeks(latest, account, by_date):
    return _schedules_for_pattern(latest - timedelta(weeks=7), 7 * 2,
                                  {"frequency": "weekly", "interval": 2}, account, by_date)


def _monthly(latest, account, by_date):
    def cfg(start):
        if start.day > 28:
            return False
        return {"start": start, "frequency": "monthly"}
    return _schedules_for_pattern(_add_months(latest, -4), 31 * 2, cfg, account, by_date)


def _monthly_last_day(latest, account, by_date):
    pattern = {"frequency": "monthly", "patterns": [{"type": "day", "value": -1}]}
    s1 = _schedules_for_pattern(_add_months(latest, -3), 1, pattern, account, by_date)
    s2 = _schedules_for_pattern(_add_months(latest, -4), 1, pattern, account, by_date)
    return s1 + s2


def _monthly_1st_or_3rd(latest, account, by_date, today):
    wd = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"][today.isoweekday() - 1]

    def cfg(start):
        return {"start": start, "frequency": "monthly",
                "patterns": [{"type": wd, "value": 1}, {"type": wd, "value": 3}]}
    return _schedules_for_pattern(latest - timedelta(weeks=8), 14, cfg, account, by_date)


def _monthly_2nd_or_4th(latest, account, by_date, today):
    wd = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"][today.isoweekday() - 1]

    def cfg(start):
        return {"start": start, "frequency": "monthly",
                "patterns": [{"type": wd, "value": 2}, {"type": wd, "value": 4}]}
    return _schedules_for_pattern(_add_months(latest, -8), 14, cfg, account, by_date)


def find_schedules(transactions, today=None, account=None):
    """
    transactions: iterable of {"date": date, "amount": float, "payee": str, "account": any}
    Returns the list of schedules Actual would create, one per payee, best rank
    first -- i.e. the set of payees Actual's "find schedules" would propose.
    """
    txns = list(transactions)
    if not txns:
        return []
    by_account = defaultdict(list)
    for t in txns:
        by_account[t.get("account", account)].append(t)

    today = today or max(t["date"] for t in txns)
    all_schedules = []
    for acct, rows in by_account.items():
        by_date = defaultdict(list)
        for t in rows:
            by_date[_day_repr(t["date"])].append(t)
        latest = max(t["date"] for t in rows)
        all_schedules.extend(_weekly(latest, acct, by_date))
        all_schedules.extend(_every_2_weeks(latest, acct, by_date))
        all_schedules.extend(_monthly(latest, acct, by_date))
        all_schedules.extend(_monthly_last_day(latest, acct, by_date))
        all_schedules.extend(_monthly_1st_or_3rd(latest, acct, by_date, today))
        all_schedules.extend(_monthly_2nd_or_4th(latest, acct, by_date, today))

    grouped = defaultdict(list)
    for s in all_schedules:
        grouped[s["payee"]].append(s)
    winners = []
    for payee, ss in grouped.items():
        ss.sort(key=lambda s: -s["rank"])
        winners.append(ss[0])
    return winners