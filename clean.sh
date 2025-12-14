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

rm -rf \
  .DS_Store \
  .env* \
  .github \
  .gitattributes \
  .git \
  __pycache__ \
  .pytest_cache \
  .venv \
  assets \
  docs \
  README.md \
  tasks.html \
  LICENSE \
  tasks.json \
  CONTRIBUTING.md \
  CODE_OF_CONDUCT.md \
  GUIDELINE.md

if [ -n "$AGENTCTL_DOC_TMP" ]; then
  mkdir -p docs
  mv "$AGENTCTL_DOC_TMP" "$AGENTCTL_DOC"
fi

# Recreate an empty tasks.json so the framework is usable after cleanup.
python - <<'PY' > tasks.json
import hashlib
import json

tasks = []
payload = json.dumps({"tasks": tasks}, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
checksum = hashlib.sha256(payload).hexdigest()

data = {
    "tasks": tasks,
    "meta": {
        "schema_version": 1,
        "managed_by": "agentctl",
        "checksum_algo": "sha256",
        "checksum": checksum,
    },
}

print(json.dumps(data, indent=2, ensure_ascii=False))
PY

# Initialize a fresh repository after the cleanup so the folder can be reused independently.
git init
git add .AGENTS scripts .gitignore AGENTS.md tasks.json
if [ -f "$AGENTCTL_DOC" ]; then
  git add "$AGENTCTL_DOC"
fi
git commit -m "Initial commit"

rm -rf clean.sh
