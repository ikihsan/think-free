#!/usr/bin/env python3
"""
Docker Hub image classification logic.
"""

from typing import List

# Keywords indicating an image solves a specific infrastructure/developer/operator need
NEED_KEYWORDS: List[str] = [
    # Databases
    "database", "postgres", "mysql", "mongo", "redis", "elasticsearch",
    "cassandra", "couchdb", "sqlite", "mariadb", "dynamodb", "etcd",
    "consul", "vault", "cockroachdb", "timescaledb", "influxdb",
    "clickhouse", "scylla", "tidb", "yugabyte", "singlestore",
    
    # Cache
    "cache", "caching", "memcached", "hazelcast", "ignite", "dragonfly",
    "keydb", "valkey",
    
    # Queue/Message
    "queue", "rabbitmq", "kafka", "nats", "pulsar", "activemq",
    "mosquitto", "emqx", "mqtt", "redpanda", "vector",
    
    # Web/Proxy
    "nginx", "apache", "traefik", "haproxy", "envoy", "caddy",
    "reverse-proxy", "load-balancer", "api-gateway", "ingress",
    "openresty", "kong", "apisix", "gloo", "ambassador",
    
    # CI/CD
    "jenkins", "gitlab", "github-actions", "circleci", "travis",
    "drone", "tekton", "argo", "spinnaker", "concourse",
    "woodpecker", "gitea", "forgejo",
    
    # Monitoring
    "prometheus", "grafana", "datadog", "newrelic", "jaeger",
    "zipkin", "otel", "opentelemetry", "loki", "tempo",
    "thanos", "victoria-metrics", "cortex", "mimir",
    "alertmanager", "karma", "signoz",
    
    # Logging
    "elk", "fluentd", "logstash", "filebeat", "vector",
    "syslog", "lumberjack", "fluent-bit",
    
    # Kubernetes
    "kubernetes", "k8s", "kubectl", "helm", "kustomize",
    "operator", "crd", "cni", "csi", "service-mesh",
    "istio", "linkerd", "cilium", "calico", "flannel",
    "weave", "kube-proxy", "kubelet", "containerd",
    "crio", "k3s", "k0s", "kind", "minikube", "microk8s",
    "rancher", "harvester", "longhorn", "openebs", "rook",
    
    # Security
    "cert-manager", "oauth", "oidc", "sso", "ldap", "kerberos",
    "firewall", "waf", "falco", "trivy", "anchore", "syft",
    "cosign", "notary", "kyverno", "gatekeeper", "opa",
    "spiffe", "spire", "letsencrypt", "acme",
    
    # Storage/Backup
    "minio", "ceph", "rook", "longhorn", "openebs", "nfs",
    "csi-driver", "backup", "restic", "velero", "kopia",
    "duplicati", "borg", "rclone",
    
    # Network
    "coredns", "dns", "vpn", "wireguard", "tailscale",
    "zerotier", "frp", "ngrok", "cloudflare-tunnel",
    "istio", "linkerd", "consul", "envoy", "sidecar", "mtls",
    
    # Development Tools
    "build", "compile", "maven", "gradle", "npm", "yarn",
    "pnpm", "pip", "poetry", "cargo", "go-build", "bazel",
    "make", "cmake", "meson", "ninja",
    "test", "pytest", "jest", "mocha", "junit", "testcontainers",
    "cypress", "playwright", "k6", "locust", "gatling",
    "lint", "prettier", "eslint", "black", "ruff", "gofmt",
    "clang-format", "fmt", "golangci-lint", "pylint",
    "mypy", "typer", "click", "argparse", "cobra",
    "vscode", "vim", "neovim", "emacs", "intellij", "goland", "pycharm",
    "git", "github", "gitlab", "bitbucket", "gitea", "forgejo",
]


# Generic terms that indicate a non-specific/utility image
GENERIC_TERMS: List[str] = [
    "utils", "common", "core", "library", "package", "tool", "util", "helper",
    "base", "standard", "stdlib", "internal", "private", "experimental",
    "template", "boilerplate", "scaffold", "starter", "example", "demo",
    "tutorial", "learning", "practice", "playground", "sandbox", "toy",
    "sample", "proof-of-concept", "poc", "prototype", "experiment",
    "test", "testing", "test-", "debug", "debug-",
]


def classify_image(image_data: dict) -> str:
    """Classify an image as need-related or random based on search result metadata."""
    text = " ".join([
        image_data.get("repo_name", "") or "",
        image_data.get("short_description", "") or "",
        image_data.get("description", "") or "",
    ]).lower()
    
    # Check for generic terms first - if present, classify as random
    for term in GENERIC_TERMS:
        if term in text:
            return "random"
    
    # Check for need-related keywords
    for kw in NEED_KEYWORDS:
        if kw in text:
            return "need-related"
    
    return "random"


# Keyword groups for need-related sampling
NEED_KEYWORD_GROUPS: List[str] = [
    "database", "cache", "queue", "nginx", "traefik", "prometheus",
    "grafana", "kafka", "rabbitmq", "redis", "postgres", "mysql",
    "kubernetes", "istio", "vault", "minio", "cert-manager",
    "jenkins", "gitlab", "argocd", "flux",
    "nginx-ingress", "traefik-ingress", "envoy", "consul",
    "coredns", "external-dns", "metallb", "calico", "cilium",
    "containerd", "crio", "k3s", "kind", "rancher",
    "trivy", "falco", "kyverno", "opa", "gatekeeper",
    "velero", "restic", "rclone", "borgbackup",
    "wireguard", "tailscale", "zerotier", "frp", "ngrok",
    "buildkit", "kaniko", "buildpacks",
    "gitlab-runner", "jenkins-agent", "drone-runner",
]

# Non-selective queries for random sampling
RANDOM_QUERIES: List[str] = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
]