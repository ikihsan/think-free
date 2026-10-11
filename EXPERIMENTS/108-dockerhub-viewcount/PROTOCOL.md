# E108 — View-count principle on Docker Hub (container registry)

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-11
-->

## Origin
- Mission: Think Free
- Decision driver: D083 — "the next session must start from fresh observation in a new domain"
- Predecessors: E071 (PyPI), E090 (Maven Central), E095 (crates.io), E101 (Hugging Face Hub), E102 (NuGet), E103 (Hex.pm), 0xx-cpan-viewcount (CPAN), 0xx-packagist-viewcount (Packagist)
- This experiment tests whether the view-count principle generalizes to Docker Hub, the primary container image registry

## Question
Does the view-count principle hold on Docker Hub? Specifically: are container images whose metadata indicates they address a developer/operator need (need-related) systematically more active (higher pull counts) than random images?

## Hypothesis
H0: Need-related images on Docker Hub have the same pull activity distribution as random images.
H1: Need-related images on Docker Hub have significantly higher pull activity than random images.

## Population and Sampling

### Source
Docker Hub API v2: `https://hub.docker.com/v2/search/repositories/?query=<query>&page_size=100`

### Need-related image definition
An image is "need-related" if its name, short_description, or full_description contain keywords indicating it solves a specific infrastructure/developer/operator problem or fulfills a common operational need. Keywords include but are not limited to:

**Infrastructure & Operations:**
- Database: "database", "db", "postgres", "mysql", "mongo", "redis", "elasticsearch", "cassandra", "couchdb", "sqlite", "mariadb", "dynamodb", "etcd", "consul", "vault"
- Cache: "cache", "caching", "memcached", "hazelcast", "ignite"
- Queue/Message: "queue", "rabbitmq", "kafka", "nats", "pulsar", "activemq", "mosquitto", "emqx", "mqtt"
- Web/Proxy: "nginx", "apache", "traefik", "haproxy", "envoy", "caddy", "reverse-proxy", "load-balancer", "api-gateway", "ingress"
- CI/CD: "jenkins", "gitlab", "github-actions", "circleci", "travis", "drone", "tekton", "argo", "spinnaker", "concourse"
- Monitoring: "prometheus", "grafana", "datadog", "newrelic", "jaeger", "zipkin", "otel", "opentelemetry", "loki", "tempo", "thanos", "victoria-metrics"
- Logging: "elk", "fluentd", "logstash", "filebeat", "vector", "syslog", "lumberjack"
- Kubernetes: "kubernetes", "k8s", "kubectl", "helm", "kustomize", "operator", "crd", "cni", "csi", "service-mesh", "istio", "linkerd", "cilium", "calico"
- Security: "vault", "cert-manager", "oauth", "oidc", "sso", "ldap", "kerberos", "firewall", "waf", "falco", "trivy", "anchore", "syft", "cosign", "notary"
- Storage: "minio", "ceph", "rook", "longhorn", "openebs", "nfs", "csi-driver", "backup", "restic", "velero"
- Network: "coredns", "dns", "vpn", "wireguard", "tailscale", "zerotier", "frp", "ngrok", "cloudflare-tunnel"
- Service Mesh: "istio", "linkerd", "consul", "envoy", "sidecar", "mtls"
- Observability: "tracing", "metrics", "logging", "profiling", "apm", "rum", "synthetics"

**Development Tools:**
- Build: "build", "compile", "maven", "gradle", "npm", "yarn", "pnpm", "pip", "poetry", "cargo", "go-build", "bazel", "make", "cmake"
- Test: "test", "pytest", "jest", "mocha", "junit", "testcontainers", "cypress", "playwright", "k6", "locust"
- Lint/Format: "lint", "prettier", "eslint", "black", "ruff", "gofmt", "clang-format", "fmt"
- IDE/Editor: "vscode", "vim", "neovim", "emacs", "intellij", "goland", "pycharm"
- Version Control: "git", "github", "gitlab", "bitbucket", "gitea", "forgejo"

### Random image definition
An image sampled without keyword filtering, using a non-selective query (e.g., common letters, pagination through default listing) that does not select for need-relatedness.

### Sample sizes
- Need-related: target n ≥ 50 (per G1 gate)
- Random: target n ≥ 50 (per G1 gate)

### Activity metric
Primary: `pull_count` field from Docker Hub API (cumulative pulls across all tags)
Secondary: `star_count` field from Docker Hub API

## Gates (predeclared, must all pass for principle to be considered supported)

### G1 — Retrieval (sample size)
Both arms must return ≥50 classified images each.
- If either arm <50: FAIL, principle not testable on this platform.

### G2 — Separation (statistical significance)
Mann-Whitney U test (two-sided) comparing pull_count of need-related vs random images.
- p < 0.05 required for PASS.
- Effect size (Cliff's delta) also reported, must exceed 0.147 (small effect threshold).

### G3 — Effect magnitude (practical significance)
Wilson lower bound of the proportion of need-related images with pull_count > median of random images must exceed 0.60.
- Equivalent to: need-related images are "more active" than random at a rate that is practically meaningful.

### G4 — Arrival field coverage
≥95% of sampled images must have a non-zero, non-null `pull_count` field.
- If field missing or zero for >5%: FAIL, activity metric not reliable on this platform.

## Procedure

1. Fetch need-related images: query Docker Hub API with keyword-based queries, classify each result.
2. Fetch random images: query Docker Hub API with non-selective queries (e.g., "a", "b", "c", pagination), classify each result.
3. For each image, record: name, pull_count, star_count, short_description, full_description, classification.
4. Apply gates G1–G4.
5. Report all numbers, confidence intervals, and gate verdicts.

## Analysis script
`run.py` — implements the protocol, prints gate verdicts, writes `results.json`.

## Reproduction
```bash
cd EXPERIMENTS/108-dockerhub-viewcount
python3 run.py --gate
```

## Outputs
- `results.json` — machine-readable gate results and raw data
- `README.md` — human-readable summary

## Kill condition
If any gate FAILs, the view-count principle does not generalize to Docker Hub under this protocol. The experiment closes the Docker Hub line for this principle.