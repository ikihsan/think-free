#!/usr/bin/env python3
"""
E119 — classifier patterns (split from classifier_v3.py for line cap compliance).

Declared anchored word-boundary patterns for need-related and excluded classification.
Patterns are DECLARED BEFORE MEASUREMENT and not tuned post-hoc.
"""

# Need-related indicators: question forms and problem statements
# Anchored word-boundary patterns (\b delimiters) to reduce false positives
NEED_PATTERNS = [
    # Core question forms (what/how/why/when/where/which/who + verb)
    r'\bhow\s+do\b', r'\bhow\s+can\b', r'\bhow\s+to\b',
    r'\bhow\s+does\b', r'\bhow\s+is\b', r'\bhow\s+are\b', r'\bhow\s+would\b',
    r'\bhow\s+will\b', r'\bhow\s+could\b', r'\bhow\s+fast\b', r'\bhow\s+much\b',
    r'\bhow\s+many\b', r'\bhow\s+long\b', r'\bhow\s+often\b', r'\bhow\s+did\b',
    
    r'\bwhy\s+does\b', r'\bwhy\s+is\b', r'\bwhy\s+are\b', r'\bwhy\s+would\b',
    r'\bwhy\s+do\b', r'\bwhy\s+did\b', r'\bwhy\s+don\'t\b', r'\bwhy\s+doesn\'t\b',
    r'\bwhy\s+won\'t\b', r'\bwhy\s+can\b',
    
    r'\bwhat\s+is\b', r'\bwhat\s+are\b', r'\bwhat\s+does\b', r'\bwhat\s+do\b',
    r'\bwhat\s+would\b', r'\bwhat\s+happens\b', r'\bwhat\s+make\b',
    r'\bwhat\'s\s+the\b', r'\bwhat\s+is\s+the\b', r'\bwhat\s+causes\b', r'\bwhat\s+caused\b',
    
    r'\bwhen\s+does\b', r'\bwhen\s+is\b', r'\bwhen\s+would\b', r'\bwhen\s+do\b',
    r'\bwhere\s+is\b', r'\bwhere\s+are\b', r'\bwhere\s+does\b', r'\bwhere\s+do\b',
    r'\bwhere\s+would\b',
    
    r'\bwhich\s+is\b', r'\bwhich\s+are\b', r'\bwhich\s+does\b', r'\bwhich\s+do\b',
    r'\bwho\s+is\b', r'\bwho\s+are\b',
    
    # Modal question forms (can/could/would/will + pronoun)
    r'\bcan\s+you\b', r'\bcan\s+anyone\b', r'\bcan\s+someone\b', r'\bcan\s+i\b', r'\bcan\s+we\b',
    r'\bcould\s+you\b', r'\bcould\s+anyone\b', r'\bcould\s+someone\b', r'\bcould\s+i\b',
    r'\bwould\s+you\b', r'\bwould\s+anyone\b', r'\bwould\s+someone\b',
    r'\bwill\s+you\b', r'\bwill\s+this\b', r'\bwill\s+it\b', r'\bwill\s+a\b', r'\bwill\s+the\b',
    
    # Existence/possibility questions
    r'\bis\s+there\b', r'\bare\s+there\b', r'\bdoes\s+anyone\b', r'\bdo\s+you\b',
    r'\bdoes\s+it\b', r'\bdoes\s+the\b', r'\bdoes\s+a\b',
    r'\bis\s+it\b', r'\bare\s+they\b', r'\bis\s+\w+\b',  # "Is X Y?" pattern
    r'\bdo\s+we\b', r'\bdo\s+they\b',
    
    # Negation questions (often indicate problems)
    r'\bdon\'t\b', r'\bdoesn\'t\b', r'\bwon\'t\b', r'\bcan\'t\b', r'\bcannot\b',
    
    # Direct help/request patterns
    r'\bhelp\s+me\b', r'\bplease\s+help\b', r'\bneed\s+help\b',
    r'\bexplain\b', r'\bclarify\b', r'\bunderstand\b',
    
    # Comparison/choice questions
    r'\bdifference\s+between\b', r'\bvs\.?\b',
    
    # Recommendation/guidance requests
    r'\brecommend\b', r'\bsuggest\b', r'\badvice\b', r'\bguidance\b',
    # Note: "tutorial", "guide", "learn" removed - too ambiguous (appear in both
    # genuine questions and generic descriptions like "tutorial material")
    
    # Personal problem forms
    r'\bhow\s+do\s+i\b', r'\bhow\s+can\s+i\b',
    r'\bmy\s+\w+\s+(not|doesn\'t|won\'t|can\'t|error|fail|issue|problem)',
    
    # Technical problem keywords
    r'\bfix\b', r'\bdebug\b', r'\brefactor\b', r'\boptimize\b', r'\bresolve\b',
    r'\bhelp\b', r'\berror\b', r'\bnot working\b', r'\bcannot\b', r'\bissue\b',
    r'\bproblem\b', r'\bbug\b', r'\bfail\b', r'\bcrash\b', r'\bexception\b',
    
    # Additional modal forms for hypothetical/speculative questions
    r'\bwould\s+it\b', r'\bwould\s+a\b', r'\bwould\s+the\b',
    r'\bcould\s+it\b', r'\bcould\s+a\b', r'\bcould\s+the\b',
    r'\bdoes\s+it\b', r'\bdoes\s+the\b', r'\bdoes\s+a\b',
    r'\bdo\s+it\b', r'\bdo\s+the\b',
    r'\bis\s+it\b', r'\bis\s+a\b', r'\bis\s+the\b',
    r'\bdid\s+it\b', r'\bdid\s+the\b', r'\bdid\s+a\b',
    r'\bwill\s+it\b', r'\bwill\s+the\b', r'\bwill\s+a\b',
    
    # Modal + noun phrase (for hypothetical questions like "Would time freeze...")
    r'\bwould\s+\w+\s+(freeze|work|break|fail|change|stop|start|continue|end|begin)\b',
    r'\bcould\s+\w+\s+(kill|break|damage|destroy|work|function|operate|run|execute)\b',
    r'\bdoes\s+\w+\s+(change|work|flow|move|travel|propagate|reflect|refract|absorb)\b',
    r'\bdo\s+\w+\s+(change|work|flow|move|travel|propagate|reflect|refract|absorb)\b',
    
    # "would you/could you" already covered above
    # "would X" where X is a noun - more general pattern
    r'\bwould\s+\w{3,}\s+\w+\b',
    r'\bcould\s+\w{3,}\s+\w+\b',
    
    # Recommendation/guidance (adjective forms)
    r'\brecommended\b', r'\brecommends\b',
    
    # Derivation/explanation requests
    r'\bderivation\b', r'\bderive\b', r'\bexplain\b',
    
    # Technical question starters
    r'\bphase\s+shift\b', r'\bmaximum\s+theoretical\b',
    r'\brelationship\s+between\b', r'\bwhat\s+equation\b',
    r'\bwhat\s+formula\b',
    
    # Book/resource requests
    r'\bbooks?\s+for\b', r'\bbook\s+on\b', r'\bresource\s+for\b',
    r'\breference\s+for\b', r'\btextbook\b',
    
    # Mathematical/technical imperative problem statements
    # These capture "Determine X", "Calculate Y", "Find Z", etc.
    r'\bdetermine\b', r'\bcalculate\b', r'\bcompute\b', r'\bfind\b',
    r'\bevaluate\b', r'\bprove\b', r'\bshow\s+that\b', r'\bderive\b',
    r'\bverify\b', r'\bcheck\b', r'\btest\b',
    
    # "Where to" guidance questions
    r'\bwhere\s+to\b',
    
    # "What is/are the" noun phrase questions (more specific than generic "what is")
    r'\bwhat\s+is\s+the\b', r'\bwhat\s+are\s+the\b',
    
    # "How to" already covered, but add "how do i/we" variants
    r'\bhow\s+do\s+i\b', r'\bhow\s+do\s+we\b', r'\bhow\s+can\s+i\b', r'\bhow\s+can\s+we\b',
    
    # Mathematical noun-phrase question forms: "X of Y", "X between Y and Z"
    r'\bintegral\s+of\b', r'\bderivative\s+of\b', r'\bprobability\s+of\b',
    r'\bproduct\s+of\b', r'\binverse\s+of\b', r'\bsum\s+of\b',
    r'\bexpected\s+(number|value|payoff|time)\s+of\b', r'\bexpectation\s+of\b',
    r'\bdistance\s+between\b', r'\bsimilarity\s+between\b', r'\bangle\s+between\b',
    r'\bbasis\s+of\b', r'\bnull\s+space\s+of\b', r'\bkernel\s+of\b',
    r'\beigen(vectors?|values?)\s+of\b', r'\bdeterminant\s+of\b', r'\btrace\s+of\b',
    r'\blimit\s+of\b', r'\basymptotic\s+of\b',
    
    # "Why study", "Can X", "Are all X" forms
    r'\bwhy\s+study\b', r'\bcan\s+\w+\s+be\b', r'\bare\s+all\b',
    
    # Statement-form questions: "X is Y?" / "X does Y?"
    r'\b\w+\s+is\s+\w+\?', r'\b\w+\s+are\s+\w+\?', r'\b\w+\s+has\s+\w+\?',
    r'\bcan\s+\w+\s+\w+\?', r'\bdoes\s+\w+\s+\w+\?', r'\bis\s+\w+\s+\w+\?',
    
    # "Evaluating the", "Taking", "Understanding" as gerund question starters
    r'\bevaluating\s+the\b', r'\btaking\s+the\b', r'\bunderstanding\s+the\b',
    r'\bcomputing\s+the\b', r'\bfinding\s+the\b', r'\bcalculating\s+the\b',
    r'\bdetermining\s+the\b', r'\bproving\s+the\b', r'\bshowing\s+the\b',
]


# Excluded (non-need) patterns: announcements, showcases, meta-content
# Hard exclusion — if any matches, classify as 'random' regardless of need patterns
# NOTE: Generic terms like 'learning', 'tutorial', 'example' are REMOVED from excluded
# because they frequently appear in genuine Q&A questions (e.g., "roadmap for learning",
# "tutorial for X", "example of how to"). They were in E113 GENERIC_TERMS for GitHub
# repo descriptions but are false positives for Q&A forums.
EXCLUDED_PATTERNS = [
    # Meta/announcement patterns
    r'\bIC\b', r'\bshow\s+off\b', r'\bmy\s+new\b', r'\bwelcome\s+to\b',
    r'\bthank(s)?\b', r'\bimage(s)?\b', r'\bpicture(s)?\b', r'\bintroduction(s)?\b',
    r'\bannounc', r'\brelease\b', r'\blaunch\b', r'\bintroducing\b',
    r'\bshowcase\b', r'\bdemo\b', r'\bportfolio\b',
    r'^free\s', r'^best\s', r'^top\s', r'^awesome\s',
    
    # Generic/scaffolding vocabulary (refined from E113 GENERIC_TERMS)
    # Only patterns that clearly indicate template/boilerplate/showcase content
    r'\butils?\b', r'\bcommon\b', r'\bcore\b', r'\blibrary\b', r'\bpackage\b',
    r'\btool\b', r'\bhelper\b', r'\bbase\b', r'\bstandard\b', r'\bstdlib\b',
    r'\binternal\b', r'\bprivate\b', r'\bexperimental\b',
    r'\btemplate\b', r'\bboilerplate\b', r'\bscaffold\b', r'\bstarter\b',
    r'\bsandbox\b', r'\bplayground\b', r'\bexperimenting\b', r'\btoy\b', r'\bsample\b',
    r'\bproof\s+of\s+concept\b', r'\bpoc\b', r'\bprototype\b',
    r'\bexperiment\b',
]