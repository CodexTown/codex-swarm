# Workflow Review (T-011)

## Current Flow Snapshot

- **Single-orchestrator entry point.** `AGENTS.md` centralizes all global rules and forces every session to start in `ORCHESTRATOR` mode before dispatching specialized agents (`AGENTS.md:9-197`).
- **Strict commit-per-task policy.** Each task in `PLAN.md` must land as its own commit and the orchestrator pauses until that commit exists (`AGENTS.md:23-38`).
- **Dual task sources of truth.** Humans rely on `PLAN.md` while automation consumes `.AGENTS/TASKS.json`; discrepancies must always be reconciled manually (`AGENTS.md:42-94`).
- **Status lifecycle.** Tasks transition through TODO → DOING → DONE/Blocked, with CODER or DOCS expected to flip to DOING and REVIEWER/DOCS handling completion (`AGENTS.md:50-65`).

## Improvement Opportunities

### 1. Align status responsibilities with agent permissions

- The status protocol assigns CODER/DOCS to start work by setting DOING and lets DOCS close doc-only items (`AGENTS.md:58-64`), yet both `.AGENTS/CODER.json:15-17` and `.AGENTS/DOCS.json:13-17` only grant read access to `PLAN.md` / `.AGENTS/TASKS.json`.
- Result: the orchestrator or REVIEWER must edit status files on their behalf, which is slow and contradicts the stated workflow.
- **Optimizations:**
  - Expand CODER/DOCS permissions to "read + write" for both files, and explicitly document when they may update statuses (e.g., CODER → DOING, DOCS → DOING/DONE for doc tasks).
  - Alternatively, introduce a lightweight `STATUS` agent empowered to perform transitions when CODER/DOCS request them, clarifying the handshake.
  - Mirror the change in `AGENTS.md` so the responsibility matrix is unambiguous for every session.

### 2. Automate PLAN.md ↔ .AGENTS/TASKS.json synchronization

- Agents are told to keep the Markdown and JSON views in lockstep (`AGENTS.md:42-94`), but the repo lacks tooling to detect drift. Any typo (e.g., forgetting to move a task from Backlog to In Progress) silently violates the rules.
- **Optimizations:**
  - Add a maintenance script (e.g., `scripts/check_task_sync.py`) that parses both files and fails when IDs, statuses, or titles diverge.
  - Wire the script into a pre-commit hook or lightweight CI step so contributors get immediate feedback instead of discovering inconsistencies mid-run.
  - Consider making `PLAN.md` generated from `.AGENTS/TASKS.json`; PLANNER would then update only the JSON, and a command would regenerate the Markdown view, eliminating manual duplication.

### 3. Provide a standard deliverable path for research tasks

- The commit policy mandates "one commit per plan task" regardless of whether work happens in code (`AGENTS.md:23-38`). Analytical or planning tasks (like this one) typically have no natural file to change, forcing contributors to invent ad-hoc documents just to satisfy the commit requirement.
- **Optimizations:**
  - Establish a canonical `notes/` or `reports/` directory with a template (summary, findings, next steps) that agents can drop analysis into without debating file names.
  - Allow PLAN tasks tagged as `analysis` to attach their findings directly in the conversation log, with REVIEWER recording completion via a lightweight metadata file if no persistent artifact is needed.
  - Document these options in `AGENTS.md` so future analytical tasks have a predictable flow and do not block on artificial file creation.

### 4. Normalize the PLAN.md layout for In-Progress work

- The specification references "sections like Backlog, In Progress, Done" (`AGENTS.md:50-55`), yet the shipped `PLAN.md` only listed Backlog and Done, so DOING items still appeared in Backlog before this review.
- **Optimizations:**
  - Provide a starter `PLAN.md` template (perhaps stored under `.AGENTS/templates/plan.md`) that always includes Backlog, In Progress, Done, and Blocked headers with placeholder text.
  - Add a lint check (similar to opportunity #2) ensuring DOING tasks sit under the In Progress header, preventing regressions.
  - Mention the expected section structure in the PLANNER workflow so new tasks automatically land in the right bucket.

## Next Steps

1. Decide whether CODER/DOCS should be empowered to update statuses directly or if a dedicated status agent makes more sense; document the outcome in both the JSON files and `AGENTS.md`.
2. Prioritize building the sync/lint script because it unlocks safer commits for every other improvement.
3. Create the reusable analysis/notes template so future research tasks follow a consistent pattern without extra orchestration overhead.
