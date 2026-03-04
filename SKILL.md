---
name: openclaw-version
description: Manage OpenClaw code synchronization, rebasing, and global builds. Use when user asks to update OpenClaw, sync latest code, rebase main into their dev branch, or rebuild the CLI locally.
---

# OpenClaw Version Management & Auto Build

## Core Context

- **Project Path:** `~/openclaw` (absolute: `/Users/moss/openclaw`)
- **Driver Script:** `scripts/sync_and_build.py` (bundled in this skill)
- **Branch Strategy:**
  - `main`: Remote tracking only — NEVER manually modify
  - `mydev-rebase`: User's custom development branch, rebases onto main

## Execution Protocol

### Phase 1: Pre-flight Checks

1. Confirm working directory is `~/openclaw`
2. Check for uncommitted changes — if present, either alert user or run `git stash`

### Phase 2: Execute Build Script

```bash
cd ~/openclaw && python3 scripts/sync_and_build.py
```

### Phase 3: Handle Results

**Success:** Confirm OpenClaw has been rebuilt, linked globally, and Gateway restarted:

1. `pnpm link --global` completes
2. Check if gateway service is installed via `openclaw gateway status`
3. If not loaded or not installed, run `openclaw gateway install` first
4. Then run `openclaw gateway restart` to apply the new version

**Rebase Conflicts:**

- Stop execution and show conflicting files
- Offer to help resolve or let user handle manually

**Build Failure:** Check pnpm error output — determine if dependency issue or code conflict

## Interaction Guidelines

- **Protect main:** Never commit or push on `main` branch
- **Light humor during waits:** While `pnpm build` runs (30-60s), lighten the mood: "搬运上游的砖块中，并用您的黑科技重新打磨，稍等片刻..."
- **Verify completion:** After build, confirm `openclaw` CLI points to latest code via `openclaw --version` or `which openclaw`

## Bundled Scripts

This skill includes `scripts/sync_and_build.py` which automates:

1. Checkout and pull `main`
2. Checkout `mydev-rebase` and rebase onto `main`
3. Run `pnpm install && pnpm ui:build && pnpm build && pnpm link --global`

Execute the script directly rather than re-implementing the workflow.

## Manual Fallback Commands

If script is unavailable:

```bash
cd ~/openclaw
git checkout main && git pull origin main
git checkout mydev-rebase && git rebase main
pnpm install && pnpm ui:build && pnpm build && pnpm link --global
```

## Conflict Resolution

```bash
# View conflicts
git status

# After resolving
git add <files> && git rebase --continue

# Or abort
git rebase --abort
```

## Verification

```bash
which openclaw
openclaw --version
openclaw status
```
