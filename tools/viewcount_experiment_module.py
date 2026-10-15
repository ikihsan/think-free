            "user_date": __import__('time').strftime("%Y-%m-%d", __import__('time').gmtime()),
            "platform": self.platform,
            "keyword": self.keyword,
            "sample_size": 0,
            "classified": {"need-related": 0, "random": 0},
            "active": {"need-related": 0, "random": 0},
            "active_rates": {"need-related": 0, "random": 0},
            "g1_pass": False,
            "g2_pass": False,
            "g3_pass": False,
            "g4_pass": False,
            "conclusion": reason,
            "experiment_description": f"View-count principle on {self.platform} for keyword: {self.keyword}",
            "note": f"Experiment aborted: {reason}",
        }
    
    def _determine_conclusion(self, gates: Dict[str, Any]) -> str:
        """Determine the experiment conclusion from gate results."""
        if gates["g1_pass"] and gates["g2_pass"] and gates["g3_pass"] and gates["g4_pass"]:
            return "gates_all_pass"
        elif not gates["g1_pass"] and not gates["g2_pass"]:
            return "g1_and_g2_fail"
        elif not gates["g1_pass"]:
            return "g1_fail"
        elif not gates["g2_pass"]:
            return "g2_fail"
        else:
            return "partial"


# ---------------------------------------------------------------------------
# Framework entry point
# ---------------------------------------------------------------------------

def list_need_indicators() -> List[str]:
    """Return the sorted list of need-indicator terms."""
    return sorted(NEED_INDICATORS)


def list_generic_terms() -> List[str]:
    """Return the sorted list of generic terms."""
    return sorted(GENERIC_TERMS)


def run_classification_demo(texts: List[str]) -> None:
    """Run a quick classification demo on a list of texts."""
    print("=== Classification Demo ===")
    for i, text in enumerate(texts):
        cls = classify_text(text)
        print(f"  {i+1}. [{cls}] {text[:80]}")


if __name__ == "__main__":
    # Quick demo
    demo_texts = [
        "A Python database connection pool with caching and monitoring",
        "A utility library for common operations",
        "A security authentication framework with OAuth2 support",
        "A tool for debugging web application issues",
    ]
    run_classification_demo(demo_texts)
    
    print("\n=== Need Indicators ===")
    for term in sorted(NEED_INDICATORS)[:10]:
        print(f"  - {term}")
    
    print("\n=== Generic Terms ===")
    for term in sorted(GENERIC_TERMS)[:10]:
        print(f"  - {term}")