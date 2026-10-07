#!/usr/bin/env python3
"""
Rule-based claim extractor for directional contradictions in paper abstracts.
Stdlib only: re, json, csv, pathlib, urllib, argparse, sys, collections.
"""

import re
import json
import argparse
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set, Optional

# Relationship verb patterns - using word boundaries carefully
INCREASE_VERBS = [
    r"increases?", r"raises?", r"elevates?", r"enhances?", r"improves?",
    r"augments?", r"boosts?", r"upregulates?", r"promotes?",
    r"heightens?", r"intensifies?", r"amplifies?", r"strengthens?",
    r"is associated with higher", r"is linked to higher", r"correlates with higher",
    r"leads to higher", r"results in higher", r"causes higher",
    r"greater", r"larger", r"more", r"higher", r"elevated"
]

DECREASE_VERBS = [
    r"decreases?", r"reduces?", r"lowers?", r"diminishes?", r"impairs?",
    r"worsens?", r"attenuates?", r"downregulates?", r"inhibits?",
    r"suppresses?", r"weakens?", r"lessens?", r"alleviates?",
    r"is associated with lower", r"is linked to lower", r"correlates with lower",
    r"leads to lower", r"results in lower", r"causes lower",
    r"smaller", r"lower", r"less", r"fewer", r"reduced"
]

NO_EFFECT_VERBS = [
    r"has no effect on", r"has no significant effect on", r"does not affect",
    r"does not significantly affect", r"does not change", r"does not alter",
    r"no significant difference", r"no difference", r"unchanged",
    r"not associated with", r"not linked to", r"not correlated with",
    r"does not increase", r"does not decrease", r"does not improve", r"does not reduce",
    r"no impact on", r"no influence on"
]

HEDGE_VERBS = [
    r"may increase", r"might increase", r"could increase", r"suggests.*increase",
    r"may decrease", r"might decrease", r"could decrease", r"suggests.*decrease",
    r"may have no effect", r"might have no effect", r"could have no effect",
    r"potentially increases?", r"potentially decreases?", r"potentially has no effect",
    r"hint at.*increase", r"hint at.*decrease", r"hint at.*no effect"
]

# Compile patterns - use simple search without \b for multi-word phrases
def compile_patterns(verbs):
    patterns = []
    for v in verbs:
        if " " in v:  # multi-word phrase
            patterns.append(re.compile(v, re.IGNORECASE))
        else:
            patterns.append(re.compile(rf"\b{v}\b", re.IGNORECASE))
    return patterns

INCREASE_PATTERNS = compile_patterns(INCREASE_VERBS)
DECREASE_PATTERNS = compile_patterns(DECREASE_VERBS)
NO_EFFECT_PATTERNS = compile_patterns(NO_EFFECT_VERBS)
HEDGE_PATTERNS = compile_patterns(HEDGE_VERBS)

# Negation patterns
NEGATION_PATTERNS = [
    re.compile(r"\bnot\b", re.IGNORECASE),
    re.compile(r"\bno\b", re.IGNORECASE),
    re.compile(r"\bnever\b", re.IGNORECASE),
    re.compile(r"\bwithout\b", re.IGNORECASE),
    re.compile(r"\babsent\b", re.IGNORECASE),
]

# Hedge/uncertainty words
HEDGE_WORDS = {"may", "might", "could", "suggest", "potentially", "possibly", "likely", "probable", "hint", "indicate"}

# Stopwords for noun phrase extraction
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "as", "is", "was", "were", "are", "been", "be", "have", "has", "had",
    "do", "does", "did", "will", "would", "should", "could", "may", "might", "must",
    "this", "that", "these", "those", "it", "its", "their", "our", "your", "his", "her",
    "in", "out", "up", "down", "over", "under", "between", "among", "through", "during",
    "before", "after", "since", "until", "while", "when", "where", "which", "who", "whom",
    "whose", "what", "why", "how", "all", "any", "some", "such", "only", "own", "same",
    "so", "than", "too", "very", "just", "now", "then", "also", "well", "even", "still",
    # Common adverbs that modify verbs but aren't part of subject/object
    "significantly", "significant", "substantially", "markedly", "dramatically",
    "considerably", "greatly", "largely", "mainly", "primarily", "mostly",
    "partially", "partly", "slightly", "marginally", "minimally", "modestly",
    "statistically", "clinically", "notably", "remarkably", "clearly", "evidently"
}

# Verb-phrase words that should be skipped when extracting noun phrases
# These are words that appear in multi-word relationship patterns
# (Now handled by using match span boundaries instead)
# VERB_PHRASE_WORDS = {...}

# Sentence splitter
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def split_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    text = re.sub(r"\s+", " ", text.strip())
    return SENTENCE_SPLIT.split(text)


def find_verb_token_indices(sentence: str, match: re.Match) -> Tuple[int, int]:
    """
    Find the token index range of the matched verb phrase.
    Returns (start_token_idx, end_token_idx) where end is exclusive.
    Subject should be extracted from start_token_idx - 1 backward.
    Object should be extracted from end_token_idx forward.
    """
    # Get text up to match start
    prefix = sentence[:match.start()]
    prefix_tokens = prefix.split()
    start_token_idx = len(prefix_tokens)
    
    # Get the matched text tokens
    matched_text = match.group(0)
    matched_tokens = matched_text.split()
    end_token_idx = start_token_idx + len(matched_tokens)
    
    return start_token_idx, end_token_idx


def extract_noun_phrase(tokens: List[str], start_idx: int, direction: int) -> str:
    """
    Extract noun phrase from tokens starting at start_idx going in direction.
    direction = -1 for subject (backward), +1 for object (forward).
    Skips leading stopwords, then collects content words until hitting a stopword.
    """
    phrase_tokens = []
    idx = start_idx
    
    # Skip leading stopwords/verb-phrase words
    while 0 <= idx < len(tokens):
        token = tokens[idx].strip(".,;:()[]{}\"'")
        token_lower = token.lower()
        if not token or token_lower in STOPWORDS or token in ".,;:()[]{}\"'":
            idx += direction
            continue
        break
    
    # Now collect content words
    while 0 <= idx < len(tokens):
        token = tokens[idx].strip(".,;:()[]{}\"'")
        token_lower = token.lower()
        
        # Stop at stopwords, punctuation, or empty
        if not token or token_lower in STOPWORDS or token in ".,;:()[]{}\"'":
            break
        
        if direction == -1:
            phrase_tokens.insert(0, token)
        else:
            phrase_tokens.append(token)
        
        idx += direction
    
    return " ".join(phrase_tokens)


def extract_claims_from_sentence(sentence: str) -> List[Dict]:
    """Extract (subject, relationship, object) triples from a sentence."""
    claims = []
    tokens = sentence.split()
    
    # Try each pattern category
    all_patterns = [
        (INCREASE_PATTERNS, "INCREASE"),
        (DECREASE_PATTERNS, "DECREASE"),
        (NO_EFFECT_PATTERNS, "NO_EFFECT"),
        (HEDGE_PATTERNS, "HEDGED")
    ]
    
    for patterns, rel_type in all_patterns:
        for pattern in patterns:
            for match in pattern.finditer(sentence):
                verb_start_idx, verb_end_idx = find_verb_token_indices(sentence, match)
                
                # Extract subject (before verb phrase) and object (after verb phrase)
                verb_start_idx, verb_end_idx = find_verb_token_indices(sentence, match)
                subject = extract_noun_phrase(tokens, verb_start_idx - 1, -1)
                obj = extract_noun_phrase(tokens, verb_end_idx, +1)
                
                if subject and obj:
                    rel, conf = classify_relationship(sentence, match)
                    claims.append({
                        "subject": subject.lower(),
                        "relationship": rel,
                        "object": obj.lower(),
                        "confidence": conf,
                        "sentence": sentence[:200]
                    })
    
    return claims


def classify_relationship(sentence: str, verb_match: re.Match) -> Tuple[str, float]:
    """
    Classify the relationship type and confidence.
    Returns (relationship_type, confidence)
    """
    matched_text = verb_match.group(0).lower()
    verb_start = verb_match.start()
    verb_end = verb_match.end()
    
    # Check for negation in context
    context_before = sentence[max(0, verb_start - 50):verb_start].lower()
    context_after = sentence[verb_end:verb_end + 50].lower()
    has_negation = any(neg.search(context_before) or neg.search(context_after) for neg in NEGATION_PATTERNS)
    
    # Check for hedge words in context AND in matched text
    context = context_before + " " + context_after
    hedge_count = sum(1 for hw in HEDGE_WORDS if hw in context)
    # Also check matched text for hedge words (e.g., "may decrease")
    matched_lower = matched_text.lower()
    hedge_in_match = any(hw in matched_lower for hw in HEDGE_WORDS)
    has_hedge = hedge_count > 0 or hedge_in_match
    
    # Determine base relationship from matched text
    if any(p.search(matched_text) for p in INCREASE_PATTERNS):
        base_rel = "INCREASE"
    elif any(p.search(matched_text) for p in DECREASE_PATTERNS):
        base_rel = "DECREASE"
    elif any(p.search(matched_text) for p in NO_EFFECT_PATTERNS):
        base_rel = "NO_EFFECT"
    elif any(p.search(matched_text) for p in HEDGE_PATTERNS):
        base_rel = "HEDGED"
    else:
        return "UNKNOWN", 0.0
    
    # Apply modifiers
    confidence = 1.0
    if has_negation:
        if base_rel == "INCREASE":
            base_rel = "DECREASE"
        elif base_rel == "DECREASE":
            base_rel = "INCREASE"
        confidence *= 0.7
    if has_hedge:
        base_rel = "MAY_" + base_rel if base_rel != "HEDGED" else "HEDGED"
        confidence *= 0.5
    
    return base_rel, confidence


def normalize_entity(entity: str) -> str:
    """Normalize entity names for matching."""
    entity = re.sub(r"^(the|a|an)\s+", "", entity)
    # Strip common measurement suffixes that don't change the core concept
    entity = re.sub(r"\s+(levels?|scores?|outcomes?|symptoms?|function|quality)$", "", entity)
    return entity.strip().lower()


def extract_claims(abstract: str) -> List[Dict]:
    """Extract all claims from an abstract."""
    sentences = split_sentences(abstract)
    all_claims = []
    
    for sent in sentences:
        claims = extract_claims_from_sentence(sent)
        all_claims.extend(claims)
    
    # Normalize entities
    for claim in all_claims:
        claim["subject"] = normalize_entity(claim["subject"])
        claim["object"] = normalize_entity(claim["object"])
    
    # Deduplicate similar claims
    seen = set()
    unique_claims = []
    for claim in all_claims:
        key = (claim["subject"], claim["relationship"], claim["object"])
        if key not in seen:
            seen.add(key)
            unique_claims.append(claim)
    
    return unique_claims


def detect_contradictions(claims_by_abstract: Dict[str, List[Dict]]) -> List[Dict]:
    """Detect contradictions across abstracts for the same variable pair."""
    pair_claims = defaultdict(list)
    for abstract_id, claims in claims_by_abstract.items():
        for claim in claims:
            key = (claim["subject"], claim["object"])
            pair_claims[key].append({**claim, "abstract_id": abstract_id})
    
    contradictions = []
    for (subject, obj), claims in pair_claims.items():
        if len(claims) < 2:
            continue
        
        relationships = set(c["relationship"] for c in claims)
        
        has_increase = any(r.startswith("INCREASE") or r.startswith("MAY_INCREASE") for r in relationships)
        has_decrease = any(r.startswith("DECREASE") or r.startswith("MAY_DECREASE") for r in relationships)
        has_no_effect = any(r == "NO_EFFECT" or r.startswith("MAY_NO_EFFECT") for r in relationships)
        
        contradiction_type = None
        if has_increase and has_decrease:
            contradiction_type = "INCREASE_vs_DECREASE"
        elif has_increase and has_no_effect:
            contradiction_type = "INCREASE_vs_NO_EFFECT"
        elif has_decrease and has_no_effect:
            contradiction_type = "DECREASE_vs_NO_EFFECT"
        
        if contradiction_type:
            conflicting = [c for c in claims if c["relationship"] in relationships]
            contradictions.append({
                "subject": subject,
                "object": obj,
                "contradiction_type": contradiction_type,
                "relationships": list(relationships),
                "claims": conflicting,
                "abstract_ids": [c["abstract_id"] for c in conflicting]
            })
    
    return contradictions


def load_abstracts(input_file: str) -> Dict[str, str]:
    """Load abstracts from JSONL file."""
    abstracts = {}
    with open(input_file, "r") as f:
        for line in f:
            data = json.loads(line)
            abstracts[data["id"]] = data["abstract"]
    return abstracts


def main():
    parser = argparse.ArgumentParser(description="Extract directional claims and detect contradictions")
    parser.add_argument("--input", required=True, help="Input JSONL file with abstracts")
    parser.add_argument("--output", required=True, help="Output JSONL file with contradictions")
    args = parser.parse_args()
    
    abstracts = load_abstracts(args.input)
    
    claims_by_abstract = {}
    for abs_id, abstract in abstracts.items():
        claims_by_abstract[abs_id] = extract_claims(abstract)
    
    contradictions = detect_contradictions(claims_by_abstract)
    
    with open(args.output, "w") as f:
        for contra in contradictions:
            f.write(json.dumps(contra) + "\n")
    
    print(f"Processed {len(abstracts)} abstracts")
    print(f"Extracted claims from {len(claims_by_abstract)} abstracts")
    print(f"Found {len(contradictions)} contradictions")


if __name__ == "__main__":
    main()