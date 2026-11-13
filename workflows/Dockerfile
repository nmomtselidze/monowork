# syntax=docker/dockerfile:1

ARG GO_VERSION=1.27
FROM golang:${GO_VERSION}-bookworm

ARG GOLANGCI_LINT_VERSION=2.15.0
ARG TARGETARCH

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
        curl \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install golangci-lint (pinned, checksum-verified) for the lint job.
RUN set -eux; \
    arch="${TARGETARCH:-amd64}"; \
    cd /tmp; \
    curl -fsSLO "https://github.com/golangci/golangci-lint/releases/download/v${GOLANGCI_LINT_VERSION}/golangci-lint-${GOLANGCI_LINT_VERSION}-linux-${arch}.tar.gz"; \
    curl -fsSLO "https://github.com/golangci/golangci-lint/releases/download/v${GOLANGCI_LINT_VERSION}/golangci-lint-${GOLANGCI_LINT_VERSION}-checksums.txt"; \
    grep "golangci-lint-${GOLANGCI_LINT_VERSION}-linux-${arch}.tar.gz$" "golangci-lint-${GOLANGCI_LINT_VERSION}-checksums.txt" | sha256sum -c -; \
    tar -xzf "golangci-lint-${GOLANGCI_LINT_VERSION}-linux-${arch}.tar.gz"; \
    install -m 0755 "golangci-lint-${GOLANGCI_LINT_VERSION}-linux-${arch}/golangci-lint" /usr/local/bin/golangci-lint; \
    cd /; rm -rf /tmp/golangci-lint*

# Allow git operations in CI checkouts regardless of directory ownership.
RUN git config --global --add safe.directory '*'

ENV CI=true

WORKDIR /src

CMD ["bash"]
