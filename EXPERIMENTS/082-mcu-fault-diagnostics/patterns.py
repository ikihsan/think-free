"""Pattern tables for the fault-code topic classifier.

Split out of `classify.py` at the 300-line cap: these are data, and the
module that uses them is logic. Behaviour is unchanged -- the tables are
moved verbatim, and `classify.py` imports them by name.
"""

import re  # noqa: F401  (re-exported for callers that imported it here)

NEED_PATTERNS = [
    # General need / help patterns
    r"\bhow (do|can|to|should|would|is|are)\b",
    r"\bwhat (is|are|should|would|could|causes?|makes?)\b",
    r"\bwhy (is|are|do|does|did|can|won|not)\b",
    r"\bhelp\b",
    r"\bissue|problem|error|broken|failure|not working\b",
    r"\brecommend|suggestion|advice\b",
    r"\bwhich (one|should|is best|to use)\b",
    r"\bwhere (can|to|is|are)\b",
    r"\bcan (someone|anybody|anyone)\b",
    r"\bstuck|confused|lost\b",
    r"\btrying to\b",
    r"\bdebug(ging)?\b",
    r"\bfix(ing)?\b",
    r"\btroubleshoot(ing)?\b",
    r"\bresolve\b",

    # Fault code specific patterns
    r"\bfault\b",
    r"\berror\b",
    r"\bcode\b",
    r"\blookup\b",
    r"\binterpret\b",
    r"\bdecode\b",
    r"\bunderstand\b",
    r"\bmeaning\b",
    r"\bwhat.does.this.mean\b",
    r"\bwhat does this code mean\b",

    # ARM-specific patterns
    r"\bHardFault\b",
    r"\bMemManage\b",
    r"\bBusFault\b",
    r"\bUsageFault\b",
    r"\bSVCall\b",
    r"\bPendSV\b",
    r"\bDebugMonitor\b",

    # RISC-V patterns
    r"\becall\b",
    r"\bebreak\b",

    # Vendor-specific patterns
    r"\bSTM\w+\b",
    r"\bNXP\w*\b",
    r"\bPIC\w*\b",
    r"\bAVR\w*\b",
]


# Non-need patterns — topics that are show-offs, announcements, etc.
NON_NEED_PATTERNS = [
    r"\bIC\b",  # Integrated circuit reference only
    r"\bshow.*(off|me)\b",
    r"\bmy (new|first|latest) (setup|build|project|purchase)\b",
    r"\blook at (this|my)\b",
    r"\bjust (got|bought|picked up|received)\b",
    r"\bwelcome to\b",
    r"\bthank(s| you)\b",
    r"\bimage(s)?\s*(only|thread)\b",
    r"\bpicture(s)?\s*(only|thread|una)\b",
    r"\bintroductions?\b",
    r"\bdemo\b",
    r"\bannouncement\b",
    r"\brelease\b",
    r"\bmy (first|new) (project|build|setup)\b",
]
