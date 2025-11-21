#!/usr/bin/env python3
"""Render tasks.md from the canonical tasks.json file."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent
TASKS_PATH = ROOT / "tasks.json"
OUTPUT_PATH = ROOT / "tasks.md"

STATUS_SECTIONS = [
    ("TODO", "Backlog", "_No open tasks._"),
    ("DOING", "In Progress", "_No active tasks._"),
    ("BLOCKED", "Blocked", "_No blocked tasks._"),
    ("DONE", "Done", "_No completed tasks yet._"),
]

STATUS_SYMBOLS = {
    "TODO": "[ ]",
    "DOING": "[~]",
    "BLOCKED": "[-]",
    "DONE": "[x]",
}


def load_tasks() -> List[Dict]:
    with TASKS_PATH.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list):
        raise ValueError("tasks.json must contain a top-level 'tasks' list")
    return sorted(tasks, key=lambda task: task.get("id", ""))


def format_metadata(task: Dict) -> str:
    priority = task.get("priority", "-")
    owner = task.get("owner", "-")
    tags = task.get("tags") or []
    tags_text = ", ".join(tags) if tags else "—"
    return f"Priority: {priority} | Owner: {owner} | Tags: {tags_text}"


def format_description(task: Dict) -> str:
    description = (task.get("description") or "").strip()
    return description if description else "No description provided."


def format_comments(task: Dict) -> List[str]:
    comments = task.get("comments") or []
    formatted: List[str] = []
    for comment in comments:
        if not isinstance(comment, dict):
            continue
        author = comment.get("author", "unknown") or "unknown"
        body = (comment.get("body") or "").strip()
        body = body if body else "(no additional details)"
        formatted.append(f"    - **{author}:** {body}")
    if not formatted:
        formatted.append("    - _No comments yet._")
    return formatted


def build_section(tasks: List[Dict], status: str, heading: str, empty_text: str) -> List[str]:
    block: List[str] = [f"## {heading}"]
    section_tasks = [task for task in tasks if task.get("status") == status]
    if not section_tasks:
        block.append(empty_text)
        return block
    for task in section_tasks:
        symbol = STATUS_SYMBOLS.get(status, "[?]")
        task_id = task.get("id", "<no-id>")
        title = task.get("title", "(untitled task)")
        block.append(f"- {symbol} [{task_id}] {title}")
        block.append(f"  - {format_metadata(task)}")
        block.append(f"  - Description: {format_description(task)}")
        block.append("  - Comments:")
        block.extend(format_comments(task))
        block.append("")
    if block[-1] == "":
        block.pop()
    return block


def main() -> None:
    tasks = load_tasks()
    counts: Dict[str, int] = {status: 0 for status, *_ in STATUS_SECTIONS}
    for task in tasks:
        status = task.get("status")
        if status in counts:
            counts[status] += 1
    total_tasks = len(tasks)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines: List[str] = ["# Project Tasks", "", f"_Last updated: {now}_", "", "## Summary"]
    lines.append(f"- Total tasks: {total_tasks}")
    for status, heading, _ in STATUS_SECTIONS:
        label = heading
        lines.append(f"- {label}: {counts.get(status, 0)}")
    lines.append("")

    for status, heading, empty_text in STATUS_SECTIONS:
        lines.extend(build_section(tasks, status, heading, empty_text))
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()
    lines.append("")

    OUTPUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} with {total_tasks} tasks.")


if __name__ == "__main__":
    main()
