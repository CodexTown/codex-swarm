# Codex Agents Swarm

Codex Agents Swarm is a lightweight framework that bridges the OpenAI Codex Plugin with any IDE where the plugin is installed. It treats the IDE session as a cooperative multi-agent workspace, allowing you to orchestrate specialized agents that collaborate on tasks ranging from software development to documentation, planning, or research.

## How It Works

1. **Orchestrator-focused contract.** `AGENTS.md` defines only the global rules, shared state, and the ORCHESTRATOR agent. The orchestrator interprets the user’s goal, drafts a plan, requests approval, and delegates work to other agents.
2. **External agent registry.** Every non-orchestrator agent lives in `.AGENTS/<ID>.json`. When the IDE loads this repository, it dynamically imports each JSON document and registers the agent ID, role, permissions, and workflow.
3. **Shared task state.** Human-readable plans live in `PLAN.md`, while machine-readable progress stays in `.AGENTS/TASKS.json`. This separation lets agents communicate status updates reliably no matter which IDE they run in.
4. **Plugin-agnostic operation.** Because the instructions are plain Markdown and JSON, any IDE that supports the Codex Plugin can execute the same flows without extra configuration.

## Repository Layout

```
.
├── AGENTS.md
├── LICENSE
├── PLAN.md
├── README.md
└── .AGENTS/
    ├── PLANNER.json
    ├── CODER.json
    ├── REVIEWER.json
    ├── DOCS.json
    ├── CREATOR.json
    └── TASKS.json
```

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Global rules, commit workflow, and the ORCHESTRATOR specification (plus the JSON template for new agents). |
| `.AGENTS/PLANNER.json` | Defines how tasks are added/updated across `PLAN.md` and `.AGENTS/TASKS.json`. |
| `.AGENTS/CODER.json` | Implementation specialist responsible for code or config edits tied to task IDs. |
| `.AGENTS/REVIEWER.json` | Performs reviews, verifies work, and flips task statuses accordingly. |
| `.AGENTS/DOCS.json` | Keeps README and other docs synchronized with recently completed work. |
| `.AGENTS/CREATOR.json` | On-demand agent factory that writes new JSON agents plus registry updates. |
| `.AGENTS/TASKS.json` | Machine-readable backlog mirror; canonical when discrepancies appear. |
| `PLAN.md` | Human-readable backlog shared in the conversation (Backlog / Done sections). |
| `README.md` | High-level overview and onboarding material for the repository. |
| `LICENSE` | MIT License for the project. |

## Agent Lifecycle

1. **Planning:** The ORCHESTRATOR reads `AGENTS.md`, loads `.AGENTS/*.json`, and creates a plan that maps each step to a registered agent (e.g., PLANNER, CODER, REVIEWER, DOCS).
2. **Approval:** The user can approve, edit, or cancel the plan before any work starts.
3. **Execution:** The orchestrator switches `agent_mode` according to the plan, allowing each agent to follow its JSON-defined workflow inside the IDE.
4. **Progress tracking:** Agents update `PLAN.md` and `.AGENTS/TASKS.json` according to their permissions, ensuring both humans and tools can see the current state.

This structure lets you string together arbitrary workflows such as code implementation, documentation refreshes, research digests, or task triage—all from the same IDE session.

## Commit Workflow

- The workspace is always a git repository, so every meaningful change must land in version control.
- Each atomic task listed in `PLAN.md` maps to exactly one commit with a concise, human-readable message (ideally referencing the task ID).
- The agent that performs the work stages and commits before handing control back to the orchestrator, and the orchestrator pauses the plan until that commit exists.
- Step summaries mention the new commit hash and confirm the working tree is clean so humans can audit progress directly from the conversation.
- If a plan step produces no file changes, call that out explicitly; otherwise the swarm must not proceed without a commit.

## Shared State Details

- **`PLAN.md`**: Markdown checklist intended for humans. It lists tasks with IDs, sections (Backlog, In Progress, Done), and checkbox status. Agents always read it fully before editing, and every completed entry immediately gets an indented `Review:` line that summarizes (in one or two sentences) what changed and why.
- **`.AGENTS/TASKS.json`**: Machine-focused mirror of the plan with strict JSON schema so agents can parse, filter, and update state deterministically. When discrepancies occur, `.AGENTS/TASKS.json` is the canonical source and `PLAN.md` must be reconciled.

## Adding a New Agent

1. Duplicate the template defined in `AGENTS.md` under “JSON Template for New Agents”.
2. Save the file as `.AGENTS/<AGENT_ID>.json` using an uppercase ID (e.g., `RESEARCHER.json`).
3. Fill in the `role`, `description`, `inputs`, `outputs`, `permissions`, and ordered `workflow` steps that describe exactly how the agent should behave.
4. Commit the file; on the next run the orchestrator will automatically load and expose the new agent.

Because every agent is pure JSON, you can extend the swarm with domain experts for QA, marketing, technical writing, data wrangling, or any other process you want to automate in your IDE.

## Extending Beyond Development

While Codex Agents Swarm is comfortable implementing code, nothing restricts agents to development tasks. By defining workflows in JSON you can build:

- Research agents that summarize documentation before coding begins.
- Compliance reviewers that check commits for policy violations.
- Operational runbooks that coordinate deployments or incident response.
- Documentation bots that keep changelogs and READMEs in sync.

If the OpenAI Codex Plugin can access the repository from your IDE, it can orchestrate these agents using the same framework.
