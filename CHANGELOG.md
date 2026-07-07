# Changelog

All notable Maelstrom changes. Format based on [Keep a Changelog](https://keepachangelog.com/),
versions follow [SemVer](https://semver.org/).

## [0.2.0] — July 2026

### Added
- **gRPC**: call any service straight from a `.proto` file — no `protoc` needed
  (unary + server/client/bidirectional streaming), gRPC load testing,
  automatic resolution of proto import roots.
- **WebSocket**: connect, send/receive messages, load testing (message round-trip latency).
- **Response assertions**: status / latency / header / body text / JSON field checks.
- **Databases as a data source** (in the app and the CLI): feed request data straight
  from SQL; plus **file pools** (folder / file list / S3-URL) for multipart uploads.
- **Per-environment secrets**: mark a variable as secret and it exports to CI configs
  as a `${KEY}` placeholder — each cluster injects its own value.
- "Test connection" button for database datasets.
- **English UI** as the base language + EN/RU switcher.
- **Export for CI** dialog: rename env variables on export and get the exact list of
  variables to define in your cluster; also available from the single-request Load tab.
- **CLI distribution**: Windows/macOS/Linux binaries + Docker image
  `ghcr.io/slakertop1/maelstrom-cli`; ready-made GitHub Actions / GitLab CI /
  Kubernetes examples in [`deploy/`](deploy/); a live demo API with an OpenAPI spec
  and a ready load scenario in [`examples/demo-api/`](examples/demo-api/).
- **Linux desktop builds**: `.deb` (Debian/Ubuntu), `.rpm` (Fedora/RHEL) and
  a portable `.AppImage`.
- End-to-end logging with secret redaction; "Report a bug" button in the app.

## [0.1.0] — July 2026

First public beta.

### Features
- HTTP client with collections and `{{var}}` environments.
- Load testing (virtual users / duration / RPS cap), live charts, HTML report.
- OAuth2/SSO with automatic token refresh under load; mTLS client certificates.
- Database load testing (Postgres / MySQL / SQLite); OpenAPI/Swagger import.
- Multi-endpoint "service load"; headless CLI for CI/Kubernetes + Docker image.
