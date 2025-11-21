# Project Tasks

_Last updated: 2025-11-21 14:36:21 UTC_

## Summary
- Total tasks: 26
- Backlog: 0
- In Progress: 0
- Blocked: 0
- Done: 26

## Backlog
_No open tasks._

## In Progress
_No active tasks._

## Blocked
_No blocked tasks._

## Done
- [x] [T-001] Document framework in README
  - Priority: med | Owner: codex | Tags: docs, readme
  - Description: Summarize the overall multi-agent workflow so newcomers can understand the repository quickly.
  - Comments:
    - _No comments yet._

- [x] [T-002] Restructure agent registry into JSON files
  - Priority: high | Owner: codex | Tags: agents, architecture
  - Description: Split every reusable agent prompt into a dedicated JSON file under .AGENTS for easier maintenance.
  - Comments:
    - _No comments yet._

- [x] [T-003] Move tasks data into .AGENTS/TASKS.json
  - Priority: high | Owner: codex | Tags: state, persistence
  - Description: Ensure task state is available in a machine-readable JSON file for Codex automation.
  - Comments:
    - _No comments yet._

- [x] [T-004] Enforce per-task git commits in AGENTS spec
  - Priority: high | Owner: codex | Tags: workflow, agents
  - Description: Document the rule that every plan item must end with its own git commit for traceability.
  - Comments:
    - _No comments yet._

- [x] [T-005] Document commit workflow in README
  - Priority: med | Owner: codex | Tags: docs, workflow
  - Description: Expand the README with details on emoji commits and atomic task tracking.
  - Comments:
    - _No comments yet._

- [x] [T-006] Add Agent Creator workflow
  - Priority: high | Owner: codex | Tags: agents, automation
  - Description: Describe how new specialist agents are proposed, reviewed, and added to the registry.
  - Comments:
    - _No comments yet._

- [x] [T-007] Improve commit message guidance
  - Priority: high | Owner: codex | Tags: workflow, git
  - Description: Tighten the instructions around writing meaningful, emoji-prefixed commit messages.
  - Comments:
    - _No comments yet._

- [x] [T-008] Document repository structure in README
  - Priority: med | Owner: codex | Tags: docs, readme
  - Description: Add a quick-start tour of key files and directories so contributors know where to work.
  - Comments:
    - _No comments yet._

- [x] [T-009] Define status transition protocol
  - Priority: high | Owner: codex | Tags: workflow, tasks
  - Description: Clarify which agent owns each state change and how statuses move between TODO/DOING/DONE/BLOCKED.
  - Comments:
    - _No comments yet._

- [x] [T-010] Automate agent registry updates
  - Priority: med | Owner: codex | Tags: agents, automation
  - Description: Explain how the orchestrator scans .AGENTS/*.json dynamically instead of relying on a manual list.
  - Comments:
    - _No comments yet._

- [x] [T-011] Evaluate workflow and suggest improvements
  - Priority: med | Owner: codex | Tags: workflow, analysis
  - Description: Review the end-to-end authoring flow and capture improvement ideas inside the docs.
  - Comments:
    - _No comments yet._

- [x] [T-012] Generalize AGENTS.md to remove agent-specific guidance
  - Priority: med | Owner: codex | Tags: docs, agents
  - Description: Keep AGENTS.md focused on cross-agent protocol instead of baking in individual instructions.
  - Comments:
    - _No comments yet._

- [x] [T-013] Align agent prompts with GPT-5.1 guide
  - Priority: high | Owner: codex | Tags: prompting, agents
  - Description: Update every agent spec so prompts match the GPT-5.1 best practices.
  - Comments:
    - _No comments yet._

- [x] [T-014] Document Cursor + Codex local workflow in AGENTS.md
  - Priority: high | Owner: codex | Tags: docs, agents
  - Description: Add environment assumptions for local-only workflows without remote runtimes.
  - Comments:
    - _No comments yet._

- [x] [T-015] Align agent prompts with Cursor + Codex constraints
  - Priority: high | Owner: codex | Tags: prompting, agents
  - Description: Ensure prompts mention the IDE limitations so agents avoid referencing unavailable tools.
  - Comments:
    - _No comments yet._

- [x] [T-016] Remove tool references from AGENTS.md for Codex-only workflow
  - Priority: high | Owner: codex | Tags: docs, agents
  - Description: Strip references to unsupported helper tools to keep instructions aligned with the local stack.
  - Comments:
    - _No comments yet._

- [x] [T-017] Update agent prompts for tool-less Codex context
  - Priority: high | Owner: codex | Tags: prompting, agents
  - Description: Reword prompts so agents do not assume access to external search or commands.
  - Comments:
    - _No comments yet._

- [x] [T-018] Streamline AGENTS.md English guidelines
  - Priority: high | Owner: codex | Tags: docs, agents
  - Description: Trim redundant English-language instructions and keep the doc crisp.
  - Comments:
    - _No comments yet._

- [x] [T-019] Add glossary-aware translation agent
  - Priority: high | Owner: codex | Tags: agents, localization
  - Description: Introduce a translator agent that respects glossary entries when localizing README content.
  - Comments:
    - _No comments yet._

- [x] [T-020] Add Spanish README translation
  - Priority: med | Owner: codex | Tags: docs, localization
  - Description: Provide a Spanish version of the README while keeping glossary terms consistent.
  - Comments:
    - **reviewer:** Added README.es.md and ensured glossary coverage for Spanish terminology.

- [x] [T-021] Enhance translator glossary workflow
  - Priority: high | Owner: codex | Tags: agents, localization
  - Description: Teach the translator agent how to maintain glossary metadata and usage counts automatically.
  - Comments:
    - **reviewer:** Updated the TRANSLATOR agent so every run maintains GLOSSARY.json, tracks usage frequencies, and enforces approved terms.

- [x] [T-022] Add Russian README translation
  - Priority: med | Owner: codex | Tags: docs, localization
  - Description: Add a Russian localization of the README plus supporting glossary entries.
  - Comments:
    - **reviewer:** Added README.ru.md plus GLOSSARY.json context so translation terminology stays consistent.

- [x] [T-023] Add Spanish README translation
  - Priority: med | Owner: codex | Tags: docs, localization
  - Description: Deliver another Spanish README update incorporating the refined glossary process.
  - Comments:
    - **reviewer:** Created README.es.md and updated GLOSSARY.json with Spanish equivalents for existing terms.

- [x] [T-024] Revise glossary schema for translations
  - Priority: high | Owner: codex | Tags: docs, localization, glossary
  - Description: Restructure the glossary so English remains canonical while localized entries store metadata per language.
  - Comments:
    - **reviewer:** Updated the TRANSLATOR workflow and converted GLOSSARY.json so languages own their preferred terms and descriptions.

- [x] [T-025] Clarify emoji commit workflow
  - Priority: high | Owner: codex | Tags: workflow, git
  - Description: Clarify how commits should start with emojis and summarize completed plan items.
  - Comments:
    - **reviewer:** Updated AGENTS.md and README.md so commit messages start with meaningful emojis referencing the finished plan item.

- [x] [T-026] Enforce atomic task planning
  - Priority: high | Owner: codex | Tags: workflow, planning
  - Description: Ensure the PLANNER splits every request into single-owner tasks with unique commits.
  - Comments:
    - **reviewer:** Updated .AGENTS/PLANNER.json, AGENTS.md, and README.md so the PLANNER keeps tasks atomic.
