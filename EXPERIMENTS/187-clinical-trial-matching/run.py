#!/usr/bin/env python3
"""
E187 — Clinical Trial Eligibility Matching (Redesigned)
Fresh exploration: measures structured filtering funnel for patient-trial matching.
Tests whether ClinicalTrials.gov structured fields leave enough matches to be useful.
Stdlib only, no external dependencies.
"""

import urllib.request
import urllib.parse
import json
import time
import statistics
import re
from datetime import datetime
from collections import defaultdict
import sys
import os

# Condition synonyms for matching (simplified MeSH mapping)
CONDITION_SYNONYMS = {
    'breast cancer': ['breast cancer', 'breast carcinoma', 'breast neoplasm', 'mammary cancer'],
    'lung cancer': ['lung cancer', 'lung carcinoma', 'non-small cell lung cancer', 'nsclc', 'small cell lung cancer', 'sclc'],
    'colorectal cancer': ['colorectal cancer', 'colon cancer', 'rectal cancer', 'colorectal carcinoma'],
    'prostate cancer': ['prostate cancer', 'prostatic carcinoma', 'prostate adenocarcinoma'],
    'melanoma': ['melanoma', 'malignant melanoma', 'skin melanoma'],
    'lymphoma': ['lymphoma', 'non-hodgkin lymphoma', 'hodgkin lymphoma', 'nhl'],
    'leukemia': ['leukemia', 'leukaemia', 'acute myeloid leukemia', 'aml', 'acute lymphoblastic leukemia', 'all'],
    'ovarian cancer': ['ovarian cancer', 'ovarian carcinoma', 'ovarian neoplasm'],
    'pancreatic cancer': ['pancreatic cancer', 'pancreatic carcinoma', 'pancreatic adenocarcinoma'],
    'type 2 diabetes': ['type 2 diabetes', 'type 2 diabetes mellitus', 't2dm', 'diabetes mellitus type 2'],
    'type 1 diabetes': ['type 1 diabetes', 'type 1 diabetes mellitus', 't1dm', 'diabetes mellitus type 1'],
    'rheumatoid arthritis': ['rheumatoid arthritis', 'ra', 'rheumatoid disease'],
    'psoriatic arthritis': ['psoriatic arthritis', 'psa'],
    'inflammatory bowel disease': ['inflammatory bowel disease', 'ibd', 'crohn disease', 'ulcerative colitis'],
    'multiple sclerosis': ['multiple sclerosis', 'ms'],
    'alzheimer disease': ['alzheimer disease', 'alzheimer', 'ad'],
    'parkinson disease': ['parkinson disease', 'parkinson', 'pd'],
    'heart failure': ['heart failure', 'cardiac failure', 'chf'],
    'atrial fibrillation': ['atrial fibrillation', 'afib', 'af'],
    'chronic kidney disease': ['chronic kidney disease', 'ckd', 'renal failure'],
    'copd': ['copd', 'chronic obstructive pulmonary disease', 'chronic obstructive lung disease'],
}

# Exclusion keywords that make a trial ineligible unless patient has the condition
EXCLUSION_KEYWORDS = [
    'pregnant', 'pregnancy', 'lactating', 'breastfeeding',
    'transplant', 'transplantation',
    'hiv', 'human immunodeficiency virus',
    'hepatitis b', 'hepatitis c', 'hepatitis',
    'metastatic', 'stage iv', 'stage 4',
    'uncontrolled', 'severe',
]

# Synthetic patient profiles (loaded from JSON to keep file under 300 lines)
def load_patients():
    """Load patient profiles from embedded JSON."""
    return json.loads("""[
  {"id":"P1","condition":"breast cancer","age":52,"sex":"FEMALE","country":"United States","biomarkers":["ER+","HER2-"],"history":[]},
  {"id":"P2","condition":"breast cancer","age":45,"sex":"FEMALE","country":"Canada","biomarkers":["ER+","HER2+"],"history":[]},
  {"id":"P3","condition":"breast cancer","age":60,"sex":"FEMALE","country":"United Kingdom","biomarkers":["triple-negative"],"history":[]},
  {"id":"P4","condition":"breast cancer","age":38,"sex":"FEMALE","country":"Australia","biomarkers":["ER+","HER2-"],"history":[]},
  {"id":"P5","condition":"breast cancer","age":55,"sex":"FEMALE","country":"United States","biomarkers":["ER+","HER2-"],"history":["prior chemo"]},
  {"id":"P6","condition":"lung cancer","age":65,"sex":"MALE","country":"United States","biomarkers":["EGFR+"],"history":[]},
  {"id":"P7","condition":"lung cancer","age":58,"sex":"FEMALE","country":"Canada","biomarkers":["ALK+"],"history":[]},
  {"id":"P8","condition":"lung cancer","age":70,"sex":"MALE","country":"United States","biomarkers":["KRAS+"],"history":["smoker"]},
  {"id":"P9","condition":"lung cancer","age":50,"sex":"FEMALE","country":"United Kingdom","biomarkers":["EGFR+"],"history":["never smoker"]},
  {"id":"P10","condition":"lung cancer","age":62,"sex":"MALE","country":"Australia","biomarkers":[],"history":["prior immunotherapy"]},
  {"id":"P11","condition":"colorectal cancer","age":55,"sex":"MALE","country":"United States","biomarkers":["MSI-H"],"history":[]},
  {"id":"P12","condition":"colorectal cancer","age":48,"sex":"FEMALE","country":"Canada","biomarkers":["KRAS wt"],"history":[]},
  {"id":"P13","condition":"colorectal cancer","age":63,"sex":"MALE","country":"United States","biomarkers":[],"history":["stage III"]},
  {"id":"P14","condition":"colorectal cancer","age":42,"sex":"FEMALE","country":"Germany","biomarkers":["BRAF V600E"],"history":[]},
  {"id":"P15","condition":"colorectal cancer","age":59,"sex":"MALE","country":"France","biomarkers":["MSS"],"history":[]},
  {"id":"P16","condition":"prostate cancer","age":68,"sex":"MALE","country":"United States","biomarkers":["PSA 8.2"],"history":[]},
  {"id":"P17","condition":"prostate cancer","age":72,"sex":"MALE","country":"Canada","biomarkers":["Gleason 7"],"history":["prior ADT"]},
  {"id":"P18","condition":"prostate cancer","age":60,"sex":"MALE","country":"United Kingdom","biomarkers":["PSA 12.5"],"history":[]},
  {"id":"P19","condition":"prostate cancer","age":75,"sex":"MALE","country":"Australia","biomarkers":["metastatic"],"history":["castration-resistant"]},
  {"id":"P20","condition":"prostate cancer","age":55,"sex":"MALE","country":"United States","biomarkers":["Gleason 6"],"history":[]},
  {"id":"P21","condition":"melanoma","age":45,"sex":"MALE","country":"United States","biomarkers":["BRAF V600E"],"history":[]},
  {"id":"P22","condition":"melanoma","age":52,"sex":"FEMALE","country":"Canada","biomarkers":["NRAS+"],"history":[]},
  {"id":"P23","condition":"melanoma","age":38,"sex":"MALE","country":"Australia","biomarkers":["BRAF wt"],"history":["stage III"]},
  {"id":"P24","condition":"melanoma","age":58,"sex":"FEMALE","country":"United Kingdom","biomarkers":["BRAF V600E"],"history":["prior immunotherapy"]},
  {"id":"P25","condition":"melanoma","age":42,"sex":"MALE","country":"Germany","biomarkers":[],"history":[]},
  {"id":"P26","condition":"lymphoma","age":55,"sex":"MALE","country":"United States","biomarkers":["DLBCL"],"history":[]},
  {"id":"P27","condition":"lymphoma","age":40,"sex":"FEMALE","country":"Canada","biomarkers":["follicular"],"history":[]},
  {"id":"P28","condition":"lymphoma","age":62,"sex":"MALE","country":"United States","biomarkers":["mantle cell"],"history":["relapsed"]},
  {"id":"P29","condition":"lymphoma","age":35,"sex":"FEMALE","country":"United Kingdom","biomarkers":["Hodgkin"],"history":[]},
  {"id":"P30","condition":"lymphoma","age":50,"sex":"MALE","country":"France","biomarkers":["DLBCL"],"history":["refractory"]},
  {"id":"P31","condition":"leukemia","age":45,"sex":"MALE","country":"United States","biomarkers":["AML","FLT3+"],"history":[]},
  {"id":"P32","condition":"leukemia","age":60,"sex":"FEMALE","country":"Canada","biomarkers":["CLL"],"history":[]},
  {"id":"P33","condition":"leukemia","age":30,"sex":"MALE","country":"United States","biomarkers":["ALL"],"history":[]},
  {"id":"P34","condition":"leukemia","age":55,"sex":"FEMALE","country":"Germany","biomarkers":["AML","NPM1+"],"history":[]},
  {"id":"P35","condition":"leukemia","age":38,"sex":"MALE","country":"United Kingdom","biomarkers":["CML"],"history":["TKI failure"]},
  {"id":"P36","condition":"ovarian cancer","age":58,"sex":"FEMALE","country":"United States","biomarkers":["BRCA1+"],"history":[]},
  {"id":"P37","condition":"ovarian cancer","age":52,"sex":"FEMALE","country":"Canada","biomarkers":["HRD+"],"history":["platinum-sensitive"]},
  {"id":"P38","condition":"ovarian cancer","age":65,"sex":"FEMALE","country":"United Kingdom","biomarkers":[],"history":["platinum-resistant"]},
  {"id":"P39","condition":"ovarian cancer","age":45,"sex":"FEMALE","country":"Australia","biomarkers":["BRCA2+"],"history":[]},
  {"id":"P40","condition":"ovarian cancer","age":50,"sex":"FEMALE","country":"United States","biomarkers":[],"history":["recurrent"]},
  {"id":"P41","condition":"pancreatic cancer","age":62,"sex":"MALE","country":"United States","biomarkers":["BRCA2+"],"history":[]},
  {"id":"P42","condition":"pancreatic cancer","age":55,"sex":"FEMALE","country":"Canada","biomarkers":[],"history":["locally advanced"]},
  {"id":"P43","condition":"pancreatic cancer","age":68,"sex":"MALE","country":"United Kingdom","biomarkers":[],"history":["metastatic"]},
  {"id":"P44","condition":"pancreatic cancer","age":50,"sex":"FEMALE","country":"Germany","biomarkers":["MSI-H"],"history":[]},
  {"id":"P45","condition":"pancreatic cancer","age":58,"sex":"MALE","country":"France","biomarkers":[],"history":["post-Whipple"]},
  {"id":"P46","condition":"type 2 diabetes","age":58,"sex":"FEMALE","country":"United States","biomarkers":["HbA1c 8.2%"],"history":["metformin"]},
  {"id":"P47","condition":"type 2 diabetes","age":65,"sex":"MALE","country":"Canada","biomarkers":["HbA1c 7.5%"],"history":["insulin"]},
  {"id":"P48","condition":"type 2 diabetes","age":45,"sex":"FEMALE","country":"United Kingdom","biomarkers":["HbA1c 9.0%"],"history":["obesity"]},
  {"id":"P49","condition":"type 2 diabetes","age":52,"sex":"MALE","country":"Australia","biomarkers":["HbA1c 7.8%"],"history":["CKD stage 3"]},
  {"id":"P50","condition":"type 2 diabetes","age":60,"sex":"FEMALE","country":"Germany","biomarkers":["HbA1c 8.5%"],"history":[]},
  {"id":"P51","condition":"type 1 diabetes","age":25,"sex":"MALE","country":"United States","biomarkers":["HbA1c 7.2%"],"history":["CGM","pump"]},
  {"id":"P52","condition":"type 1 diabetes","age":35,"sex":"FEMALE","country":"Canada","biomarkers":["HbA1c 8.0%"],"history":["MDI"]},
  {"id":"P53","condition":"type 1 diabetes","age":18,"sex":"MALE","country":"United Kingdom","biomarkers":["HbA1c 8.5%"],"history":[]},
  {"id":"P54","condition":"type 1 diabetes","age":40,"sex":"FEMALE","country":"Australia","biomarkers":["HbA1c 7.0%"],"history":["pump"]},
  {"id":"P55","condition":"type 1 diabetes","age":30,"sex":"MALE","country":"Germany","biomarkers":["HbA1c 7.8%"],"history":["CGM"]},
  {"id":"P56","condition":"rheumatoid arthritis","age":40,"sex":"FEMALE","country":"United States","biomarkers":["seropositive","RF+","CCP+"],"history":["methotrexate"]},
  {"id":"P57","condition":"rheumatoid arthritis","age":55,"sex":"FEMALE","country":"Canada","biomarkers":["seronegative"],"history":["biologic failure"]},
  {"id":"P58","condition":"rheumatoid arthritis","age":50,"sex":"MALE","country":"United Kingdom","biomarkers":["seropositive"],"history":["TNF inhibitor"]},
  {"id":"P59","condition":"rheumatoid arthritis","age":45,"sex":"FEMALE","country":"Germany","biomarkers":["seropositive"],"history":[]},
  {"id":"P60","condition":"rheumatoid arthritis","age":60,"sex":"MALE","country":"France","biomarkers":["seronegative"],"history":["JAK inhibitor"]},
  {"id":"P61","condition":"psoriatic arthritis","age":42,"sex":"MALE","country":"United States","biomarkers":["psoriasis"],"history":["TNF inhibitor"]},
  {"id":"P62","condition":"psoriatic arthritis","age":38,"sex":"FEMALE","country":"Canada","biomarkers":[],"history":[]},
  {"id":"P63","condition":"psoriatic arthritis","age":50,"sex":"MALE","country":"United Kingdom","biomarkers":["dactylitis"],"history":["IL-17 inhibitor"]},
  {"id":"P64","condition":"psoriatic arthritis","age":45,"sex":"FEMALE","country":"Australia","biomarkers":["enthesitis"],"history":[]},
  {"id":"P65","condition":"psoriatic arthritis","age":55,"sex":"MALE","country":"France","biomarkers":[],"history":["methotrexate"]},
  {"id":"P66","condition":"inflammatory bowel disease","age":30,"sex":"FEMALE","country":"United States","biomarkers":["Crohn"],"history":["anti-TNF failure"]},
  {"id":"P67","condition":"inflammatory bowel disease","age":35,"sex":"MALE","country":"Canada","biomarkers":["ulcerative colitis"],"history":[]},
  {"id":"P68","condition":"inflammatory bowel disease","age":28,"sex":"FEMALE","country":"United Kingdom","biomarkers":["Crohn"],"history":["stricture"]},
  {"id":"P69","condition":"inflammatory bowel disease","age":40,"sex":"MALE","country":"Germany","biomarkers":["ulcerative colitis"],"history":["biologic naive"]},
  {"id":"P70","condition":"inflammatory bowel disease","age":32,"sex":"FEMALE","country":"France","biomarkers":["Crohn"],"history":["perianal disease"]},
  {"id":"P71","condition":"multiple sclerosis","age":32,"sex":"FEMALE","country":"United States","biomarkers":["relapsing-remitting"],"history":["DMT failure"]},
  {"id":"P72","condition":"multiple sclerosis","age":40,"sex":"MALE","country":"Canada","biomarkers":["primary progressive"],"history":[]},
  {"id":"P73","condition":"multiple sclerosis","age":28,"sex":"FEMALE","country":"United Kingdom","biomarkers":["relapsing-remitting"],"history":[]},
  {"id":"P74","condition":"multiple sclerosis","age":38,"sex":"MALE","country":"Germany","biomarkers":["secondary progressive"],"history":["anti-CD20"]},
  {"id":"P75","condition":"multiple sclerosis","age":35,"sex":"FEMALE","country":"France","biomarkers":["relapsing-remitting"],"history":["natalizumab"]},
  {"id":"P76","condition":"alzheimer disease","age":72,"sex":"FEMALE","country":"United States","biomarkers":["amyloid+","tau+"],"history":["MCI"]},
  {"id":"P77","condition":"alzheimer disease","age":68,"sex":"MALE","country":"Canada","biomarkers":["amyloid+"],"history":["early onset"]},
  {"id":"P78","condition":"alzheimer disease","age":75,"sex":"FEMALE","country":"United Kingdom","biomarkers":["APOE4/4"],"history":[]},
  {"id":"P79","condition":"alzheimer disease","age":70,"sex":"MALE","country":"Germany","biomarkers":["amyloid+"],"history":["donepezil"]},
  {"id":"P80","condition":"alzheimer disease","age":65,"sex":"FEMALE","country":"France","biomarkers":[],"history":["MCI"]},
  {"id":"P81","condition":"parkinson disease","age":62,"sex":"MALE","country":"United States","biomarkers":["motor fluctuations"],"history":["levodopa"]},
  {"id":"P82","condition":"parkinson disease","age":58,"sex":"FEMALE","country":"Canada","biomarkers":["tremor dominant"],"history":[]},
  {"id":"P83","condition":"parkinson disease","age":65,"sex":"MALE","country":"United Kingdom","biomarkers":[],"history":["DBS candidate"]},
  {"id":"P84","condition":"parkinson disease","age":55,"sex":"FEMALE","country":"Germany","biomarkers":["early onset"],"history":[]},
  {"id":"P85","condition":"parkinson disease","age":70,"sex":"MALE","country":"France","biomarkers":[],"history":["levodopa"]},
  {"id":"P86","condition":"heart failure","age":65,"sex":"MALE","country":"United States","biomarkers":["HFrEF","EF 30%"],"history":["GDMT"]},
  {"id":"P87","condition":"heart failure","age":70,"sex":"FEMALE","country":"Canada","biomarkers":["HFpEF","EF 55%"],"history":["AFib"]},
  {"id":"P88","condition":"heart failure","age":58,"sex":"MALE","country":"United Kingdom","biomarkers":["HFrEF","EF 25%"],"history":["ICD"]},
  {"id":"P89","condition":"heart failure","age":62,"sex":"FEMALE","country":"Germany","biomarkers":["HFrEF","EF 35%"],"history":["CRT"]},
  {"id":"P90","condition":"heart failure","age":75,"sex":"MALE","country":"France","biomarkers":["HFpEF"],"history":["hypertension"]},
  {"id":"P91","condition":"atrial fibrillation","age":68,"sex":"MALE","country":"United States","biomarkers":["paroxysmal"],"history":["anticoagulated"]},
  {"id":"P92","condition":"atrial fibrillation","age":72,"sex":"FEMALE","country":"Canada","biomarkers":["persistent"],"history":["ablation"]},
  {"id":"P93","condition":"atrial fibrillation","age":60,"sex":"MALE","country":"United Kingdom","biomarkers":["paroxysmal"],"history":[]},
  {"id":"P94","condition":"atrial fibrillation","age":75,"sex":"FEMALE","country":"Germany","biomarkers":["permanent"],"history":["rate control"]},
  {"id":"P95","condition":"atrial fibrillation","age":55,"sex":"MALE","country":"France","biomarkers":["paroxysmal"],"history":[]},
  {"id":"P96","condition":"chronic kidney disease","age":55,"sex":"FEMALE","country":"United States","biomarkers":["CKD stage 3b","eGFR 38"],"history":["diabetes"]},
  {"id":"P97","condition":"chronic kidney disease","age":62,"sex":"MALE","country":"Canada","biomarkers":["CKD stage 4","eGFR 22"],"history":["hypertension"]},
  {"id":"P98","condition":"chronic kidney disease","age":48,"sex":"FEMALE","country":"United Kingdom","biomarkers":["CKD stage 3a","eGFR 48"],"history":["IgA nephropathy"]},
  {"id":"P99","condition":"chronic kidney disease","age":58,"sex":"MALE","country":"Germany","biomarkers":["CKD stage 3b","eGFR 35"],"history":[]},
  {"id":"P100","condition":"chronic kidney disease","age":65,"sex":"FEMALE","country":"France","biomarkers":["CKD stage 4","eGFR 20"],"history":["pre-dialysis"]}
]""")

PATIENT_PROFILES = load_patients()