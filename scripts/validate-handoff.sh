#!/usr/bin/env bash
# Validate an agent handoff report against its Pydantic schema.
#
# Usage:
#   echo '{"agent": "researcher", ...}' | ./scripts/validate-handoff.sh
#   ./scripts/validate-handoff.sh '{"agent": "reviewer", ...}'
#
# Exit codes:
#   0 = valid handoff
#   1 = invalid handoff (errors on stderr)
#   2 = missing dependencies

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Check for Python and pydantic
if ! command -v python3 &>/dev/null; then
    echo "python3 not found" >&2
    exit 2
fi

cd "$PROJECT_DIR"

if [ $# -gt 0 ]; then
    python3 -m src.schemas.validate "$1"
else
    python3 -m src.schemas.validate
fi
