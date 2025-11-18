# Codex Agents Swarm

Codex Agents Swarm is a lightweight framework that bridges the OpenAI Codex Plugin with any IDE where the plugin is installed. It treats the IDE session as a cooperative multi-agent workspace, allowing you to orchestrate specialized agents that collaborate on tasks ranging from software development to documentation, planning, or research.

## How It Works

1. **Orchestrator-focused contract.** `AGENTS.md` defines only the global rules, shared state, and the ORCHESTRATOR agent. The orchestrator interprets the user’s goal, drafts a plan, requests approval, and delegates work to other agents.
2. **External agent registry.** Every non-orchestrator agent lives in `.AGENTS/<ID>.json`. When the IDE loads this repository, it dynamically imports each JSON document and registers the agent ID, role, permissions, and workflow.
3. **Shared task state.** Human-readable plans live in `PLAN.md`, while machine-readable progress stays in `.AGENTS/TASKS.json`. This separation lets agents communicate status updates reliably no matter which IDE they run in.
4. **Plugin-agnostic operation.** Because the instructions are plain Markdown and JSON, any IDE that supports the Codex Plugin can execute the same flows without extra configuration.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `AGENTS.md` | Global rules and the ORCHESTRATOR specification, including the JSON template for new agents. |
| `.AGENTS/` | JSON registry for domain agents (PLANNER, CODER, REVIEWER, DOCS) plus the canonical `TASKS.json`. |
| `PLAN.md` | Human-readable backlog tracked by PLANNER and shared with the rest of the swarm. |
| `LICENSE` | MIT License. |

## Agent Lifecycle

1. **Planning:** The ORCHESTRATOR reads `AGENTS.md`, loads `.AGENTS/*.json`, and creates a plan that maps each step to a registered agent (e.g., PLANNER, CODER, REVIEWER, DOCS).
2. **Approval:** The user can approve, edit, or cancel the plan before any work starts.
3. **Execution:** The orchestrator switches `agent_mode` according to the plan, allowing each agent to follow its JSON-defined workflow inside the IDE.
4. **Progress tracking:** Agents update `PLAN.md` and `.AGENTS/TASKS.json` according to their permissions, ensuring both humans and tools can see the current state.

This structure lets you string together arbitrary workflows such as code implementation, documentation refreshes, research digests, or task triage—all from the same IDE session.

## Shared State Details

- **`PLAN.md`**: Markdown checklist intended for humans. It lists tasks with IDs, sections (Backlog, In Progress, Done), and checkbox status. Agents always read it fully before editing.
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
