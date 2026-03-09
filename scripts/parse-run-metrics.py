#!/usr/bin/env python3
"""Parse a Claude Code JSONL session log and extract agent performance metrics.

Usage:
    python scripts/parse-run-metrics.py <session.jsonl>
    python scripts/parse-run-metrics.py latest                    # most recent JSONL across all projects
    python scripts/parse-run-metrics.py latest --project greenlake # most recent JSONL matching 'greenlake'

Output: Markdown metrics table to stdout, suitable for pasting into a review doc.
"""

import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


def find_latest_jsonl(project_filter: str | None = None) -> Path:
    """Find the most recently modified JSONL in the Claude projects directory.

    Args:
        project_filter: Optional substring to match against the JSONL's parent
            directory name (e.g., 'greenlake' or 'blind-roll'). This filters
            to a specific project's session logs.
    """
    projects_dir = Path.home() / ".claude" / "projects"
    jsonls = sorted(projects_dir.rglob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if project_filter:
        jsonls = [p for p in jsonls if project_filter in p.parent.name]
    if not jsonls:
        msg = "No JSONL files found"
        if project_filter:
            msg += f" matching project filter '{project_filter}'"
        print(msg, file=sys.stderr)
        sys.exit(1)
    return jsonls[0]


def parse_messages(path: Path) -> list[dict]:
    """Parse JSONL file into list of message objects."""
    messages = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                messages.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return messages


def parse_ts(ts: str) -> datetime | None:
    """Parse ISO 8601 timestamp."""
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def build_agent_timeline(messages: list[dict]) -> list[dict]:
    """Build a timeline of agent dispatch/result events using temporal overlap detection.

    Claude Code dispatches agents as separate messages but runs them concurrently.
    We detect parallelism by checking if an agent was dispatched before a previously
    dispatched agent's result came back.
    """
    # Collect agent dispatch tool_use IDs and descriptions
    agent_info: dict[str, dict] = {}  # tool_use_id -> {description, subagent_type, ...}

    for obj in messages:
        msg = obj.get("message", {})
        role = msg.get("role", "")
        content = msg.get("content", [])
        ts = obj.get("timestamp", "")

        if role == "assistant" and isinstance(content, list):
            for block in content:
                if (isinstance(block, dict)
                        and block.get("type") == "tool_use"
                        and block.get("name") == "Agent"):
                    tid = block.get("id", "")
                    inp = block.get("input", {})
                    agent_info[tid] = {
                        "description": inp.get("description", ""),
                        "subagent_type": inp.get("subagent_type", ""),
                        "background": inp.get("run_in_background", False),
                        "prompt_len": len(str(inp.get("prompt", ""))),
                        "dispatch_ts": ts,
                        "result_ts": None,
                    }

    # Find result timestamps (tool_result blocks in user messages)
    for obj in messages:
        msg = obj.get("message", {})
        role = msg.get("role", "")
        content = msg.get("content", [])
        ts = obj.get("timestamp", "")

        if role == "user" and isinstance(content, list):
            for block in content:
                if (isinstance(block, dict)
                        and block.get("type") == "tool_result"
                        and block.get("tool_use_id", "") in agent_info):
                    agent_info[block["tool_use_id"]]["result_ts"] = ts

    return list(agent_info.values())


def detect_parallel_batches(timeline: list[dict]) -> list[list[dict]]:
    """Group agents into concurrent batches based on temporal overlap.

    An agent is in the same batch as the previous one if it was dispatched
    before any currently-running agent returned its result.
    """
    if not timeline:
        return []

    # Sort by dispatch time
    sorted_agents = sorted(timeline, key=lambda a: a["dispatch_ts"])

    batches: list[list[dict]] = []
    current_batch: list[dict] = [sorted_agents[0]]

    for agent in sorted_agents[1:]:
        dispatch_dt = parse_ts(agent["dispatch_ts"])
        if dispatch_dt is None:
            current_batch.append(agent)
            continue

        # Check if this dispatch overlaps with any agent in the current batch
        # (dispatched before any current batch member returned)
        overlaps = False
        for running in current_batch:
            result_dt = parse_ts(running["result_ts"]) if running["result_ts"] else None
            if result_dt is None or dispatch_dt < result_dt:
                overlaps = True
                break

        if overlaps:
            current_batch.append(agent)
        else:
            batches.append(current_batch)
            current_batch = [agent]

    batches.append(current_batch)
    return batches


IDLE_THRESHOLD = 120  # seconds — gaps longer than this are considered user idle time


def extract_metrics(messages: list[dict]) -> dict:
    """Extract all performance metrics from parsed messages."""
    tool_calls: list[dict] = []
    read_paths: list[str] = []
    timestamps: list[str] = []
    token_usage = {"input": 0, "output": 0, "cache_create": 0, "cache_read": 0}

    for obj in messages:
        ts = obj.get("timestamp", "")
        if ts:
            timestamps.append(ts)

        msg = obj.get("message", {})
        role = msg.get("role", "")
        content = msg.get("content", [])
        usage = msg.get("usage", {})

        if usage and role == "assistant":
            token_usage["input"] += usage.get("input_tokens", 0)
            token_usage["output"] += usage.get("output_tokens", 0)
            token_usage["cache_create"] += usage.get("cache_creation_input_tokens", 0)
            token_usage["cache_read"] += usage.get("cache_read_input_tokens", 0)

        if role == "assistant" and isinstance(content, list):
            for block in content:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                name = block.get("name", "")
                inp = block.get("input", {})
                tool_calls.append({"name": name, "input": inp})

                if name == "Read":
                    read_paths.append(inp.get("file_path", ""))

    # Build agent timeline and detect parallelism
    timeline = build_agent_timeline(messages)
    batches = detect_parallel_batches(timeline)

    total_agents = len(timeline)
    parallel_batches = [b for b in batches if len(b) > 1]
    sequential_batches = [b for b in batches if len(b) == 1]
    parallel_agents = sum(len(b) for b in parallel_batches)
    sequential_agents = sum(len(b) for b in sequential_batches)
    background_agents = sum(1 for a in timeline if a["background"])

    # Compute read metrics
    read_counter = Counter(read_paths)
    total_reads = len(read_paths)
    unique_reads = len(read_counter)
    duplicate_reads = total_reads - unique_reads
    duplicated_files = {f: c for f, c in read_counter.items() if c > 1}

    # Compute tool frequency
    tool_freq = Counter(tc["name"] for tc in tool_calls)

    # Compute wall clock: session duration and lead active time
    wall_clock_seconds = None
    lead_active_seconds = None
    idle_gaps: list[dict] = []
    if len(timestamps) >= 2:
        t0 = parse_ts(timestamps[0])
        t1 = parse_ts(timestamps[-1])
        if t0 and t1:
            wall_clock_seconds = (t1 - t0).total_seconds()

        # Compute lead active time by subtracting idle gaps.
        # An idle gap is a period between consecutive assistant tool_calls
        # (or tool_results) where nothing happens for > IDLE_THRESHOLD seconds.
        # This filters out user think time, AFK time, etc.
        parsed_ts = [parse_ts(t) for t in timestamps]
        valid_ts = [t for t in parsed_ts if t is not None]
        if len(valid_ts) >= 2:
            total_idle = 0.0
            for i in range(1, len(valid_ts)):
                gap = (valid_ts[i] - valid_ts[i - 1]).total_seconds()
                if gap > IDLE_THRESHOLD:
                    idle_gaps.append({
                        "start": valid_ts[i - 1].isoformat(),
                        "end": valid_ts[i].isoformat(),
                        "duration_s": gap,
                    })
                    total_idle += gap
            lead_active_seconds = wall_clock_seconds - total_idle if wall_clock_seconds else None

    return {
        "total_agents": total_agents,
        "parallel_agents": parallel_agents,
        "sequential_agents": sequential_agents,
        "parallel_batches_count": len(parallel_batches),
        "background_agents": background_agents,
        "timeline": timeline,
        "batches": batches,
        "total_reads": total_reads,
        "unique_reads": unique_reads,
        "duplicate_reads": duplicate_reads,
        "duplicated_files": duplicated_files,
        "tool_freq": tool_freq,
        "token_usage": token_usage,
        "wall_clock_seconds": wall_clock_seconds,
        "lead_active_seconds": lead_active_seconds,
        "idle_gaps": idle_gaps,
        "total_messages": len(messages),
        "timestamps": (timestamps[0] if timestamps else "", timestamps[-1] if timestamps else ""),
    }


def format_report(metrics: dict, path: Path) -> str:
    """Format metrics as a markdown report."""
    m = metrics
    total = m["total_agents"]
    parallel_rate = (m["parallel_agents"] / total * 100) if total else 0
    dup_rate = (m["duplicate_reads"] / m["total_reads"] * 100) if m["total_reads"] else 0
    session_min = f"~{m['wall_clock_seconds'] / 60:.1f} min" if m["wall_clock_seconds"] else "unknown"
    active_min = f"~{m['lead_active_seconds'] / 60:.1f} min" if m["lead_active_seconds"] else "unknown"
    total_tokens = m["token_usage"]["input"] + m["token_usage"]["output"]

    lines = [
        "# Run Metrics (JSONL ground truth)",
        "",
        f"**Source**: `{path}`",
        f"**Period**: {m['timestamps'][0]} to {m['timestamps'][1]}",
        f"**Messages**: {m['total_messages']}",
        "",
        "## Dispatch Metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Dispatches (total) | {total} |",
        f"| Dispatches (parallel) | {m['parallel_agents']} ({m['parallel_batches_count']} batches) |",
        f"| Dispatches (sequential) | {m['sequential_agents']} |",
        f"| Dispatches (background) | {m['background_agents']} |",
        f"| **Parallel dispatch rate** | **{parallel_rate:.0f}%** |",
        "",
    ]

    if m["timeline"]:
        lines += [
            "### Agent Dispatch Detail",
            "",
            "| # | Description | Type | Background | Prompt Size |",
            "|---|-------------|------|------------|-------------|",
        ]
        for i, a in enumerate(sorted(m["timeline"], key=lambda x: x["dispatch_ts"]), 1):
            bg = "yes" if a["background"] else "no"
            lines.append(
                f"| {i} | {a['description']} | {a['subagent_type']} | {bg} | {a['prompt_len']} chars |"
            )

        lines += [
            "",
            "### Concurrent Batches (detected by temporal overlap)",
            "",
        ]
        for i, batch in enumerate(m["batches"], 1):
            label = f"PARALLEL ({len(batch)} agents)" if len(batch) > 1 else "sequential (1 agent)"
            lines.append(f"**Batch {i}** [{label}]:")
            for a in sorted(batch, key=lambda x: x["dispatch_ts"]):
                d_time = a["dispatch_ts"].split("T")[1][:12] if "T" in a["dispatch_ts"] else "?"
                r_time = "?"
                if a["result_ts"] and "T" in a["result_ts"]:
                    r_time = a["result_ts"].split("T")[1][:12]
                lines.append(f"- {a['description']} (dispatched {d_time}, returned {r_time})")
            lines.append("")

    # Timeline
    if m["timeline"]:
        events = []
        for a in m["timeline"]:
            events.append((a["dispatch_ts"], "DISPATCH", a["description"]))
            if a["result_ts"]:
                events.append((a["result_ts"], "RESULT", a["description"]))
        events.sort(key=lambda x: x[0])

        lines += [
            "### Timeline",
            "",
            "| Time | Event | Agent |",
            "|------|-------|-------|",
        ]
        for ts, etype, desc in events:
            t = ts.split("T")[1][:12] if "T" in ts else ts
            lines.append(f"| {t} | {etype} | {desc} |")
        lines.append("")

    lines += [
        "## Read Metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Reads (total, lead only) | {m['total_reads']} |",
        f"| Reads (unique files) | {m['unique_reads']} |",
        f"| Reads (duplicate) | {m['duplicate_reads']} |",
        f"| **Duplicate read rate** | **{dup_rate:.0f}%** |",
        "",
    ]

    if m["duplicated_files"]:
        lines += [
            "### Duplicated Files",
            "",
            "| File | Times Read |",
            "|------|-----------|",
        ]
        for f, c in sorted(m["duplicated_files"].items(), key=lambda x: -x[1]):
            short = f.split("/")[-1]
            lines.append(f"| `{short}` | {c} |")
        lines.append("")

    lines += [
        "## Token Usage (lead only)",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Input tokens | {m['token_usage']['input']:,} |",
        f"| Output tokens | {m['token_usage']['output']:,} |",
        f"| Cache creation | {m['token_usage']['cache_create']:,} |",
        f"| Cache read | {m['token_usage']['cache_read']:,} |",
        f"| **Total (input+output)** | **{total_tokens:,}** |",
        "",
        "## Tool Usage",
        "",
        "| Tool | Calls |",
        "|------|-------|",
    ]
    for tool, count in m["tool_freq"].most_common():
        lines.append(f"| {tool} | {count} |")

    # Idle gaps section (if any)
    if m["idle_gaps"]:
        lines += [
            "",
            "## Idle Gaps (excluded from lead active time)",
            "",
            f"Threshold: >{IDLE_THRESHOLD}s between messages.",
            "",
            "| Start | End | Duration |",
            "|-------|-----|----------|",
        ]
        for gap in m["idle_gaps"]:
            start = gap["start"].split("T")[1][:8] if "T" in gap["start"] else gap["start"]
            end = gap["end"].split("T")[1][:8] if "T" in gap["end"] else gap["end"]
            dur_min = gap["duration_s"] / 60
            lines.append(f"| {start} | {end} | {dur_min:.1f} min |")
        lines.append("")

    lines += [
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Parallel dispatch rate | {parallel_rate:.0f}% |",
        f"| Duplicate read rate | {dup_rate:.0f}% |",
        f"| Total tokens (lead) | {total_tokens:,} |",
        f"| Lead active time | {active_min} |",
        f"| Session duration | {session_min} |",
    ]

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    arg = sys.argv[1]
    project_filter = None
    if "--project" in sys.argv:
        idx = sys.argv.index("--project")
        if idx + 1 < len(sys.argv):
            project_filter = sys.argv[idx + 1]

    if arg == "latest":
        path = find_latest_jsonl(project_filter)
        print(f"Using: {path}", file=sys.stderr)
    else:
        path = Path(arg)

    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        sys.exit(1)

    messages = parse_messages(path)
    metrics = extract_metrics(messages)
    report = format_report(metrics, path)
    print(report)


if __name__ == "__main__":
    main()
