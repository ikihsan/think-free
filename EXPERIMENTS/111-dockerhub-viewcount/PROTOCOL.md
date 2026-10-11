<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E111 — View-count principle on Docker Hub container images

## Objective

Test whether the view-count principle generalizes to Docker Hub container images. The principle states that **need-related images** (images addressing common infrastructure/deployment needs like web servers, databases, caches, message queues, monitoring, CI/CD, etc.) have systematically higher pull counts than **random images**.

## Background

The view-count principle has been tested on:
- **PyPI (E071)**: WORKS — need-related 82.93% active vs random 57.50%, all gates pass
- **NPM (E072)**: WORKS — 100% need-related active vs 0% random
- **NuGet (E102)**: WORKS — strong significance (p=1.7e-14, Cliff's δ=0.996)
- **Hex.pm (E103)**: WORKS — all gates pass, p≈0.000, Cliff's δ=0.861, need median 220× random
- **Packagist (E108)**: WORKS — all gates pass, p<0.001, Cliff's δ=0.994, need-related 100% active vs random 26%
- **RubyGems (E109)**: WORKS — all gates pass, p=0.0045, Cliff's δ=0.214, need median 2.0× random
- **Maven Central (E090)**: FAILS — activity-rate difference not significant (60% vs 52.2%)
- **crates.io (E095)**: FAILS — all crates active (100%), no binary discrimination
- **Hugging Face Hub (E101)**: FAILS — download dynamics differ, signal too weak
- **GitHub repos (E107)**: WORKS — all gates pass, Cliff's δ=0.826, need median 8.6× random
- **Code Review Stack Exchange (E100)**: WORKS — all gates pass, 73.3% unserved need rate
- **Discourse forums (E077, E082, E101)**: WORKS — unserved fraction 11-15%

Docker Hub is a genuinely new domain axis: **container image registry** with pull counts as the primary arrival metric. Unlike package registries (which distribute code libraries), Docker Hub distributes **runtime images** — complete, runnable environments. The pull count directly measures how many times an image has been downloaded/run, which is a strong proxy for "independent arrivals at a need."

## Hypothesis

**H1**: Need-related Docker images on Docker Hub have significantly higher pull counts than random images.

**H0**: No significant difference in pull counts between need-related and random images.

## Gates (per E071/E107/E108/E109 protocol)

| Gate | Criterion | Threshold |
|------|-----------|-----------|
| G1 | Classified sample size | ≥ 200 total (100 per group minimum) |
| G2 | Need-related pull counts > random pull counts | Mann-Whitney U test, p < 0.05, Cliff's delta > 0.147 |
| G3 | Effect size | Wilson CI95 lower bound for proportion of need-related above random median > 0.60 |
| G4 | Both categories represented | need-related > 0 AND random > 0 |

**Active definition**: An image is "active" if its pull count > 0. (All public images on Docker Hub have pull counts; we use pull_count as the primary continuous metric.)

**Need classification**: A Docker image is `need-related` iff its name/description contains at least one term from `NEED_INDICATORS` and does NOT contain any term from `GENERIC_TERMS` as a primary classifier.

```python
NEED_INDICATORS = {
    # Web servers / reverse proxies
    "nginx", "apache", "httpd", "caddy", "traefik", "envoy", "haproxy",
    # Databases
    "postgres", "mysql", "mariadb", "redis", "mongo", "mongodb", "cassandra",
    "elasticsearch", "opensearch", "dynamodb", "couchdb", "rethinkdb",
    "influxdb", "timescaledb", "clickhouse", "questdb", "sqlite",
    # Message queues / streaming
    "rabbitmq", "kafka", "nats", "pulsar", "redis", "memcached", "hazelcast",
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
    "istio", "linkerd", "consul", "envoy", "cilium", "calico", "flannel",
    # Databases - specialized
    "etcd", "zookeeper", "consul", "redis", "memcached",
    # Programming language runtimes (official images)
    "python", "node", "golang", "rust", "openjdk", "java", "ruby",
    "php", "dotnet", "swift", "elixir", "erlang", "clojure", "scala",
    "r-base", "julia", "perl", "haskell", "ocaml",
    # Infrastructure tools
    "terraform", "ansible", "packer", "vagrant", "vault", "consul",
    "nomad", "waypoint", "boundary",
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
    "elasticsearch", "opensearch", "solr", "meilisearch", "typesense",
    # Time series
    "influxdb", "timescaledb", "prometheus", "victoriametrics", "thanos",
    "cortex", "m3db",
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
    "personal", "private", "internal", "custom", "my-", "test-",
}
```

Note: Official images (is_official=true) are excluded from both groups to avoid biasing toward Docker-maintained images. We classify community images.

## Methodology

1. **Need-related sample**: Search Docker Hub API with need-indicator search terms. Collect up to 200 repositories.
2. **Random sample**: Search Docker Hub API with generic/random terms. Collect up to 200 repositories.
3. **Classification**: Apply need classification to all collected repositories. Keep only those confidently classified as `need-related` or `random`. Exclude official images.
4. **Activity measurement**: For each repo, record pull_count, star_count, is_official, is_automated, description.
5. **Gate evaluation**: Run Mann-Whitney U test on pull counts, compute Cliff's delta, Wilson CI95 for proportion above median.

## API Endpoints

- Search repos: `https://hub.docker.com/v2/search/repositories/?query={query}&page_size=100&page={page}`
- Rate limit: Unauthenticated, per-minute limit (headers: X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset)

Rate limit is per minute; we'll pace requests and respect Retry-After headers.

## Search Queries (pre-declared)

**Need-related queries** (will search and aggregate):
- `nginx`, `postgres`, `mysql`, `redis`, `mongo`, `rabbitmq`, `kafka`
- `prometheus`, `grafana`, `jenkins`, `gitlab`, `kubernetes`, `docker`
- `terraform`, `ansible`, `vault`, `consul`, `nginx`, `traefik`
- `kong`, `elasticsearch`, `influxdb`, `minio`, `cert-manager`

**Random queries** (generic terms that shouldn't systematically select need-related images):
- `ubuntu`, `debian`, `alpine`, `busybox`, `centos`, `fedora`
- `python`, `node`, `golang`, `openjdk`, `ruby`, `php` (language runtimes - these may be need-related; we'll classify by description)
- `hello-world`, `busybox`, `scratch`, `distroless`

Actually, language runtimes are need-related (official Python/Node/Java images serve the need "I need to run Python/Node/Java"). We'll include them in need-related queries but classify by description.

Better approach: Search broadly, then classify all results by description/name.

## Success Criteria

All four gates (G1-G4) must pass for the principle to be considered supported on Docker Hub.

## Falsification

If G2 fails (p ≥ 0.05 or Cliff's delta ≤ 0.147) OR G3 fails (Wilson LB ≤ 0.60), the principle does not generalize to Docker Hub under this measurement.

## Deliverables

- `harvest.py` — Data collection script
- `classify.py` — Classification script
- `analyze.py` — Gate evaluation script
- `results.json` — Raw results with gate outcomes
- `raw_data.json` — Raw harvested data
- `README.md` — Experiment summary