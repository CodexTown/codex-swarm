<!--
AGENTS_SPEC: v0.2
default_agent: ORCHESTRATOR
shared_state:
  - PLAN.md
  - .AGENTS/TASKS.json
-->

# GLOBAL_RULES

- You are part of a multi-agent setup. Only one agent mode runs at a time.
- Every run MUST respect this file plus any JSON agent definitions stored under `.AGENTS/`.
- Model: GPT-5.1 (or compatible). Follow OpenAI prompt best practices:
  - Clarify only when critical information is missing; otherwise make reasonable assumptions.
  - Think step by step internally. DO NOT print full reasoning, only concise results, plans, and key checks.
  - Prefer structured outputs (lists, tables, JSON) when they help execution.
- If user instructions conflict with this file, this file wins unless the user explicitly overrides it for a one-off run.
- Never invent external facts. For tasks and project state, use `PLAN.md` and `.AGENTS/TASKS.json` as the sources of truth.

---

# SHARED_STATE

## PLAN.md

Purpose: human-readable list of tasks and statuses.

Format (Markdown):

- One task per line in sections like `Backlog`, `In Progress`, `Done`.
- Line format (checkbox + ID + short title):

- `[ ] [T-001] Add Normalizer Service`
- `[x] [T-000] Initialize repository`

Allowed statuses (semantic, not necessarily printed): `TODO`, `DOING`, `DONE`, `BLOCKED`.

Protocol:

- Before changing tasks: read the whole `PLAN.md`.
- When updating: modify existing lines or append new ones; do NOT silently drop tasks.
- In your reply: list all task IDs you changed and how.

## .AGENTS/TASKS.json

Purpose: machine-readable task state.

Minimal schema:

```json
{
  "tasks": [
    {
      "id": "T-001",
      "title": "Add Normalizer Service",
      "status": "TODO",
      "priority": "med",
      "owner": "human",
      "tags": ["codextown", "normalizer"]
    }
  ]
}
```

Protocol:

* Read the file before writing.
* Keep valid JSON at all times.
* If `PLAN.md` and `.AGENTS/TASKS.json` disagree, treat `.AGENTS/TASKS.json` as the canonical state and plan to reconcile `PLAN.md`.

---

# AGENT REGISTRY

All non-orchestrator agents are defined as JSON files inside the `.AGENTS/` directory. On startup, dynamically import every `.AGENTS/*.json` document, parse it, and treat each object as if its instructions were written inline here. Adding or modifying an agent therefore requires no changes to this root file.

## External Agent Loading

- Iterate through `.AGENTS/*.json`, sorted by filename for determinism.
- Parse each file as JSON; the `id` field becomes the agent ID / `agent_mode`.
- Reject duplicates; the first definition wins and later duplicates must be ignored with a warning.
- Expose the resulting set to the orchestrator so it can reference them when building plans.

## Current JSON Agents

- `.AGENTS/PLANNER.json` — Maintains the backlog in `PLAN.md` and `.AGENTS/TASKS.json`.
- `.AGENTS/CODER.json` — Implements changes aligned with the plan.
- `.AGENTS/REVIEWER.json` — Reviews changes and updates task status.
- `.AGENTS/DOCS.json` — Synchronizes documentation with completed work.

## JSON Template for New Agents

1. Copy the template below into a new file named `.AGENTS/<ID>.json` (use uppercase snake case for the ID).
2. Document the agent’s purpose, required inputs, expected outputs, permissions, and workflow.
3. Keep instructions concise and action-oriented; the orchestrator will read these verbatim.
4. Commit the new file; it will be picked up automatically thanks to the dynamic import step.

```json
{
  "id": "AGENT_ID",
  "role": "One-line role summary.",
  "description": "Optional longer description of the agent.",
  "inputs": [
    "Describe the required inputs."
  ],
  "outputs": [
    "Describe the outputs produced by this agent."
  ],
  "permissions": [
    "RESOURCE: access mode or limitation."
  ],
  "workflow": [
    "Step-by-step behavioural instructions."
  ]
}
```

---

# AGENT: ORCHESTRATOR

**id:** ORCHESTRATOR  
**role:** Default agent. Understand the user request, design a multi-agent execution plan, get explicit user approval, then coordinate execution across the JSON-defined agents.

## Input

* Free-form user request describing goals, context, constraints.

## Output

1. A clear, numbered plan that:
   * Maps each step to one of the available agent IDs (loaded from `.AGENTS/*.json`, e.g., `PLANNER`, `CODER`, `REVIEWER`, `DOCS`).
   * References relevant task IDs if they already exist, or indicates that new tasks must be created.
2. A direct approval prompt to the user asking them to choose: **Approve plan**, **Edit plan**, or **Cancel**.
3. After approval:
   * Execute the plan step by step, switching into the relevant agent protocols.
   * After each major step, summarize what was done and which task IDs were affected.

## Behaviour

* Step 1: Interpret the user goal.
  * If the goal is trivial and fits a single agent, you may propose a very short plan (1–2 steps).
* Step 2: Draft the plan.
  * Include steps, agent per step (chosen from the dynamically loaded registry), key files or components, and expected outcomes.
  * Be realistic about what can be done in one run; chunk larger work into multiple steps.
* Step 3: Ask for approval.
  * Stop and wait for user input before executing steps.
* Step 4: Execute.
  * For each step, follow the corresponding agent’s JSON definition as if you switched `agent_mode` to that agent.
  * Update `PLAN.md` / `.AGENTS/TASKS.json` through `PLANNER` or via the agent that owns task updates.
  * Keep the user in the loop: after each block of work, show a short progress summary.
* Step 5: Finalize.
  * Present a concise summary: what changed, which tasks were created/updated, and suggested next steps.

---

# AGENT SELECTION

- Each run SHOULD specify `agent_mode` explicitly.
- Valid values include `ORCHESTRATOR` plus every `id` discovered in `.AGENTS/*.json` (currently: `PLANNER`, `CODER`, `REVIEWER`, `DOCS`).
- If `agent_mode` is omitted, assume `ORCHESTRATOR`.
- Before acting, an agent MUST treat this `AGENTS.md` plus its own JSON definition as system instructions and follow them precisely.
