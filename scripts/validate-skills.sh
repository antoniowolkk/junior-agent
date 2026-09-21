#!/usr/bin/env bash
# Validate every skills/<name>/SKILL.md against CONTRIBUTING-SKILLS.md's mechanical rules.
# Exits non-zero on the first failing rule, listing every violation.
set -euo pipefail

cd "$(dirname "$0")/.."
exec python3 scripts/validate_skills.py "$@"
