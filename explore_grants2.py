#!/usr/bin/env python3
import urllib.request, json

# Explore USAspending grants by category
# Use spending_by_category/recipient for grants

# First, get grant award types
# 02 = Block Grant, 03 = Formula Grant, 04 = Project Grant, 05 = Cooperative Agreement
# 06 = Direct Payment, 07 = Direct Loan, 08 = Guaranteed Loan, 09 = Insurance

url = 'https://api.usaspending.gov/api/v2/search/spending_by_category/recipient/?'
params = {
    "filters": {
        "time_period": [{"start_date": "2020-01-01", "end_date": "2023-12-31"}],
        "award_type_codes": ["02", "03", "04", "05"],  # Grants only
    },
    "category": "recipient",
    "limit": 20,
}
import urllib.parse
full_url = url + urllib.parse.urlencode({"payload": json.dumps(params)})
# Actually, this endpoint might use POST
print(full_url)