---
name: openclaw-version
description: Manage OpenClaw code synchronization, rebasing, and global builds. Use when user asks to update OpenClaw, sync latest code, rebase main into their dev branch, or rebuild the CLI locally.
---

# OpenClaw Version Management & Auto Build

## Core Context

- **Project Path:** `~/openclaw` (absolute: `/Users/moss/openclaw`)
- **Driver Script:** `sync_and_build.py` — located in the **same directory as this SKILL.md** (`~/.openclaw/skills/openclaw-version/sync_and_build.py`)
- **Branch Strategy:**
  - `main`: Remote tracking only — NEVER manually modify
  - `mydev-rebase`: User's custom development branch, rebases onto main

## Execution Protocol

### Phase 1: Pre-flight Checks

1. Confirm working directory is `~/openclaw`
2. Check for uncommitted changes — if present, either alert user or run `git stash`

### Phase 2: Execute Build Script

```bash
# Option A: Script in same directory as SKILL.md
python3 ~/.openclaw/skills/openclaw-version/sync_and_build.py

# Option B: Manual fallback (if script doesn't exist)
cd ~/openclaw
git checkout main && git pull origin main
git checkout mydev-rebase && git rebase main
pnpm install && pnpm ui:build && pnpm build && pnpm link --global
```

### Phase 3: Gateway Install & Restart (REQUIRED)

**After build completes, always run these steps in order:**

1. **Re-install Gateway service** (mandatory, ensures service file is up-to-date):
   ```bash
   openclaw gateway install
   ```

2. **Restart Gateway** to apply the new version:
   ```bash
   openclaw gateway restart
   ```

3. **Verify** the Gateway is running with the new version:
   ```bash
   openclaw gateway status
   openclaw --version
   ```

**Why `gateway install` is mandatory:** Even if the Gateway service is already installed, running `gateway install` ensures the service file is synchronized with the latest code changes. Skipping this step may result in the Gateway running with outdated configuration or code.

**Rebase Conflicts:**

- Stop execution and show conflicting files
- Offer to help resolve or let user handle manually

**Build Failure:** Check pnpm error output — determine if dependency issue or code conflict

## Interaction Guidelines

- **Protect main:** Never commit or push on `main` branch
- **Light humor during waits:** While `pnpm build` runs (30-60s), lighten the mood: "搬运上游的砖块中，并用您的黑科技重新打磨，稍等片刻..."
- **Verify completion:** After build, confirm `openclaw` CLI points to latest code via `openclaw --version` or `which openclaw`

## Bundled Scripts

This skill includes `sync_and_build.py` located at **`<skill-directory>/sync_and_build.py`** (where `<skill-directory>` is the same folder containing this SKILL.md, i.e., `~/.openclaw/skills/openclaw-version/`).

The script automates:

1. Checkout and pull `main`
2. Checkout `mydev-rebase` and rebase onto `main`
3. Run `pnpm install && pnpm ui:build && pnpm build && pnpm link --global`
4. Run `openclaw gateway install` (mandatory)
5. Run `openclaw gateway restart`

Execute the script directly rather than re-implementing the workflow:

```bash
python3 ~/.openclaw/skills/openclaw-version/sync_and_build.py
```

**Note:** If you run the build commands manually instead of using the script, remember to always follow up with:
```bash
openclaw gateway install
openclaw gateway restart
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
