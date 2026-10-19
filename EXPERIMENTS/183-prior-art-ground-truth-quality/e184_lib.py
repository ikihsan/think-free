"""E184 support — Stack Exchange API and text processing.

Split from e184_experiment.py at the 300-line cap (2026-10-18). The
experiment driver imports `fetch_questions`, `fetch_answers` and
`compute_tfidf` from here; `e184_model.py` imports `tokenize` and
`cosine_similarity`. No behaviour changed in the split.
"""

import gzip
import io
import json
import math
import re
import time
import urllib.parse
import urllib.request
from collections import Counter

# ---------- Stack Exchange API ----------

API_BASE = "https://api.stackexchange.com/2.3"
SITE = "stackoverflow"


def api_get(path, params=None, max_retries=3):
    """Make a GET request to the Stack Exchange API with retry."""
    if params is None:
        params = {}
    params["site"] = SITE
    params["filter"] = "withbody"
    url = f"{API_BASE}/{path}?{urllib.parse.urlencode(params)}"
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip"})
            resp = urllib.request.urlopen(req, timeout=15)
            data = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                data = gzip.GzipFile(fileobj=io.BytesIO(data)).read()
            return json.loads(data)
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))
            else:
                raise


def fetch_questions(n=200, pagesize=100):
    """Fetch n high-vote questions with answers."""
    questions = []
    page = 1
    while len(questions) < n:
        params = {
            "pagesize": min(pagesize, n - len(questions)),
            "page": page,
            "order": "desc",
            "sort": "votes",
            "filter": "withbody",
        }
        data = api_get("questions", params)
        items = data.get("items", [])
        if not items:
            break
        for item in items:
            if item.get("answer_count", 0) >= 2:
                questions.append(item)
        page += 1
        if not data.get("has_more"):
            break
        time.sleep(0.5)
    return questions[:n]


def fetch_answers(question_id):
    """Fetch all answers for a question."""
    params = {
        "pagesize": 100,
        "order": "desc",
        "sort": "votes",
        "filter": "withbody",
    }
    data = api_get(f"questions/{question_id}/answers", params)
    return data.get("items", [])


# ---------- Text processing ----------

def tokenize(text):
    """Simple tokenizer: lowercase, extract word tokens."""
    if not text:
        return []
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"```.*?```", " CODE ", text, flags=re.DOTALL)
    return re.findall(r"[a-z]+", text.lower())


def compute_tfidf(documents):
    """Compute TF-IDF vectors for a list of documents."""
    tokenized = [tokenize(doc) for doc in documents]
    df = Counter()
    for tokens in tokenized:
        for token in set(tokens):
            df[token] += 1
    n_docs = len(documents)
    vectors = []
    for tokens in tokenized:
        tf = Counter(tokens)
        vec = {}
        for token, count in tf.items():
            if df[token] > 1:
                tf_val = 1 + math.log(count)
                idf_val = math.log(n_docs / df[token])
                vec[token] = tf_val * idf_val
        norm = math.sqrt(sum(v ** 2 for v in vec.values()))
        if norm > 0:
            vec = {k: v / norm for k, v in vec.items()}
        vectors.append(vec)
    return vectors


def cosine_similarity(vec1, vec2):
    """Cosine similarity between two sparse vectors."""
    common = set(vec1.keys()) & set(vec2.keys())
    if not common:
        return 0.0
    return sum(vec1[k] * vec2[k] for k in common)
