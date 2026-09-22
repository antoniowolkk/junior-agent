# Security Policy

Junior is a Claude Code plugin: a set of markdown skills and prompt instructions. It contains no
runtime code that executes on your machine outside of Claude Code itself, but skills can still
carry unsafe instructions (e.g. a compromised skill telling an agent to run destructive commands
or exfiltrate data).

## Reporting a vulnerability

If you find a skill that could cause an agent to take an unsafe or unintended action — data
exfiltration, destructive commands, prompt injection vectors, or similar — please report it
privately rather than opening a public issue:

- Email: security@wolkk.com
- Or use GitHub's [private vulnerability reporting](https://github.com/antoniowolkk/junior-agent/security/advisories/new)

Include the affected skill/file, the triggering prompt, and the unsafe behavior observed.

## Response

We aim to acknowledge reports within 5 business days and to ship a fix or mitigation before
public disclosure. Please give us reasonable time to respond before disclosing publicly.

## Scope

In scope: skill instructions, scripts under `scripts/`, plugin/marketplace manifests.
Out of scope: vulnerabilities in Claude Code itself (report those to Anthropic) or in projects
that merely use this pack.
