#!/usr/bin/env bash
# Export all agent schemas to JSON Schema files.
#
# Usage:
#   ./scripts/export-schemas.sh [output_dir]
#
# Default output: src/schemas/json/

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

OUTPUT_DIR="${1:-src/schemas/json}"
python3 -m src.schemas.export "$OUTPUT_DIR"
