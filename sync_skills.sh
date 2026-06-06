#!/usr/bin/env bash
# Syncs skills from this repo into agent skill directories as individual symlinks.
# Run after adding, renaming, or removing skills.
# Works on macOS and Linux.

set -euo pipefail

# Resolve the repo skills directory (portable, no readlink -f needed)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_SKILLS="$SCRIPT_DIR/skills"
DEFAULT_TARGET_SKILL_DIRS=(
    "$HOME/.claude/skills"
    "$HOME/.codex/skills"
)

if [ "$#" -gt 0 ]; then
    TARGET_SKILL_DIRS=("$@")
elif [ -n "${AGENT_SKILL_DIRS:-}" ]; then
    IFS=: read -r -a TARGET_SKILL_DIRS <<< "$AGENT_SKILL_DIRS"
else
    TARGET_SKILL_DIRS=("${DEFAULT_TARGET_SKILL_DIRS[@]}")
fi

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

    echo "syncing: $global_skills"

    # Remove stale symlinks: point into this repo but their target is gone
    # (e.g. a skill was renamed or deleted). Valid links are kept so we can
    # report them as unchanged below.
    for link in "$global_skills"/*; do
        [ -L "$link" ] || continue
        resolved="$(resolve_link "$link")"
        case "$resolved" in
            "${REPO_SKILLS}"/*) [ -d "$resolved" ] || { rm "$link"; echo "  removed: $(basename "$link") (stale)"; } ;;
        esac
    done

    # Link every skill in the repo, reporting whether each was added, changed,
    # or already correct.
    added=0 changed=0 unchanged=0
    for skill_dir in "$REPO_SKILLS"/*/; do
        [ -d "$skill_dir" ] || continue
        name="$(basename "$skill_dir")"
        dest="$global_skills/$name"
        if [ -L "$dest" ] && [ "$(resolve_link "$dest")" = "${skill_dir%/}" ]; then
            : $((unchanged++))  # already a correct symlink — nothing to do
            continue
        elif [ -e "$dest" ] || [ -L "$dest" ]; then
            : $((changed++)); echo "  changed: $name"
        else
            : $((added++)); echo "  added:   $name"
        fi
        ln -sfn "$skill_dir" "$dest"
    done
    echo "  $added added, $changed changed, $unchanged unchanged"
done
