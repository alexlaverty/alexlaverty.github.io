#!/bin/bash
#
# Sync alexlaverty.github.io repo to GitHub
#

LOG_FILE="/var/log/alexlaverty.github.io.log"
WEBSITE_PATH="/src/alexlaverty.github.io"

# Safer environment for cron
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export GIT_SSH_COMMAND="ssh -i /root/.ssh/id_ed25519"

# Redirect all output to log
exec >> "$LOG_FILE" 2>&1

echo "------------------------------------------------------------"
echo "$(date): Starting update script"

cd "$WEBSITE_PATH" || {
  echo "$(date): ERROR - Cannot cd to $WEBSITE_PATH"
  exit 1
}

# Stash any local changes
if git stash push; then
  echo "$(date): Unstaged changes stashed"
else
  echo "$(date): WARNING - git stash push failed, may have conflicts"
fi

# Pull latest changes with rebase (safer for multi-device sync)
if git pull --rebase origin main; then
  echo "$(date): Changes pulled (with rebase) successfully"

  # Pop the stashed changes
  if git stash pop; then
    echo "$(date): Stashed changes popped"
  else
    echo "$(date): WARNING - git stash pop failed, may need manual conflict resolution"
  fi
else
  echo "$(date): ERROR - git pull --rebase failed, manual fix needed"
  exit 1
fi

# Stage all changes (tracked + untracked + deletions)
git add -A

# Only commit if there are staged changes
if ! git diff --cached --quiet; then
  if git commit -m "Update website - $(date)"; then
    echo "$(date): Commit created"
    if git push origin main; then
      echo "$(date): Changes pushed successfully"
    else
      echo "$(date): ERROR - git push failed"
    fi
  else
    echo "$(date): ERROR - git commit failed"
  fi
else
  echo "$(date): Nothing new to commit"
fi

echo "$(date): Update script complete"
echo "------------------------------------------------------------"
