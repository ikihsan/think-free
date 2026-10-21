#!/usr/bin/env python3
"""E206 Keyword sets for award categorization."""

# Award fields (same as E203/E204/E205)
AWARD_FIELDS = [
    "Award ID", "Award Amount", "Description", "Recipient Name",
    "PSC Code", "NAICS Code", "Agency Name", "Funding Agency Name",
    "Start Date", "End Date", "Award Type", "Type of Contract Pricing",
]

# Categorization keyword sets (same as E203/E204/E205)
SOFTWARE_KEYWORDS = [
    "software", "saas", "license", "licence", "subscription", "cloud",
    "platform", "application", "app", "system", "solution", "service now",
    "servicenow", "salesforce", "microsoft", "oracle", "sap", "adobe",
    "red hat", "linux", "windows", "vmware", "docker", "kubernetes",
    "aws", "azure", "gcp", "google cloud", "amazon web",
    "development", "programming", "coding", "api", "sdk", "framework",
    "database", "analytics", "reporting", "dashboard", "portal",
    "cybersecurity", "security", "encryption", "firewall", "antivirus",
    "backup", "recovery", "monitoring", "logging", "devops", "ci/cd",
    "github", "gitlab", "jira", "confluence", "atlassian", "slack",
    "teams", "zoom", "webex", "office 365", "o365", "google workspace",
    "erp", "crm", "hris", "hrms", "payroll", "finance", "accounting",
    "machine learning", "ml", "ai", "artificial intelligence", "data science",
    "etl", "pipeline", "warehouse", "bi", "business intelligence",
]

SERVICE_KEYWORDS = [
    "service", "support", "maintenance", "help desk", "helpdesk",
    "consulting", "advisory", "implementation", "integration",
    "migration", "deployment", "configuration", "customization",
    "training", "education", "certification", "managed services",
    "outsourcing", "staffing", "augmentation", "contractor",
    "professional services", "technical services", "it services",
    "cloud services", "hosting", "colocation", "data center",
    "network services", "telecom", "telecommunications", "voice",
    "video", "conferencing", "unified communications",
    "security services", "audit", "assessment", "penetration test",
    "vulnerability", "compliance", "governance", "risk",
    "project management", "pm", "scrum", "agile", "waterfall",
    "business analysis", "requirements", "testing", "qa", "quality",
]

HARDWARE_KEYWORDS = [
    "hardware", "server", "laptop", "desktop", "workstation",
    "router", "switch", "firewall appliance", "storage", "disk",
    "tape", "backup device", "ups", "power", "rack", "cabinet",
    "cable", "connector", "fiber", "copper", "patch panel",
    "monitor", "display", "projector", "printer", "scanner",
    "peripheral", "keyboard", "mouse", "docking station",
    "mobile", "tablet", "phone", "smartphone", "iphone", "android",
    "equipment", "device", "appliance", "blade", "chassis",
    "memory", "ram", "cpu", "processor", "gpu", "graphics card",
    "hard drive", "ssd", "nvme", "sata", "raid", "san", "nas",
]

TELECOM_KEYWORDS = [
    "telecom", "telecommunications", "bandwidth", "internet",
    "circuit", "line", "trunk", "sip", "voip", "pbx", "pstn",
    "wireless", "cellular", "5g", "4g", "lte", "satellite",
    "transmission", "fiber optic", "dark fiber", "wavelength",
    "carrier", "isp", "provider", "connectivity", "network",
    "leased line", "mpls", "vpn", "sd-wan",
]

# Screen score baselines from E199/E200
BASELINE_DATA = {
    "7030": {"screen_score": 2412.0, "top10_share": 0.384, "recipients": 3917},
    "DA01": {"screen_score": 2363.0, "top10_share": 0.345, "recipients": 3625},
    "DA10": {"screen_score": 2345.0, "top10_share": 0.358, "recipients": 3649},
    "7A21": {"screen_score": 2034.0, "top10_share": 0.489, "recipients": 3950},
    "D304": {"screen_score": 490.0, "top10_share": 0.576, "recipients": 1156},
}


def categorize_description(description):
    """Categorize as software, service, hardware, telecom, or other."""
    if not description:
        return "unknown"
    desc_lower = description.lower()

    software_score = sum(1 for kw in SOFTWARE_KEYWORDS if kw in desc_lower)
    service_score = sum(1 for kw in SERVICE_KEYWORDS if kw in desc_lower)
    hardware_score = sum(1 for kw in HARDWARE_KEYWORDS if kw in desc_lower)
    telecom_score = sum(1 for kw in TELECOM_KEYWORDS if kw in desc_lower)

    scores = {
        "software": software_score,
        "service": service_score,
        "hardware": hardware_score,
        "telecom": telecom_score,
    }
    max_cat = max(scores, key=scores.get)
    if scores[max_cat] == 0:
        return "other"
    return max_cat


def is_software(description):
    return categorize_description(description) == "software"