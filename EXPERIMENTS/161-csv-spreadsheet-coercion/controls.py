"""E161 control arm: values that people report being altered by spreadsheets,
put through the same engine so the engine's behaviour is measured, not assumed.

One value per row, a label in the first column.  These are the folklore cases:
postcodes, FIPS codes, phone numbers, account numbers, long identifiers, the
date formats a real system emits, and the numeric spellings spreadsheets and
CSV writers disagree about.
"""

ROWS = [
    ("leading_zero_5", "01234"),
    ("leading_zero_2", "07"),
    ("leading_zero_zero", "0"),
    ("leading_zero_plus", "+01234"),
    ("leading_zero_zip_5", "02108"),
    ("leading_zero_uk_postcode", "01234"),
    ("leading_zero_account", "0001234567890123"),
    ("leading_zero_phone", "01234567890"),
    ("long_16_digits", "4111111111111111"),
    ("long_17_digits", "12345678901234567"),
    ("long_20_digits", "12345678901234567890"),
    ("long_15_digits", "123456789012345"),
    ("long_float", "1234567890.123456789"),
    ("isbn13", "9780306406157"),
    ("credit_card_spaces", "4111 1111 1111 1111"),
    ("credit_card_dashes", "4111-1111-1111-1111"),
    ("vin", "1HGBH41JXMN109186"),
    ("iban", "GB82 WEST 1234 5698 7654 32"),
    ("us_phone_parens", "(555) 123-4567"),
    ("us_phone_plain", "8005551212"),
    ("intl_phone", "+1-800-555-1212"),
    ("uk_phone_spaces", "020 7946 0018"),
    ("date_iso", "2020-01-02"),
    ("date_slash_us", "01/02/2020"),
    ("date_slash_ambig", "1/2/2020"),
    ("date_slash_2digit", "01/02/20"),
    ("date_dotted", "02.01.2020"),
    ("date_dash_us", "01-02-2020"),
    ("date_slash_iso", "2020/01/02"),
    ("date_month_name", "2-Jan-2020"),
    ("date_month_full", "January 2, 2020"),
    ("datetime_us_midnight", "02/09/2005 12:00:00 AM"),
    ("datetime_us_afternoon", "02/09/2005 01:30:00 PM"),
    ("datetime_us_morning", "02/09/2005 09:05:00 AM"),
    ("datetime_iso_afternoon", "2020-01-02T13:45:30"),
    ("datetime_iso", "2020-01-02T15:04:05"),
    ("datetime_z", "2020-01-02T15:04:05Z"),
    ("time_24h", "12:30"),
    ("time_sec", "12:30:45"),
    ("time_ampm", "1:30 PM"),
    ("percent", "12%"),
    ("percent_float", "0.12"),
    ("currency_usd", "$1,234.56"),
    ("currency_plain", "1234.56"),
    ("thousands_quoted", "1,234"),
    ("thousands_narrow_nbsp", "1 234"),
    ("decimal_comma", "1.234,56"),
    ("sci_upper", "1.5E10"),
    ("sci_lower", "1e-7"),
    ("sci_long", "1.23456789012345678E18"),
    ("trailing_dot", "5."),
    ("leading_dot", ".5"),
    ("leading_plus", "+.5"),
    ("negative", "-1234"),
    ("bool_true", "TRUE"),
    ("bool_yes", "Yes"),
    ("leading_space", " 12345"),
    ("trailing_space", "12345 "),
    ("inner_tab", "12\t34"),
    ("equals_formula", "=1+1"),
    ("plus_formula", "+1-1"),
    ("at_formula", "@SUM(A1)"),
    ("url", "http://opendatacommunities.org/id/london-borough-council/camden"),
    ("email", "a.b@example.gov.uk"),
    ("serial_number", "38392"),
    ("hash_ref", "PREM-LIC\\1617"),
    ("uuid", "3f2504e0-4f89-11d3-9a0c-0305e82c3301"),
    ("text_255", "x" * 255),
    ("text_300", "y" * 300),
    ("accented", "Zürich"),
    ("cjk", "東京都"),
    ("emoji", "a\U0001f600b"),
    ("null_text", "NULL"),
    ("nan_text", "NaN"),
    ("infinity", "Infinity"),
    ("trailing_zero", "1.50"),
    ("big_int_no_frac", "1000000000000"),
    ("one", "1"),
]


def write(path):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("label,value\n")
        for label, value in ROWS:
            f.write('"%s","%s"\n' % (label, value.replace('"', '""')))
    return len(ROWS)


if __name__ == "__main__":
    import os
    import sys
    d = sys.argv[1] if len(sys.argv) > 1 else "controls"
    os.makedirs(d, exist_ok=True)
    print(write(os.path.join(d, "controls.csv")))