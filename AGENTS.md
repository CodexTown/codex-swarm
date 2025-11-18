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
- The workspace is always a git repository. After completing each atomic task from `PLAN.md`, create a concise, human-readable commit before continuing.

---

# COMMIT_WORKFLOW

- Treat each plan task (`T-###`) as an atomic unit of work that must end with its own git commit.
- Commit messages must stay short, human friendly, and include the relevant task ID when possible.
- Agents responsible for editing files (typically `CODER` and `DOCS`) stage and commit their changes before handing control back to the orchestrator.
- The ORCHESTRATOR must not advance to the next plan step until the previous step’s commit is recorded.
- Each step summary should mention the new commit hash so every change is traceable from the conversation log.
- Before switching agents, ensure `git status --short` is clean (no stray changes) other than files intentionally ignored.

## Commit Message Patterns

- **Planning commits (PLANNER)** — When opening or reshaping tasks, use messages like `Plan T-010 data cleanup tasks` so the log makes it obvious which IDs entered the backlog.
- **Implementation commits (CODER)** — Describe the delivered change while naming every task, e.g., `Implement T-007 commit policy updates`.
- **Documentation commits (DOCS)** — Tie the docs change to the task and audience, such as `Docs T-008 describe repo layout`.
- **Review/closure commits (REVIEWER)** — When marking work DONE or BLOCKED without code edits, prefer messages like `Review T-007 completed` to clarify intent.
- If one commit spans multiple IDs, list them all (`Finish T-007/T-008 release tweaks`). Avoid vague phrases like “misc fixes”.

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

### Status Transition Protocol

- **Create / Reprioritize (PLANNER only).** PLANNER is the sole writer of new tasks and the only agent that may change priorities or mark work as `BLOCKED`; when blocking a task it must capture the reason in both files.
- **Start Work (CODER or DOCS).** The agent assuming ownership flips the task to `DOING` in both trackers before editing files, signaling that the work is in progress.
- **Complete Work (REVIEWER or DOCS).** REVIEWER marks tasks `DONE` after validating the deliverable. DOCS may mark doc-only tasks as `DONE` when no code change occurred; otherwise they request REVIEWER sign-off.
- **Status Sync.** Every transition must be mirrored in `PLAN.md` and `.AGENTS/TASKS.json` within the same commit, referencing the affected task IDs in the message. If a discrepancy is detected, pause and reconcile before continuing.
- **Escalations.** Agents lacking permission for a desired transition must request PLANNER or REVIEWER involvement rather than editing statuses directly.

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

- The orchestrator regenerates this list at startup by scanning `.AGENTS/*.json`, sorting the filenames alphabetically, and rendering the role summary from each file. Manual edits are discouraged because the list is derived data.
- Whenever CREATOR introduces a new agent, it writes the JSON file, ensures the filename fits the alphabetical order (uppercase snake case), and reruns the generation step so the registry reflects the latest roster automatically.
- If a new agent requires additional documentation, CREATOR adds any necessary narrative in the “On-Demand Agent Creation” section, but the current-agent list itself is always produced from the filesystem scan.

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

## On-Demand Agent Creation

- When the PLANNER determines that no existing agent can fulfill a plan step, it must schedule the `CREATOR` agent and provide the desired skill set, constraints, and target deliverables.
- `CREATOR` assumes the mindset of a subject-matter expert in the requested specialty, drafts precise instructions, and outputs a new `.AGENTS/<ID>.json` following the template above.
- After writing the file, CREATOR triggers the automatic registry refresh (filesystem scan) so the “Current JSON Agents” list immediately includes the new entry without any manual editing.
- CREATOR stages and commits the new agent plus any supporting docs with the relevant task ID, enabling the orchestrator to reuse the updated roster in the next planning cycle.

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
  * Ensure the acting agent stages and commits its changes with a concise message (including task IDs) before proceeding to the next plan step, then confirm the working tree is clean and report the commit hash in the progress summary.
  * Keep the user in the loop: after each block of work, show a short progress summary.
* Step 5: Finalize.
  * Present a concise summary: what changed, which tasks were created/updated, and suggested next steps.

---

# AGENT SELECTION

- Each run SHOULD specify `agent_mode` explicitly.
- Valid values include `ORCHESTRATOR` plus every `id` discovered in `.AGENTS/*.json` (currently: `PLANNER`, `CODER`, `REVIEWER`, `DOCS`, `CREATOR`).
- If `agent_mode` is omitted, assume `ORCHESTRATOR`.
- Before acting, an agent MUST treat this `AGENTS.md` plus its own JSON definition as system instructions and follow them precisely.
