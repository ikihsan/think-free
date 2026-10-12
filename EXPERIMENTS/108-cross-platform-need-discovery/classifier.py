#!/usr/bin/env python3
"""Need and language classifier for cross-platform need discovery."""

import re
from typing import Dict, List, Set, Tuple


# Need indicators from E078/E103/E106
NEED_INDICATORS: Set[str] = {
    "web", "rest", "api", "http", "client", "server", "framework",
    "database", "orm", "sql", "postgres", "mysql", "redis", "mongo",
    "json", "xml", "yaml", "parser", "serializer", "encoder", "decoder",
    "auth", "oauth", "jwt", "session", "cookie", "security",
    "cache", "queue", "worker", "job", "background", "async",
    "test", "mock", "fixture", "benchmark", "profile",
    "config", "settings", "env", "environment", "secret",
    "logger", "logging", "telemetry", "metrics", "tracing",
    "email", "mail", "smtp", "notification", "push",
    "file", "storage", "upload", "download", "archive",
    "image", "video", "audio", "media", "thumbnail",
    "search", "index", "elasticsearch", "fulltext",
    "graphql", "grpc", "websocket", "realtime", "pubsub",
    "crypto", "hash", "encrypt", "decrypt", "sign", "verify",
    "validate", "validator", "schema", "contract",
    "template", "render", "view", "html", "css", "asset",
    "router", "routing", "dispatch", "handler", "middleware",
    "dependency", "injection", "container", "provider",
    "cli", "command", "argument", "flag", "option",
    "migration", "schema", "seed", "factory",
}

GENERIC_TERMS: Set[str] = {
    "utils", "common", "core", "library", "package",
    "dep", "dependency", "tool", "util", "helper", "base",
    "standard", "stdlib", "internal", "private", "experimental",
}

# Language detection keywords
LANGUAGE_KEYWORDS: Dict[str, List[str]] = {
    "python": ["python", "py", "django", "flask", "fastapi", "asyncio", "pypi", "pip", "pytest", "aiohttp", "requests"],
    "javascript": ["javascript", "js", "node", "npm", "react", "vue", "angular", "express", "webpack", "babel"],
    "typescript": ["typescript", "ts", "node", "npm", "deno"],
    "csharp": ["csharp", "c#", ".net", "dotnet", "nuget", "aspnet", "entityframework", "blazor"],
    "elixir": ["elixir", "ex", "phoenix", "ecto", "hex", "mix", "plug"],
    "rust": ["rust", "cargo", "crates", "tokio", "actix", "serde"],
    "go": ["go", "golang", "gin", "echo", "fiber"],
    "java": ["java", "maven", "gradle", "spring", "springboot"],
    "ruby": ["ruby", "rails", "gem", "bundler", "rake"],
    "php": ["php", "laravel", "symfony", "composer"],
}


def classify_need(query: str) -> Dict[str, any]:
    """
    Classify a natural language query into need categories.
    
    Returns:
        dict with keys: need_indicators_found, generic_terms_found, 
        classification (need-related/random/ambiguous), categories (list of detected categories)
    """
    query_lower = query.lower()
    
    # Find need indicators
    need_found = [term for term in NEED_INDICATORS if term in query_lower]
    
    # Find generic terms
    generic_found = [term for term in GENERIC_TERMS if term in query_lower]
    
    # Determine classification
    if need_found and not generic_found:
        classification = "need-related"
    elif not need_found and generic_found:
        classification = "random"
    else:
        # Both or neither - use counts
        need_count = len(need_found)
        generic_count = len(generic_found)
        if need_count > generic_count:
            classification = "need-related"
        elif generic_count > need_count:
            classification = "random"
        else:
            classification = "ambiguous"
    
    # Categorize by functional area
    categories = categorize_need(need_found)
    
    return {
        "need_indicators_found": need_found,
        "generic_terms_found": generic_found,
        "classification": classification,
        "categories": categories,
    }


def categorize_need(need_terms: List[str]) -> List[str]:
    """Map need indicators to functional categories."""
    category_map = {
        "web": ["web", "rest", "api", "http", "client", "server", "framework", "router", "routing", "middleware", "handler", "dispatch", "template", "render", "view", "html", "css", "asset"],
        "database": ["database", "orm", "sql", "postgres", "mysql", "redis", "mongo", "migration", "schema", "seed", "factory"],
        "auth": ["auth", "oauth", "jwt", "session", "cookie", "security", "crypto", "hash", "encrypt", "decrypt", "sign", "verify", "validate", "validator"],
        "cache": ["cache", "queue", "worker", "job", "background", "async", "pubsub", "realtime", "websocket", "grpc", "graphql"],
        "testing": ["test", "mock", "fixture", "benchmark", "profile"],
        "config": ["config", "settings", "env", "environment", "secret", "dependency", "injection", "container", "provider"],
        "observability": ["logger", "logging", "telemetry", "metrics", "tracing"],
        "messaging": ["email", "mail", "smtp", "notification", "push", "queue", "pubsub"],
        "file": ["file", "storage", "upload", "download", "archive", "parser", "serializer", "encoder", "decoder", "json", "xml", "yaml"],
        "media": ["image", "video", "audio", "media", "thumbnail"],
        "search": ["search", "index", "elasticsearch", "fulltext"],
        "cli": ["cli", "command", "argument", "flag", "option"],
    }
    
    categories = []
    for cat, terms in category_map.items():
        if any(t in need_terms for t in terms):
            categories.append(cat)
    
    return categories if categories else ["general"]


def detect_language(query: str) -> List[Tuple[str, int]]:
    """
    Detect likely programming languages from query.
    
    Returns list of (language, score) tuples sorted by score descending.
    """
    query_lower = query.lower()
    scores = {}
    
    for lang, keywords in LANGUAGE_KEYWORDS.items():
        score = 0
        for kw in keywords:
            # Exact word boundary match for better precision
            if kw in ["c#", "csharp", "f#", "vb.net"]:
                # Special handling for language identifiers with special chars
                if kw in query_lower:
                    score += 3  # Higher weight for explicit language identifiers
            elif re.search(r'\b' + re.escape(kw) + r'\b', query_lower):
                score += 1
        if score > 0:
            scores[lang] = score
    
    # Sort by score descending, then by language name for consistency
    return sorted(scores.items(), key=lambda x: (-x[1], x[0]))


def extract_search_terms(query: str, max_terms: int = 5) -> List[str]:
    """Extract key search terms from query for platform APIs."""
    # Remove common words
    stopwords = {"a", "an", "the", "for", "in", "on", "at", "to", "with", "and", "or", "of", "my", "i", "need", "want", "looking", "find", "get", "use", "using"}
    
    words = re.findall(r'\b\w+\b', query.lower())
    terms = [w for w in words if w not in stopwords and len(w) > 2]
    
    # Prioritize need indicators
    prioritized = []
    remaining = []
    for term in terms:
        if term in NEED_INDICATORS:
            prioritized.append(term)
        else:
            remaining.append(term)
    
    return (prioritized + remaining)[:max_terms]


def build_platform_query(query: str, platform: str, language: str = None) -> str:
    """Build a platform-specific search query."""
    terms = extract_search_terms(query)
    
    if platform == "pypi":
        # PyPI search works well with space-separated terms
        return " ".join(terms)
    elif platform == "npm":
        # NPM search also uses space-separated
        return " ".join(terms)
    elif platform == "github":
        # GitHub search supports qualifiers
        base = " ".join(terms)
        if language:
            base += f" language:{language}"
        return base
    elif platform == "nuget":
        return " ".join(terms)
    elif platform == "hex":
        return " ".join(terms)
    else:
        return " ".join(terms)


if __name__ == "__main__":
    import sys
    
    test_queries = [
        "async HTTP client for Python",
        "React state management library",
        "C# database ORM Entity Framework",
        "Elixir web framework Phoenix",
        "Rust async runtime Tokio",
        "generic utility library",
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = classify_need(query)
        print(f"  Classification: {result['classification']}")
        print(f"  Need indicators: {result['need_indicators_found']}")
        print(f"  Categories: {result['categories']}")
        langs = detect_language(query)
        print(f"  Languages: {langs}")
        print(f"  Search terms: {extract_search_terms(query)}")