#!/usr/bin/env python3
"""
OpenClaw Sync & Build Script
Automatically syncs main branch updates, rebases onto dev branch, and rebuilds.
"""

import subprocess
import sys

PROJECT_PATH = "/Users/moss/openclaw"
DEV_BRANCH = "mydev-rebase"
MAIN_BRANCH = "main"


def run(cmd, check=True):
    """Execute shell command and print output."""
    print(f"🔧 执行：{cmd}")
    result = subprocess.run(
        cmd,
        shell=True,
        check=check,
        cwd=PROJECT_PATH,
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result


def sync_and_build():
    """Main workflow: sync main, rebase dev, build and link."""
    print("🏗️  OpenClaw 自动构建脚本启动...\n")

    # Step 1: Sync main branch
    print("📥 步骤 1: 同步 main 分支...")
    run(f"git checkout {MAIN_BRANCH}")
    run("git pull origin main")

    # Step 2: Rebase dev branch onto main
    print(f"\n🔀 步骤 2: Rebase {DEV_BRANCH} 到 main...")
    run(f"git checkout {DEV_BRANCH}")

    try:
        run("git rebase main", check=True)
    except subprocess.CalledProcessError as e:
        print("❌ 检测到 Rebase 冲突！请手动解决后继续。")
        print(f"错误信息：{e}")
        sys.exit(1)

    # Step 3: Install dependencies and build
    print("\n📦 步骤 3: 安装依赖并构建...")
    run("pnpm install && pnpm ui:build && pnpm build && pnpm link --global")

    # Step 4: Check gateway service status and install if needed
    print("\n🔍 步骤 4: 检查 Gateway 服务状态...")
    result = run("openclaw gateway status", check=False)
    
    if "not loaded" in result.stdout.lower() or "not loaded" in result.stderr.lower() or result.returncode != 0:
        print("\n📥 Gateway 服务未安装，正在安装...")
        run("openclaw gateway install")
    
    # Step 5: Restart Gateway to apply new version
    print("\n🔄 步骤 5: 重启 Gateway 使新版本生效...")
    run("openclaw gateway restart")

    print("\n✅ OpenClaw 已更新至最新并重新链接！")
    print("💡 提示：运行 `openclaw --version` 验证版本")


if __name__ == "__main__":
    sync_and_build()
