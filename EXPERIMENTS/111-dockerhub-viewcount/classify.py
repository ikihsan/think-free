#!/usr/bin/env python3
"""
E111 — Classify Docker Hub repositories as need-related or random.
"""

import json
import re
from pathlib import Path


NEED_INDICATORS = {
    # Web servers / reverse proxies
    "nginx", "apache", "httpd", "caddy", "traefik", "envoy", "haproxy",
    # Databases
    "postgres", "mysql", "mariadb", "redis", "mongo", "mongodb", "cassandra",
    "elasticsearch", "opensearch", "dynamodb", "couchdb", "rethinkdb",
    "influxdb", "timescaledb", "clickhouse", "questdb", "sqlite",
    # Message queues / streaming
    "rabbitmq", "kafka", "nats", "pulsar", "memcached", "hazelcast",
    # Monitoring / observability
    "prometheus", "grafana", "loki", "tempo", "jaeger", "zipkin", "datadog",
    "newrelic", "elastic", "filebeat", "logstash", "fluentd", "vector",
    "telegraf", "collectd", "node-exporter", "cadvisor",
    # CI/CD / deployment
    "jenkins", "gitlab", "drone", "argo", "tekton", "spinnaker", "helm",
    "kustomize", "kube", "kubectl", "istio", "linkerd", "consul", "vault",
    # Containers / orchestration
    "kubernetes", "k8s", "docker", "containerd", "cri-o", "podman",
    "rancher", "k3s", "microk8s", "kind", "minikube",
    # Service mesh / networking
    "cilium", "calico", "flannel",
    # Databases - specialized
    "etcd", "zookeeper",
    # Programming language runtimes (official images)
    "python", "node", "golang", "rust", "openjdk", "java", "ruby",
    "php", "dotnet", "swift", "elixir", "erlang", "clojure", "scala",
    "r-base", "julia", "perl", "haskell", "ocaml",
    # Infrastructure tools
    "terraform", "ansible", "packer", "vagrant", "nomad", "waypoint", "boundary",
    # Security / auth
    "oauth", "oauth2", "oidc", "keycloak", "dex", "authelia",
    "oauth2-proxy", "cert-manager", "letsencrypt", "acme",
    # Storage / file systems
    "minio", "ceph", "rook", "longhorn", "nfs", "glusterfs",
    # Logging / tracing
    "fluentd", "fluent-bit", "logstash", "filebeat", "vector",
    # Load balancing / proxy
    "nginx", "traefik", "haproxy", "envoy", "caddy", "apache",
    # API gateway
    "kong", "krakend", "tyk", "gloo", "ambassador", "apisix",
    # Databases - search / analytics
    "solr", "meilisearch", "typesense",
    # Time series
    "victoriametrics", "thanos", "cortex", "m3db",
}

GENERIC_TERMS = {
    "base", "minimal", "alpine", "scratch", "distroless", "slim",
    "latest", "stable", "edge", "main", "master", "dev", "test",
    "ci", "build", "builder", "compile", "runtime", "debug",
    "example", "demo", "sample", "template", "boilerplate",
    "sandbox", "playground", "poc", "prototype", "experiment",
    "tutorial", "learning", "practice", "training", "workshop",
    "fork", "mirror", "copy", "backup", "archive", "old",
    "deprecated", "legacy", "unmaintained", "abandoned",
    "personal", "private", "internal", "custom",
}


def tokenize(text):
    """Tokenize text into lowercase words, splitting on non-alphanumeric."""
    if not text:
        return []
    # Split on non-alphanumeric, keep hyphens within words
    tokens = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text.lower())
    return tokens


def classify_repo(repo):
    """
    Classify a repository as 'need-related', 'random', or 'uncertain'.
    Excludes official images entirely.
    """
    # Skip official images
    if repo.get("is_official"):
        return "official"

    name = repo.get("repo_name", "").lower()
    description = repo.get("short_description", "").lower()

    # Combine name and description for classification
    full_text = f"{name} {description}"
    tokens = set(tokenize(full_text))

    # Check for generic terms first (these disqualify from need-related)
    generic_matches = tokens & GENERIC_TERMS
    # But only disqualify if generic term is dominant (e.g., "nginx-base" is still need-related)
    # For now, if ANY generic term matches AND no need indicator matches -> random

    need_matches = tokens & NEED_INDICATORS

    # Special handling: language runtimes are need-related
    # But only if they're the main focus (e.g., "python" not "my-python-app")
    language_runtimes = {"python", "node", "golang", "rust", "openjdk", "java",
                         "ruby", "php", "dotnet", "swift", "elixir", "erlang",
                         "clojure", "scala", "r-base", "julia", "perl", "haskell", "ocaml"}

    # If name is exactly a language runtime or starts with it (official-style)
    name_parts = name.split("/")[-1]  # Get last part after /
    is_language_runtime = name_parts in language_runtimes

    if need_matches:
        # Has need indicator
        if generic_matches and not (need_matches - generic_matches):
            # Only generic matches, no pure need matches
            return "random"
        return "need-related"

    if is_language_runtime:
        return "need-related"

    # If no need indicators but also no strong generic signals -> uncertain
    if not generic_matches:
        return "uncertain"

    return "random"


def main():
    input_path = Path(__file__).parent / "raw_data.json"
    with open(input_path) as f:
        data = json.load(f)

    repos = data["repositories"]

    classified = {
        "need-related": [],
        "random": [],
        "uncertain": [],
        "official": [],
    }

    for repo in repos:
        classification = classify_repo(repo)
        classified[classification].append(repo)

    print("Classification results:")
    for cat, items in classified.items():
        print(f"  {cat}: {len(items)}")

    # Filter to only need-related and random for analysis
    analysis_repos = classified["need-related"] + classified["random"]

    # Save classified data
    output = {
        "classified": classified,
        "analysis_set": analysis_repos,
        "counts": {k: len(v) for k, v in classified.items()},
    }

    out_path = Path(__file__).parent / "classified_data.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved classified data to {out_path}")

    # Show some examples
    print("\nExample need-related:")
    for repo in classified["need-related"][:10]:
        print(f"  {repo['repo_name']}: pulls={repo.get('pull_count', 0)}, stars={repo.get('star_count', 0)}")

    print("\nExample random:")
    for repo in classified["random"][:10]:
        print(f"  {repo['repo_name']}: pulls={repo.get('pull_count', 0)}, stars={repo.get('star_count', 0)}")


if __name__ == "__main__":
    main()