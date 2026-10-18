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

# Synthetic patient profiles
PATIENT_PROFILES = [
    # Breast Cancer
    {'id': 'P1', 'condition': 'breast cancer', 'age': 52, 'sex': 'FEMALE', 'country': 'United States', 'biomarkers': ['ER+', 'HER2-'], 'history': []},
    {'id': 'P2', 'condition': 'breast cancer', 'age': 45, 'sex': 'FEMALE', 'country': 'Canada', 'biomarkers': ['ER+', 'HER2+'], 'history': []},
    {'id': 'P3', 'condition': 'breast cancer', 'age': 60, 'sex': 'FEMALE', 'country': 'United Kingdom', 'biomarkers': ['triple-negative'], 'history': []},
    {'id': 'P4', 'condition': 'breast cancer', 'age': 38, 'sex': 'FEMALE', 'country': 'Australia', 'biomarkers': ['ER+', 'HER2-'], 'history': []},
    {'id': 'P5', 'condition': 'breast cancer', 'age': 55, 'sex': 'FEMALE', 'country': 'United States', 'biomarkers': ['ER+', 'HER2-'], 'history': ['prior chemo']},
    
    # Lung Cancer
    {'id': 'P6', 'condition': 'lung cancer', 'age': 65, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['EGFR+'], 'history': []},
    {'id': 'P7', 'condition': 'lung cancer', 'age': 58, 'sex': 'FEMALE', 'country': 'Canada', 'biomarkers': ['ALK+'], 'history': []},
    {'id': 'P8', 'condition': 'lung cancer', 'age': 70, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['KRAS+'], 'history': ['smoker']},
    {'id': 'P9', 'condition': 'lung cancer', 'age': 50, 'sex': 'FEMALE', 'country': 'United Kingdom', 'biomarkers': ['EGFR+'], 'history': ['never smoker']},
    {'id': 'P10', 'condition': 'lung cancer', 'age': 62, 'sex': 'MALE', 'country': 'Australia', 'biomarkers': [], 'history': ['prior immunotherapy']},
    
    # Colorectal Cancer
    {'id': 'P11', 'condition': 'colorectal cancer', 'age': 55, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['MSI-H'], 'history': []},
    {'id': 'P12', 'condition': 'colorectal cancer', 'age': 48, 'sex': 'FEMALE', 'country': 'Canada', 'biomarkers': ['KRAS wt'], 'history': []},
    {'id': 'P13', 'condition': 'colorectal cancer', 'age': 63, 'sex': 'MALE', 'country': 'United States', 'biomarkers': [], 'history': ['stage III']},
    {'id': 'P14', 'condition': 'colorectal cancer', 'age': 42, 'sex': 'FEMALE', 'country': 'Germany', 'biomarkers': ['BRAF V600E'], 'history': []},
    {'id': 'P15', 'condition': 'colorectal cancer', 'age': 59, 'sex': 'MALE', 'country': 'France', 'biomarkers': ['MSS'], 'history': []},
    
    # Prostate Cancer
    {'id': 'P16', 'condition': 'prostate cancer', 'age': 68, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['PSA 8.2'], 'history': []},
    {'id': 'P17', 'condition': 'prostate cancer', 'age': 72, 'sex': 'MALE', 'country': 'Canada', 'biomarkers': ['Gleason 7'], 'history': ['prior ADT']},
    {'id': 'P18', 'condition': 'prostate cancer', 'age': 60, 'sex': 'MALE', 'country': 'United Kingdom', 'biomarkers': ['PSA 12.5'], 'history': []},
    {'id': 'P19', 'condition': 'prostate cancer', 'age': 75, 'sex': 'MALE', 'country': 'Australia', 'biomarkers': ['metastatic'], 'history': ['castration-resistant']},
    {'id': 'P20', 'condition': 'prostate cancer', 'age': 55, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['Gleason 6'], 'history': []},
    
    # Melanoma
    {'id': 'P21', 'condition': 'melanoma', 'age': 45, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['BRAF V600E'], 'history': []},
    {'id': 'P22', 'condition': 'melanoma', 'age': 52, 'sex': 'FEMALE', 'country': 'Canada', 'biomarkers': ['NRAS+'], 'history': []},
    {'id': 'P23', 'condition': 'melanoma', 'age': 38, 'sex': 'MALE', 'country': 'Australia', 'biomarkers': ['BRAF wt'], 'history': ['stage III']},
    {'id': 'P24', 'condition': 'melanoma', 'age': 58, 'sex': 'FEMALE', 'country': 'United Kingdom', 'biomarkers': ['BRAF V600E'], 'history': ['prior immunotherapy']},
    {'id': 'P25', 'condition': 'melanoma', 'age': 42, 'sex': 'MALE', 'country': 'Germany', 'biomarkers': [], 'history': []},
    
    # Lymphoma
    {'id': 'P26', 'condition': 'lymphoma', 'age': 55, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['DLBCL'], 'history': []},
    {'id': 'P27', 'condition': 'lymphoma', 'age': 40, 'sex': 'FEMALE', 'country': 'Canada', 'biomarkers': ['follicular'], 'history': []},
    {'id': 'P28', 'condition': 'lymphoma', 'age': 62, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['mantle cell'], 'history': ['relapsed']},
    {'id': 'P29', 'condition': 'lymphoma', 'age': 35, 'sex': 'FEMALE', 'country': 'United Kingdom', 'biomarkers': ['Hodgkin'], 'history': []},
    {'id': 'P30', 'condition': 'lymphoma', 'age': 50, 'sex': 'MALE', 'country': 'France', 'biomarkers': ['DLBCL'], 'history': ['refractory']},
    
    # Leukemia
    {'id': 'P31', 'condition': 'leukemia', 'age': 45, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['AML', 'FLT3+'], 'history': []},
    {'id': 'P32', 'condition': 'leukemia', 'age': 60, 'sex': 'FEMALE', 'country': 'Canada', 'biomarkers': ['CLL'], 'history': []},
    {'id': 'P33', 'condition': 'leukemia', 'age': 30, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['ALL'], 'history': []},
    {'id': 'P34', 'condition': 'leukemia', 'age': 55, 'sex': 'FEMALE', 'country': 'Germany', 'biomarkers': ['AML', 'NPM1+'], 'history': []},
    {'id': 'P35', 'condition': 'leukemia', 'age': 38, 'sex': 'MALE', 'country': 'United Kingdom', 'biomarkers': ['CML'], 'history': ['TKI failure']},
    
    # Ovarian Cancer
    {'id': 'P36', 'condition': 'ovarian cancer', 'age': 58, 'sex': 'FEMALE', 'country': 'United States', 'biomarkers': ['BRCA1+'], 'history': []},
    {'id': 'P37', 'condition': 'ovarian cancer', 'age': 52, 'sex': 'FEMALE', 'country': 'Canada', 'biomarkers': ['HRD+'], 'history': ['platinum-sensitive']},
    {'id': 'P38', 'condition': 'ovarian cancer', 'age': 65, 'sex': 'FEMALE', 'country': 'United Kingdom', 'biomarkers': [], 'history': ['platinum-resistant']},
    {'id': 'P39', 'condition': 'ovarian cancer', 'age': 45, 'sex': 'FEMALE', 'country': 'Australia', 'biomarkers': ['BRCA2+'], 'history': []},
    {'id': 'P40', 'condition': 'ovarian cancer', 'age': 50, 'sex': 'FEMALE', 'country': 'United States', 'biomarkers': [], 'history': ['recurrent']},
    
    # Pancreatic Cancer
    {'id': 'P41', 'condition': 'pancreatic cancer', 'age': 62, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['BRCA2+'], 'history': []},
    {'id': 'P42', 'condition': 'pancreatic cancer', 'age': 55, 'sex': 'FEMALE', 'country': 'Canada', 'biomarkers': [], 'history': ['locally advanced']},
    {'id': 'P43', 'condition': 'pancreatic cancer', 'age': 68, 'sex': 'MALE', 'country': 'United Kingdom', 'biomarkers': [], 'history': ['metastatic']},
    {'id': 'P44', 'condition': 'pancreatic cancer', 'age': 50, 'sex': 'FEMALE', 'country': 'Germany', 'biomarkers': ['MSI-H'], 'history': []},
    {'id': 'P45', 'condition': 'pancreatic cancer', 'age': 58, 'sex': 'MALE', 'country': 'France', 'biomarkers': [], 'history': ['post-Whipple']},
    
    # Type 2 Diabetes
    {'id': 'P46', 'condition': 'type 2 diabetes', 'age': 58, 'sex': 'FEMALE', 'country': 'United States', 'biomarkers': ['HbA1c 8.2%'], 'history': ['metformin']},
    {'id': 'P47', 'condition': 'type 2 diabetes', 'age': 65, 'sex': 'MALE', 'country': 'Canada', 'biomarkers': ['HbA1c 7.5%'], 'history': ['insulin']},
    {'id': 'P48', 'condition': 'type 2 diabetes', 'age': 45, 'sex': 'FEMALE', 'country': 'United Kingdom', 'biomarkers': ['HbA1c 9.0%'], 'history': ['obesity']},
    {'id': 'P49', 'condition': 'type 2 diabetes', 'age': 52, 'sex': 'MALE', 'country': 'Australia', 'biomarkers': ['HbA1c 7.8%'], 'history': ['CKD stage 3']},
    {'id': 'P50', 'condition': 'type 2 diabetes', 'age': 60, 'sex': 'FEMALE', 'country': 'Germany', 'biomarkers': ['HbA1c 8.5%'], 'history': []},
    
    # Type 1 Diabetes
    {'id': 'P51', 'condition': 'type 1 diabetes', 'age': 25, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['HbA1c 7.2%'], 'history': ['CGM', 'pump']},
    {'id': 'P52', 'condition': 'type 1 diabetes', 'age': 35, 'sex': 'FEMALE', 'country': 'Canada', 'biomarkers': ['HbA1c 8.0%'], 'history': ['MDI']},
    {'id': 'P53', 'condition': 'type 1 diabetes', 'age': 18, 'sex': 'MALE', 'country': 'United Kingdom', 'biomarkers': ['HbA1c 8.5%'], 'history': []},
    {'id': 'P54', 'condition': 'type 1 diabetes', 'age': 40, 'sex': 'FEMALE', 'country': 'Australia', 'biomarkers': ['HbA1c 7.0%'], 'history': ['pump']},
    {'id': 'P55', 'condition': 'type 1 diabetes', 'age': 30, 'sex': 'MALE', 'country': 'Germany', 'biomarkers': ['HbA1c 7.8%'], 'history': ['CGM']},
    
    # Rheumatoid Arthritis
    {'id': 'P56', 'condition': 'rheumatoid arthritis', 'age': 40, 'sex': 'FEMALE', 'country': 'United States', 'biomarkers': ['seropositive', 'RF+', 'CCP+'], 'history': ['methotrexate']},
    {'id': 'P57', 'condition': 'rheumatoid arthritis', 'age': 55, 'sex': 'FEMALE', 'country': 'Canada', 'biomarkers': ['seronegative'], 'history': ['biologic failure']},
    {'id': 'P58', 'condition': 'rheumatoid arthritis', 'age': 50, 'sex': 'MALE', 'country': 'United Kingdom', 'biomarkers': ['seropositive'], 'history': ['TNF inhibitor']},
    {'id': 'P59', 'condition': 'rheumatoid arthritis', 'age': 45, 'sex': 'FEMALE', 'country': 'Germany', 'biomarkers': ['seropositive'], 'history': []},
    {'id': 'P60', 'condition': 'rheumatoid arthritis', 'age': 60, 'sex': 'MALE', 'country': 'France', 'biomarkers': ['seronegative'], 'history': ['JAK inhibitor']},
    
    # Psoriatic Arthritis
    {'id': 'P61', 'condition': 'psoriatic arthritis', 'age': 42, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['psoriasis'], 'history': ['TNF inhibitor']},
    {'id': 'P62', 'condition': 'psoriatic arthritis', 'age': 38, 'sex': 'FEMALE', 'country': 'Canada', 'biomarkers': [], 'history': []},
    {'id': 'P63', 'condition': 'psoriatic arthritis', 'age': 50, 'sex': 'MALE', 'country': 'United Kingdom', 'biomarkers': ['dactylitis'], 'history': ['IL-17 inhibitor']},
    {'id': 'P64', 'condition': 'psoriatic arthritis', 'age': 45, 'sex': 'FEMALE', 'country': 'Australia', 'biomarkers': ['enthesitis'], 'history': []},
    {'id': 'P65', 'condition': 'psoriatic arthritis', 'age': 55, 'sex': 'MALE', 'country': 'France', 'biomarkers': [], 'history': ['methotrexate']},
    
    # Inflammatory Bowel Disease
    {'id': 'P66', 'condition': 'inflammatory bowel disease', 'age': 30, 'sex': 'FEMALE', 'country': 'United States', 'biomarkers': ['Crohn'], 'history': ['anti-TNF failure']},
    {'id': 'P67', 'condition': 'inflammatory bowel disease', 'age': 35, 'sex': 'MALE', 'country': 'Canada', 'biomarkers': ['ulcerative colitis'], 'history': []},
    {'id': 'P68', 'condition': 'inflammatory bowel disease', 'age': 28, 'sex': 'FEMALE', 'country': 'United Kingdom', 'biomarkers': ['Crohn'], 'history': ['stricture']},
    {'id': 'P69', 'condition': 'inflammatory bowel disease', 'age': 40, 'sex': 'MALE', 'country': 'Germany', 'biomarkers': ['ulcerative colitis'], 'history': ['biologic naive']},
    {'id': 'P70', 'condition': 'inflammatory bowel disease', 'age': 32, 'sex': 'FEMALE', 'country': 'France', 'biomarkers': ['Crohn'], 'history': ['perianal disease']},
    
    # Multiple Sclerosis
    {'id': 'P71', 'condition': 'multiple sclerosis', 'age': 32, 'sex': 'FEMALE', 'country': 'United States', 'biomarkers': ['relapsing-remitting'], 'history': ['DMT failure']},
    {'id': 'P72', 'condition': 'multiple sclerosis', 'age': 40, 'sex': 'MALE', 'country': 'Canada', 'biomarkers': ['primary progressive'], 'history': []},
    {'id': 'P73', 'condition': 'multiple sclerosis', 'age': 28, 'sex': 'FEMALE', 'country': 'United Kingdom', 'biomarkers': ['relapsing-remitting'], 'history': []},
    {'id': 'P74', 'condition': 'multiple sclerosis', 'age': 38, 'sex': 'MALE', 'country': 'Germany', 'biomarkers': ['secondary progressive'], 'history': ['anti-CD20']},
    {'id': 'P75', 'condition': 'multiple sclerosis', 'age': 35, 'sex': 'FEMALE', 'country': 'France', 'biomarkers': ['relapsing-remitting'], 'history': ['natalizumab']},
    
    # Alzheimer Disease
    {'id': 'P76', 'condition': 'alzheimer disease', 'age': 72, 'sex': 'FEMALE', 'country': 'United States', 'biomarkers': ['amyloid+', 'tau+'], 'history': ['MCI']},
    {'id': 'P77', 'condition': 'alzheimer disease', 'age': 68, 'sex': 'MALE', 'country': 'Canada', 'biomarkers': ['amyloid+'], 'history': ['early onset']},
    {'id': 'P78', 'condition': 'alzheimer disease', 'age': 75, 'sex': 'FEMALE', 'country': 'United Kingdom', 'biomarkers': ['APOE4/4'], 'history': []},
    {'id': 'P79', 'condition': 'alzheimer disease', 'age': 70, 'sex': 'MALE', 'country': 'Germany', 'biomarkers': ['amyloid+'], 'history': ['donepezil']},
    {'id': 'P80', 'condition': 'alzheimer disease', 'age': 65, 'sex': 'FEMALE', 'country': 'France', 'biomarkers': [], 'history': ['MCI']},
    
    # Parkinson Disease
    {'id': 'P81', 'condition': 'parkinson disease', 'age': 62, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['motor fluctuations'], 'history': ['levodopa']},
    {'id': 'P82', 'condition': 'parkinson disease', 'age': 58, 'sex': 'FEMALE', 'country': 'Canada', 'biomarkers': ['tremor dominant'], 'history': []},
    {'id': 'P83', 'condition': 'parkinson disease', 'age': 65, 'sex': 'MALE', 'country': 'United Kingdom', 'biomarkers': [], 'history': ['DBS candidate']},
    {'id': 'P84', 'condition': 'parkinson disease', 'age': 55, 'sex': 'FEMALE', 'country': 'Germany', 'biomarkers': ['early onset'], 'history': []},
    {'id': 'P85', 'condition': 'parkinson disease', 'age': 70, 'sex': 'MALE', 'country': 'France', 'biomarkers': [], 'history': ['levodopa']},
    
    # Heart Failure
    {'id': 'P86', 'condition': 'heart failure', 'age': 65, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['HFrEF', 'EF 30%'], 'history': ['GDMT']},
    {'id': 'P87', 'condition': 'heart failure', 'age': 70, 'sex': 'FEMALE', 'country': 'Canada', 'biomarkers': ['HFpEF', 'EF 55%'], 'history': ['AFib']},
    {'id': 'P88', 'condition': 'heart failure', 'age': 58, 'sex': 'MALE', 'country': 'United Kingdom', 'biomarkers': ['HFrEF', 'EF 25%'], 'history': ['ICD']},
    {'id': 'P89', 'condition': 'heart failure', 'age': 62, 'sex': 'FEMALE', 'country': 'Germany', 'biomarkers': ['HFrEF', 'EF 35%'], 'history': ['CRT']},
    {'id': 'P90', 'condition': 'heart failure', 'age': 75, 'sex': 'MALE', 'country': 'France', 'biomarkers': ['HFpEF'], 'history': ['hypertension']},
    
    # Atrial Fibrillation
    {'id': 'P91', 'condition': 'atrial fibrillation', 'age': 68, 'sex': 'MALE', 'country': 'United States', 'biomarkers': ['paroxysmal'], 'history': ['anticoagulated']},
    {'id': 'P92', 'condition': 'atrial fibrillation', 'age': 72, 'sex': 'FEMALE', 'country': 'Canada', 'biomarkers': ['persistent'], 'history': ['ablation']},
    {'id': 'P93', 'condition': 'atrial fibrillation', 'age': 60, 'sex': 'MALE', 'country': 'United Kingdom', 'biomarkers': ['paroxysmal'], 'history': []},
    {'id': 'P94', 'condition': 'atrial fibrillation', 'age': 75, 'sex': 'FEMALE', 'country': 'Germany', 'biomarkers': ['permanent'], 'history': ['rate control']},
    {'id': 'P95', 'condition': 'atrial fibrillation', 'age': 55, 'sex': 'MALE', 'country': 'France', 'biomarkers': ['paroxysmal'], 'history': []},
    
    # Chronic Kidney Disease
    {'id': 'P96', 'condition': 'chronic kidney disease', 'age': 55, 'sex': 'FEMALE', 'country': 'United States', 'biomarkers': ['CKD stage 3b', 'eGFR 38'], 'history': ['diabetes']},
    {'id': 'P97', 'condition': 'chronic kidney disease', 'age': 62, 'sex': 'MALE', 'country': 'Canada', 'biomarkers': ['CKD stage 4', 'eGFR 22'], 'history': ['hypertension']},
    {'id': 'P98', 'condition': 'chronic kidney disease', 'age': 48, 'sex': 'FEMALE', 'country': 'United Kingdom', 'biomarkers': ['CKD stage 3a', 'eGFR 48'], 'history': ['IgA nephropathy']},
    {'id': 'P99', 'condition': 'chronic kidney disease', 'age': 58, 'sex': 'MALE', 'country': 'Germany', 'biomarkers': ['CKD stage 3b', 'eGFR 35'], 'history': []},
    {'id': 'P100', 'condition': 'chronic kidney disease', 'age': 65, 'sex': 'FEMALE', 'country': 'France', 'biomarkers': ['CKD stage 4', 'eGFR 20'], 'history': ['pre-dialysis']},
]

def fetch_json(url, max_retries=3):
    """Fetch JSON from URL with retries."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'ThinkFree-E187/1.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read().decode('utf-8')
                return json.loads(data)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
    return None

def parse_age_range(min_age_str, std_ages):
    """Parse minimum age and stdAges to get min/max age in years."""
    min_age = 0
    max_age = 120
    
    if min_age_str:
        match = re.search(r'(\d+)', min_age_str)
        if match:
            min_age = int(match.group(1))
    
    if std_ages:
        if 'CHILD' in std_ages:
            max_age = min(max_age, 17)
        if 'ADULT' in std_ages:
            max_age = max(max_age, 18)
        if 'OLDER_ADULT' in std_ages:
            max_age = 120
    
    return min_age, max_age

def extract_locations(trial):
    """Extract recruiting countries from trial locations."""
    countries = set()
    try:
        locations = trial.get('protocolSection', {}).get('contactsLocationsModule', {}).get('locations', [])
        for loc in locations:
            if loc.get('status') == 'RECRUITING':
                country = loc.get('country', '').strip()
                if country:
                    countries.add(country)
    except:
        pass
    return countries

def extract_eligibility(trial):
    """Extract structured eligibility info from trial."""
    elig = trial.get('protocolSection', {}).get('eligibilityModule', {})
    return {
        'criteria_text': elig.get('eligibilityCriteria', '').lower(),
        'sex': elig.get('sex', 'ALL'),
        'minimum_age': elig.get('minimumAge', ''),
        'std_ages': elig.get('stdAges', []),
        'healthy_volunteers': elig.get('healthyVolunteers', False),
    }

def extract_conditions(trial):
    """Extract conditions from trial."""
    cond_module = trial.get('protocolSection', {}).get('conditionsModule', {})
    conditions = cond_module.get('conditions', [])
    keywords = cond_module.get('keywords', [])
    return [c.lower() for c in conditions] + [k.lower() for k in keywords]

def condition_match(patient_condition, trial_conditions):
    """Check if patient condition matches trial conditions."""
    synonyms = CONDITION_SYNONYMS.get(patient_condition.lower(), [patient_condition.lower()])
    trial_cond_lower = [c.lower() for c in trial_conditions]
    
    for syn in synonyms:
        for tc in trial_cond_lower:
            if syn in tc or tc in syn:
                return True
    return False

def age_match(patient_age, min_age_str, std_ages):
    """Check if patient age fits trial age range."""
    min_age, max_age = parse_age_range(min_age_str, std_ages)
    return min_age <= patient_age <= max_age

def sex_match(patient_sex, trial_sex):
    """Check if patient sex matches trial sex requirement."""
    if trial_sex == 'ALL':
        return True
    return patient_sex == trial_sex

def location_match(patient_country, trial_countries):
    """Check if trial has recruiting site in patient's country."""
    return patient_country in trial_countries

def exclusion_check(patient, criteria_text):
    """Check exclusion keywords against patient profile."""
    criteria_lower = criteria_text.lower()
    patient_text = ' '.join([
        patient['condition'].lower(),
        ' '.join(patient['biomarkers']).lower(),
        ' '.join(patient['history']).lower()
    ]).lower()
    
    for kw in EXCLUSION_KEYWORDS:
        if kw in criteria_lower:
            if kw not in patient_text:
                return False  # Excluded
    return True  # Not excluded

def fetch_trials_for_condition(condition, max_trials=200):
    """Fetch recruiting trials for a condition."""
    search_terms = CONDITION_SYNONYMS.get(condition, [condition])
    query = ' OR '.join(search_terms[:3])
    
    url = f"https://clinicaltrials.gov/api/v2/studies?query.cond={urllib.parse.quote(query)}&filter.overallStatus=RECRUITING&pageSize=100&format=json"
    
    all_trials = []
    next_page_token = None
    
    while len(all_trials) < max_trials:
        page_url = url
        if next_page_token:
            page_url += f"&pageToken={urllib.parse.quote(next_page_token)}"
        
        data = fetch_json(page_url)
        if not data or 'studies' not in data:
            break
        
        all_trials.extend(data['studies'])
        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break
        time.sleep(1)
    
    return all_trials[:max_trials]

def fetch_random_trials(max_trials=100):
    """Fetch random recruiting trials."""
    url = f"https://clinicaltrials.gov/api/v2/studies?filter.overallStatus=RECRUITING&pageSize=100&format=json"
    
    all_trials = []
    next_page_token = None
    
    while len(all_trials) < max_trials:
        page_url = url
        if next_page_token:
            page_url += f"&pageToken={urllib.parse.quote(next_page_token)}"
        
        data = fetch_json(page_url)
        if not data or 'studies' not in data:
            break
        
        all_trials.extend(data['studies'])
        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break
        time.sleep(1)
    
    return all_trials[:max_trials]

def has_complete_eligibility(trial):
    """Check if trial has complete structured eligibility data."""
    elig = trial.get('protocolSection', {}).get('eligibilityModule', {})
    return bool(elig.get('eligibilityCriteria') and elig.get('minimumAge') and elig.get('sex'))

def apply_filter(patient, trial, filter_name):
    """Apply a single filter, return (pass, reason)."""
    elig = extract_eligibility(trial)
    trial_conditions = extract_conditions(trial)
    
    if filter_name == 'condition':
        return condition_match(patient['condition'], trial_conditions), 'condition'
    elif filter_name == 'age':
        return age_match(patient['age'], elig['minimum_age'], elig['std_ages']), 'age'
    elif filter_name == 'sex':
        return sex_match(patient['sex'], elig['sex']), 'sex'
    elif filter_name == 'location':
        trial_countries = extract_locations(trial)
        if not trial_countries:
            return True, 'no_location_data'  # Can't verify, assume pass
        return location_match(patient['country'], trial_countries), 'location'
    elif filter_name == 'exclusion':
        return exclusion_check(patient, elig['criteria_text']), 'exclusion'
    return True, 'unknown'

def main():
    print("E187: Clinical Trial Eligibility Matching - Filtering Funnel")
    print("=" * 60)
    
    # Sample trials for each condition
    conditions = list(CONDITION_SYNONYMS.keys())[:20]
    condition_trials = {}
    
    print("\nFetching condition-matched trials...")
    for cond in conditions:
        print(f"  {cond}...")
        trials = fetch_trials_for_condition(cond, max_trials=20)
        condition_trials[cond] = trials
        print(f"    Fetched {len(trials)} trials")
        time.sleep(1)
    
    # Fetch random trials
    print("\nFetching random trials...")
    random_trials = fetch_random_trials(max_trials=100)
    print(f"  Fetched {len(random_trials)} random trials")
    
    # Filter trials with complete eligibility data
    for cond in condition_trials:
        condition_trials[cond] = [t for t in condition_trials[cond] if has_complete_eligibility(t)]
    
    random_trials = [t for t in random_trials if has_complete_eligibility(t)]
    
    total_condition_trials = sum(len(v) for v in condition_trials.values())
    print(f"\nTrials with complete eligibility: {total_condition_trials} condition-matched, {len(random_trials)} random")
    
    # G1: Sample adequacy
    g1_pass = total_condition_trials >= 30
    print(f"\nG1 (sample adequacy ≥30): {total_condition_trials} -> {'PASS' if g1_pass else 'FAIL'}")
    
    # Measure filtering funnel for each patient
    filters = ['condition', 'age', 'sex', 'location', 'exclusion']
    filter_labels = ['Condition', 'Age', 'Sex', 'Location', 'Exclusion']
    
    funnel_results = []
    
    for patient in PATIENT_PROFILES:
        cond = patient['condition']
        trials_to_check = condition_trials.get(cond, [])
        
        if not trials_to_check:
            funnel_results.append({
                'patient': patient['id'],
                'condition': cond,
                'initial_trials': 0,
                'surviving': [0, 0, 0, 0, 0],
                'final_matches': 0
            })
            continue
        
        surviving = []
        current_trials = trials_to_check
        
        for fname, flabel in zip(filters, filter_labels):
            passed = []
            for trial in current_trials:
                passes, reason = apply_filter(patient, trial, fname)
                if passes:
                    passed.append(trial)
            surviving.append(len(passed))
            current_trials = passed
        
        funnel_results.append({
            'patient': patient['id'],
            'condition': cond,
            'initial_trials': len(trials_to_check),
            'surviving': surviving,
            'final_matches': len(current_trials)
        })
    
    # Aggregate funnel statistics
    print("\n" + "=" * 60)
    print("FILTERING FUNNEL (median across 100 patients)")
    print("=" * 60)
    
    for i, flabel in enumerate(filter_labels):
        counts = [r['surviving'][i] for r in funnel_results if r['initial_trials'] > 0]
        if counts:
            median = statistics.median(counts)
            mean = statistics.mean(counts)
            print(f"  After {flabel}: median={median:.1f}, mean={mean:.1f}")
    
    # Final matches statistics
    final_counts = [r['final_matches'] for r in funnel_results]
    patients_with_matches = sum(1 for c in final_counts if c > 0)
    median_final = statistics.median(final_counts) if final_counts else 0
    mean_final = statistics.mean(final_counts) if final_counts else 0
    
    print(f"\nFinal matches: median={median_final:.1f}, mean={mean_final:.1f}")
    print(f"Patients with ≥1 match: {patients_with_matches}/100")
    
    # Per-condition breakdown
    print("\n" + "=" * 60)
    print("PER-CONDITION FINAL MATCHES (median)")
    print("=" * 60)
    
    by_condition = defaultdict(list)
    for r in funnel_results:
        by_condition[r['condition']].append(r['final_matches'])
    
    for cond in conditions:
        counts = by_condition[cond]
        if counts:
            median = statistics.median(counts)
            print(f"  {cond}: median={median:.1f} (n={len(counts)})")
    
    # Gates
    # G2: ≥80 patients have ≥1 match after ALL filters
    g2_pass = patients_with_matches >= 80
    print(f"\nG2 (patients with matches ≥80): {patients_with_matches}/100 -> {'PASS' if g2_pass else 'FAIL'}")
    
    # G3: Median final matches ≥1 (at least one trial per typical patient)
    g3_pass = median_final >= 1
    print(f"G3 (median final matches ≥1): {median_final:.1f} -> {'PASS' if g3_pass else 'FAIL'}")
    
    # G4: Mean final matches ≥3 (enough choices for a useful tool)
    g4_pass = mean_final >= 3
    print(f"G4 (mean final matches ≥3): {mean_final:.1f} -> {'PASS' if g4_pass else 'FAIL'}")
    
    # G5: Condition-only baseline - condition filter alone should leave many,
    # structured filters should reduce but not eliminate
    condition_only_counts = [r['surviving'][0] for r in funnel_results if r['initial_trials'] > 0]
    median_condition = statistics.median(condition_only_counts) if condition_only_counts else 0
    
    # Structured matching should retain at least 10% of condition-matched trials
    g5_pass = median_final >= 0.1 * median_condition if median_condition > 0 else False
    print(f"G5 (retention ≥10% of condition-matched): {median_final:.1f} / {median_condition:.1f} = {median_final/median_condition*100:.1f}% -> {'PASS' if g5_pass else 'FAIL'}")
    
    gates = {'G1': g1_pass, 'G2': g2_pass, 'G3': g3_pass, 'G4': g4_pass, 'G5': g5_pass}
    overall = all(gates.values())
    
    print(f"\nOVERALL: {'ALL GATES PASS' if overall else 'KILL GATE FIRED'}")
    
    # Save results
    exp_dir = os.path.dirname(os.path.abspath(__file__))
    
    output = {
        'experiment': 'E187',
        'timestamp': datetime.now().isoformat(),
        'conditions_tested': len(conditions),
        'total_condition_trials': total_condition_trials,
        'total_random_trials': len(random_trials),
        'patient_profiles': len(PATIENT_PROFILES),
        'gates': gates,
        'funnel_medians': {flabel: statistics.median([r['surviving'][i] for r in funnel_results if r['initial_trials'] > 0]) 
                           for i, flabel in enumerate(filter_labels)},
        'funnel_means': {flabel: statistics.mean([r['surviving'][i] for r in funnel_results if r['initial_trials'] > 0]) 
                         for i, flabel in enumerate(filter_labels)},
        'final_matches_median': median_final,
        'final_matches_mean': mean_final,
        'patients_with_matches': patients_with_matches,
        'median_condition_matches': median_condition,
        'retention_rate': median_final / median_condition if median_condition > 0 else 0,
        'per_patient': funnel_results,
        'overall_pass': overall
    }
    
    with open(os.path.join(exp_dir, 'results.json'), 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\nResults saved to results.json")
    return 0 if overall else 1

if __name__ == '__main__':
    sys.exit(main())