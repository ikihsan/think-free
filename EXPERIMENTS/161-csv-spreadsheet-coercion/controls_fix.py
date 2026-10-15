"""E161 fix arm: the escapes people use to stop a spreadsheet reinterpreting a
CSV cell, put through the same engine so their effect is measured, not assumed.

For each dangerous value, every candidate escape is written as its own row.  A
fix works if the engine stores the value itself, as text, with no extra
characters.
"""

VALUES = ["01234", "0001234567890123", "4111111111111111", "2020-01-02",
          "12:30:45", "1,234", "00", "1.50", "TRUE", "=1+1"]

METHODS = [
    ("plain", lambda v: v),
    ("quote", lambda v: '"%s"' % v),
    ("apos", lambda v: "'" + v),
    ("formula", lambda v: '="%s"' % v),
    ("tab", lambda v: "\\t" + v),
    ("apos_formula", lambda v: "'=\"%s\"" % v),
]


def write(path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("value,method,escaped\n")
        for v in VALUES:
            for name, fn in METHODS:
                f.write('"%s","%s","%s"\n' % (v, name, fn(v).replace('"', '""')))
    return len(VALUES) * len(METHODS)


if __name__ == "__main__":
    import os
    import sys
    d = sys.argv[1] if len(sys.argv) > 1 else "controls-fix"
    os.makedirs(d, exist_ok=True)
    print(write(os.path.join(d, "controls-fix.csv")))