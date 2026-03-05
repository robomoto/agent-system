"""Export all agent schemas to JSON Schema files.

Usage: python -m src.schemas.export [output_dir]

Generates one .json file per agent schema in the output directory.
These JSON Schema files can be used with Claude's structured outputs
(strict: true) to constrain agent output at generation time.
"""

import json
import sys
from pathlib import Path

from src.schemas.agents import (
    ArchitectHandoff,
    ClaudeAISpecialistHandoff,
    CostAccountantHandoff,
    ImplementerHandoff,
    LanguageSpecialistHandoff,
    ResearcherHandoff,
    ReviewerHandoff,
    SREHandoff,
    SysadminHandoff,
    UIDesignerHandoff,
    UXDesignerHandoff,
    ValidatorHandoff,
)

SCHEMAS = {
    "researcher": ResearcherHandoff,
    "architect": ArchitectHandoff,
    "implementer": ImplementerHandoff,
    "reviewer": ReviewerHandoff,
    "validator": ValidatorHandoff,
    "ui-designer": UIDesignerHandoff,
    "ux-designer": UXDesignerHandoff,
    "cost-accountant": CostAccountantHandoff,
    "sre": SREHandoff,
    "sysadmin": SysadminHandoff,
    "claude-ai-specialist": ClaudeAISpecialistHandoff,
    "language-specialist": LanguageSpecialistHandoff,
}


def export_schemas(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, model in SCHEMAS.items():
        schema = model.model_json_schema()
        path = output_dir / f"{name}.schema.json"
        path.write_text(json.dumps(schema, indent=2) + "\n")
        print(f"  {path}")


if __name__ == "__main__":
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("src/schemas/json")
    print("Exporting agent schemas:")
    export_schemas(out)
    print(f"Done. {len(SCHEMAS)} schemas exported.")
