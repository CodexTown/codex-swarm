#!/usr/bin/env bash
set -euo pipefail

# This script cleans the project folder by removing the root repository links so agents can be used for anything.
# It removes leftover assets, metadata, and git state that would tie the copy to the original repo.
# It also removes framework-development artifacts that aren't needed for a reusable snapshot.
#
# Note: we preserve docs/agentctl.md (if present) as a quick reference for the workflow helper.
AGENTCTL_DOC="docs/agentctl.md"
AGENTCTL_DOC_TMP=""
if [ -f "$AGENTCTL_DOC" ]; then
  AGENTCTL_DOC_TMP="$(mktemp -t agentctl-doc.XXXXXX)"
  cp "$AGENTCTL_DOC" "$AGENTCTL_DOC_TMP"
fi

rm -rf assets docs README.md tasks.html .DS_Store .git .gitattributes .github LICENSE tasks.json CONTRIBUTING.md CODE_OF_CONDUCT.md GUIDELINE.md

if [ -n "$AGENTCTL_DOC_TMP" ]; then
  mkdir -p docs
  mv "$AGENTCTL_DOC_TMP" "$AGENTCTL_DOC"
fi

# Initialize a fresh repository after the cleanup so the folder can be reused independently.
git init
git add .AGENTS scripts .gitignore AGENTS.md
git commit -m "Initial commit"

rm -rf clean.sh
