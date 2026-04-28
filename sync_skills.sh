#!/usr/bin/env bash
# Syncs skills from this repo into agent skill directories as individual symlinks.
# Run after adding, renaming, or removing skills.
# Works on macOS and Linux.

set -euo pipefail

# Resolve the repo skills directory (portable, no readlink -f needed)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_SKILLS="$SCRIPT_DIR/skills"
TARGET_SKILL_DIRS=(
    "$HOME/.claude/skills"
    "$HOME/.codex/skills"
)

# Resolve a symlink target to an absolute path (works on macOS and Linux)
resolve_link() {
    local target
    target="$(readlink "$1")"
    # If target is relative, make it absolute based on the link's directory
    if [[ "$target" != /* ]]; then
        target="$(cd "$(dirname "$1")" && cd "$(dirname "$target")" && pwd)/$(basename "$target")"
    fi
    # Strip trailing slash for consistent comparison
    printf '%s' "${target%/}"
}

for global_skills in "${TARGET_SKILL_DIRS[@]}"; do
    mkdir -p "$global_skills"

    # Remove stale symlinks that point into this repo
    for link in "$global_skills"/*; do
        [ -L "$link" ] || continue
        resolved="$(resolve_link "$link")"
        case "$resolved" in
            "${REPO_SKILLS}"/*) rm "$link"; echo "removed stale: $(basename "$link")" ;;
        esac
    done

    echo "syncing: $global_skills"

    # Create fresh symlinks for every skill directory in the repo
    for skill_dir in "$REPO_SKILLS"/*/; do
        [ -d "$skill_dir" ] || continue
        name="$(basename "$skill_dir")"
        ln -sfn "$skill_dir" "$global_skills/$name"
        echo "linked: $name"
    done
done
