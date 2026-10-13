# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 1.x     | yes       |
| < 1.0   | no        |

## Reporting a vulnerability

Email `security@ai-talking-pet-generator.dev` with a description, a minimal
reproducer, and the affected version. We aim to acknowledge within 72 hours.

Please do not open a public issue for anything exploitable. We will credit
reporters in the release notes unless you ask us not to.

## Scope

In scope:

- Arbitrary code execution via a malicious pet profile YAML or plugin.
- Path traversal in the profile/asset loader.
- Credential leakage from `services/` integrations.
- Insecure deserialization in the model or voice cache.

Out of scope:

- Anything that requires the user to already have local code execution.
- Vulnerabilities in third-party model weights or TTS binaries.

## Hardening notes for operators

- The plugin loader refuses unsigned entry points unless
  `PETGEN_ALLOW_UNSIGNED_PLUGINS=1` is set. Leave it unset in production.
- `config/local.yaml` is gitignored on purpose. Keep it that way.
- Voice/avatar model downloads are checksum-verified against
  `petgen/config/checksums.yaml`. Do not disable verification.