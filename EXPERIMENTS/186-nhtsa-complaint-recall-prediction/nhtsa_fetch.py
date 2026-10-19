"""E186 fetch layer: NHTSA recalls and complaints."""

from nhtsa_config import COMPONENT_MAP, CATEGORIES, map_component
from nhtsa_stats import parse_date

def fetch_json(url, max_retries=3):
    """Fetch JSON from URL with retries."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'ThinkFree-E186/1.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read().decode('utf-8')
                return json.loads(data)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
    return None

def parse_date(date_str):
    """Parse NHTSA date format (MM/DD/YYYY)."""
    try:
        return datetime.strptime(date_str, '%m/%d/%Y')
    except:
        return None

def fetch_recalls(make, model, year):
    """Fetch recalls for a vehicle model/year."""
    url = f"https://api.nhtsa.gov/recalls/recallsByVehicle?make={urllib.parse.quote(make)}&model={urllib.parse.quote(model)}&modelYear={year}"
    try:
        data = fetch_json(url)
        if not data or 'results' not in data:
            return []
        recalls = []
        for r in data['results']:
            comp = r.get('Component', '')
            cat = map_component(comp)
            date = parse_date(r.get('ReportReceivedDate', ''))
            if date:
                recalls.append({
                    'campaign': r.get('NHTSACampaignNumber', ''),
                    'component': comp,
                    'category': cat,
                    'date': date,
                    'summary': r.get('Summary', '')[:200]
                })
        return recalls
    except Exception as e:
        print(f"  Error fetching recalls: {e}")
        return []

def fetch_complaints(make, model, year, max_pages=5):
    """Fetch complaints for a vehicle model/year (paginated)."""
    all_complaints = []
    for page in range(max_pages):
        url = f"https://api.nhtsa.gov/complaints/complaintsByVehicle?make={urllib.parse.quote(make)}&model={urllib.parse.quote(model)}&modelYear={year}&page={page}"
        try:
            data = fetch_json(url)
            if not data or 'results' not in data or not data['results']:
                break
            for c in data['results']:
                comp = c.get('components', '')
                cat = map_component(comp)
                date = parse_date(c.get('dateComplaintFiled', ''))
                if date:
                    all_complaints.append({
                        'odi': c.get('odiNumber', ''),
                        'component': comp,
                        'category': cat,
                        'date': date,
                        'summary': c.get('summary', '')[:200],
                        'crash': c.get('crash', False),
                        'fire': c.get('fire', False),
                        'injuries': c.get('numberOfInjuries', 0),
                        'deaths': c.get('numberOfDeaths', 0)
                    })
            time.sleep(1)  # Rate limit
        except Exception as e:
            print(f"  Error fetching complaints page {page}: {e}")
            break
    return all_complaints

