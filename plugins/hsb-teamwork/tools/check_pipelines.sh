#!/usr/bin/env bash
# CI gate: validate every declarative pipeline graph in the plugin.
# Exits non-zero on the first invalid graph. Add to CI or a pre-commit hook.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
plugin_root="$(dirname "$here")"
validator="$here/pipeline_graph.py"

shopt -s nullglob
graphs=("$plugin_root"/skills/*/pipeline.yaml)

if [ ${#graphs[@]} -eq 0 ]; then
  echo "no pipeline.yaml graphs found under $plugin_root/skills/"
  exit 0
fi

fail=0
for g in "${graphs[@]}"; do
  if python3 "$validator" "$g" --quiet; then
    echo "ok   $g"
  else
    fail=1
  fi
done

exit $fail
