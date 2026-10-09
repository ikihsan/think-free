#!/usr/bin/env python3
"""Harvest terminated and completed trials from ClinicalTrials.gov for E075."""
import urllib.request
import json
import time
import os
import sys
import urllib.parse

CONDITIONS = [
    ("cancer", "neoplasms"),
    ("alzheimer", "alzheimer"),
    ("type 2 diabetes", "diabetes type 2"),
]

PER_CONDITION_TERMINATED = 100
PER_CONDITION_COMPLETED = 50
PAGE_SIZE = 50

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_page(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ThinkFree/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())

def fetch_all(base_url, max_results):
    """Fetch all pages using pageToken pagination."""
    results = []
    url = base_url
    while len(results) < max_results:
        try:
            data = fetch_page(url)
            studies = data.get("studies", [])
            if not studies:
                break
            results.extend(studies)
            print(f"  Fetched {len(studies)} studies (total: {len(results)})")
            
            next_token = data.get("nextPageToken")
            if not next_token:
                break
            url = f"{base_url}&pageToken={urllib.parse.quote(next_token)}"
            time.sleep(0.2)
        except Exception as e:
            print(f"  Error: {e}")
            break
    return results[:max_results]

def extract_fields(study):
    """Extract relevant fields from a study."""
    proto = study.get("protocolSection", {})
    ident = proto.get("identificationModule", {})
    status = proto.get("statusModule", {})
    design = proto.get("designModule", {})
    arms = proto.get("armsInterventionsModule", {})
    sponsor = proto.get("sponsorCollaboratorsModule", {})

    return {
        "nct_id": ident.get("nctId", ""),
        "brief_title": ident.get("briefTitle", ""),
        "official_title": ident.get("officialTitle", ""),
        "overall_status": status.get("overallStatus", ""),
        "why_stopped": status.get("whyStopped", ""),
        "start_date": status.get("startDateStruct", {}).get("date", ""),
        "completion_date": status.get("completionDateStruct", {}).get("date", ""),
        "primary_completion_date": status.get("primaryCompletionDateStruct", {}).get("date", ""),
        "enrollment": design.get("enrollmentInfo", {}).get("count", 0),
        "phase": design.get("phases", []),
        "study_type": design.get("studyType", ""),
        "interventions": [i.get("name", "") for i in arms.get("interventions", [])],
        "lead_sponsor": sponsor.get("leadSponsor", {}).get("name", ""),
        "collaborators": [c.get("name", "") for c in sponsor.get("collaborators", [])],
    }

def main():
    all_terminated = []
    all_completed = []

    for cond_query, cond_name in CONDITIONS:
        print(f"\n=== Harvesting {cond_name} ({cond_query}) ===")

        # Terminated trials
        term_url = f"https://clinicaltrials.gov/api/v2/studies?query.cond={urllib.parse.quote(cond_query)}&filter.overallStatus=TERMINATED&pageSize={PAGE_SIZE}"
        term_studies = fetch_all(term_url, PER_CONDITION_TERMINATED)
        term_extracted = [extract_fields(s) for s in term_studies]
        for t in term_extracted:
            t["_condition_query"] = cond_query
            t["_condition_name"] = cond_name
        all_terminated.extend(term_extracted)
        print(f"  Terminated: {len(term_extracted)} extracted")

        # Completed trials (control)
        comp_url = f"https://clinicaltrials.gov/api/v2/studies?query.cond={urllib.parse.quote(cond_query)}&filter.overallStatus=COMPLETED&pageSize={PAGE_SIZE}"
        comp_studies = fetch_all(comp_url, PER_CONDITION_COMPLETED)
        comp_extracted = [extract_fields(s) for s in comp_studies]
        for c in comp_extracted:
            c["_condition_query"] = cond_query
            c["_condition_name"] = cond_name
        all_completed.extend(comp_extracted)
        print(f"  Completed: {len(comp_extracted)} extracted")

        time.sleep(0.5)

    # Save
    term_path = os.path.join(OUTPUT_DIR, "terminated_trials.json")
    comp_path = os.path.join(OUTPUT_DIR, "completed_trials.json")

    with open(term_path, "w") as f:
        json.dump(all_terminated, f, indent=2)
    with open(comp_path, "w") as f:
        json.dump(all_completed, f, indent=2)

    print(f"\n=== Harvest Complete ===")
    print(f"Terminated trials: {len(all_terminated)} saved to {term_path}")
    print(f"Completed trials: {len(all_completed)} saved to {comp_path}")

    # Quick stats
    for cond_name in [c[1] for c in CONDITIONS]:
        term_cond = [t for t in all_terminated if t["_condition_name"] == cond_name]
        comp_cond = [c for c in all_completed if c["_condition_name"] == cond_name]
        print(f"  {cond_name}: {len(term_cond)} terminated, {len(comp_cond)} completed")
        if term_cond:
            enrolled = sum(1 for t in term_cond if t["enrollment"] > 0)
            print(f"    Enrollment > 0: {enrolled}/{len(term_cond)} = {enrolled/len(term_cond):.2%}")

if __name__ == "__main__":
    main()