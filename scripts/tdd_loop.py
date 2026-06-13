#!/usr/bin/env python3
"""
TDD Loop: implements a feature from issue context via opencode.
Supports two modes:
  1. Initial: implement.yml — creates branch + Draft PR, runs TDD loop
  2. Rework: rework.yml  — PR already exists, applies review feedback, runs TDD loop
"""

import json
import os
import subprocess
import sys
import time
import urllib.request

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
ISSUE_URL = os.environ["ISSUE_URL"]
REPO = os.environ["REPO"]
MAX_ITERATIONS = int(os.environ.get("MAX_ITERATIONS", "10"))
TIMEOUT_MINUTES = int(os.environ.get("TIMEOUT_MINUTES", "30"))

ISSUE_NUMBER = os.environ.get("ISSUE_NUMBER", "")
REVIEW_BODY = ""
review_file = "/tmp/review_body.txt"
if os.path.exists(review_file):
    with open(review_file) as f:
        REVIEW_BODY = f.read().strip()

MODE = os.environ.get("TDD_MODE", "initial")

API_BASE = f"https://api.github.com/repos/{REPO}"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def gh_api(path, method="GET", data=None):
    url = f"{API_BASE}/{path.lstrip('/')}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def get_current_branch():
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
    return result.stdout.strip()


def get_default_branch():
    repo = gh_api("")
    return repo["default_branch"]


def get_issue_context():
    issue = gh_api(f"issues/{ISSUE_NUMBER}")
    comments = gh_api(f"issues/{ISSUE_NUMBER}/comments")
    context = f"## Issue #{ISSUE_NUMBER}\n\n{issue['body'] or ''}\n\n"
    context += "## Comments\n\n"
    for c in comments:
        context += f"---\n{c['user']['login']}: {c['body']}\n"
    return context


def get_pr_context(pr_number):
    pr = gh_api(f"pulls/{pr_number}")
    comments = gh_api(f"issues/{pr_number}/comments")
    reviews = gh_api(f"pulls/{pr_number}/reviews")
    context = f"## PR #{pr_number}\n\n{pr['body'] or ''}\n\n"
    context += "## PR Comments\n\n"
    for c in comments:
        context += f"---\n{c['user']['login']}: {c['body']}\n"
    context += "\n## Reviews\n\n"
    for r in reviews:
        context += f"---\n{r['user']['login']} ({r['state']}): {r['body']}\n"
    return context, pr


def find_pr_by_branch(branch_name):
    pulls = gh_api(f"pulls?head={REPO.split('/')[0]}:{branch_name}&state=open")
    if pulls:
        return pulls[0]["number"]
    return None


def create_feature_branch(default_branch):
    branch_name = f"feat/issue-{ISSUE_NUMBER}"
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    return branch_name


def create_draft_pr(branch_name, default_branch):
    issue = gh_api(f"issues/{ISSUE_NUMBER}")
    title = issue["title"]
    pr_data = {
        "title": title,
        "head": branch_name,
        "base": default_branch,
        "body": f"Closes #{ISSUE_NUMBER}\n\n## 实现方案\n\n由 AI 自动生成，Draft PR 表示代码正在实现中。",
        "draft": True,
    }
    pr = gh_api("pulls", method="POST", data=pr_data)
    return pr["number"]


def run_opencode(goal, context):
    cmd = [
        "opencode", "run",
        "--goal", goal,
        "--context", context,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    return result.returncode, result.stdout, result.stderr


def git_commit_and_push(message):
    subprocess.run(["git", "add", "-A"], check=True)
    subprocess.run(["git", "commit", "-m", message, "--allow-empty"], check=True)
    subprocess.run(["git", "push", "origin", "HEAD"], check=True)


def wait_for_commit_status(sha, timeout_minutes=5):
    deadline = time.time() + timeout_minutes * 60
    while time.time() < deadline:
        statuses = gh_api(f"commits/{sha}/status")
        state = statuses.get("state", "pending")
        if state == "success":
            return True
        elif state == "failure":
            return False
        time.sleep(15)
    return None


def post_comment(pr_number, body):
    gh_api(f"issues/{pr_number}/comments", method="POST", data={"body": body})


def mark_pr_ready(pr_number):
    url = f"{API_BASE}/pulls/{pr_number}"
    req = urllib.request.Request(url, data=json.dumps({"draft": False}).encode(), headers=HEADERS, method="PATCH")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def main():
    start_time = time.time()

    if MODE == "rework":
        print("=== REWORK MODE ===")
        branch_name = get_current_branch()
        pr_number = find_pr_by_branch(branch_name)
        if not pr_number:
            print(f"ERROR: no open PR found for branch {branch_name}")
            sys.exit(1)
        print(f"Found existing PR #{pr_number} on branch {branch_name}")

        pr_context, pr_data = get_pr_context(pr_number)
        original_issue = pr_data["body"] or ""
        issue_url = pr_data["html_url"]
        context = f"## 原始 Issue\n\n{original_issue}\n\n{pr_context}"
        if REVIEW_BODY:
            context += f"\n## Review 修改要求\n\n{REVIEW_BODY}\n"
        print(f"Gathered PR #{pr_number} context including review feedback")
    else:
        print("=== INITIAL MODE ===")
        print("Step 1: Fetch issue context")
        context = get_issue_context()
        print(f"Fetched issue #{ISSUE_NUMBER} context")

        print("Step 2: Create feature branch and Draft PR")
        default_branch = get_default_branch()
        branch_name = create_feature_branch(default_branch)
        pr_number = create_draft_pr(branch_name, default_branch)
        print(f"Created Draft PR #{pr_number} on branch {branch_name}")

    for iteration in range(1, MAX_ITERATIONS + 1):
        elapsed = (time.time() - start_time) / 60
        if elapsed > TIMEOUT_MINUTES:
            print(f"TIMEOUT: exceeded {TIMEOUT_MINUTES} minutes")
            post_comment(pr_number, f"## 超时\n\nTDD 循环已超过 {TIMEOUT_MINUTES} 分钟限制，请手动 review。")
            sys.exit(1)

        print(f"\n=== Iteration {iteration}/{MAX_ITERATIONS} ===")

        print("--- Phase A: Write/update tests (RED) ---")
        test_goal = (
            f"这是 Issue #{ISSUE_NUMBER} 的功能请求。当前 PR #{pr_number} 正在实现该功能。\n"
            f"请阅读 Issue 内容和现有测试文件，编写或更新测试代码来覆盖新功能的需求。\n"
            f"测试文件放在 tests/ 目录下，使用 pytest + fastapi TestClient。\n"
            f"先写测试（RED 阶段），确保新的测试能清楚表达需求。\n"
            f"不要修改 app/ 下的代码。"
        )
        ret, stdout, stderr = run_opencode(test_goal, context)
        print(f"opencode (RED) exit code: {ret}")

        git_commit_and_push(f"test: add tests for issue #{ISSUE_NUMBER} [iteration {iteration}]")

        print("--- Phase B: Wait for CI on test commit ---")
        sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        test_pass = wait_for_commit_status(sha)
        if test_pass is False:
            print("Tests failed on RED phase (expected — no implementation yet)")

        print("--- Phase C: Implement code (GREEN) ---")
        impl_goal = (
            f"这是 Issue #{ISSUE_NUMBER} 的功能请求。\n"
            f"请阅读 Issue 内容和现有 tests/ 中的测试代码。\n"
            f"在 app/ 目录下实现功能代码，让所有测试通过。\n"
            f"不要修改测试文件，只修改 app/ 下的代码。\n"
            f"这是 GREEN 阶段，目标是让测试全部通过。"
        )
        ret, stdout, stderr = run_opencode(impl_goal, context)
        print(f"opencode (GREEN) exit code: {ret}")

        git_commit_and_push(f"feat: implement for issue #{ISSUE_NUMBER} [iteration {iteration}]")

        print("--- Phase D: Wait for CI on implementation commit ---")
        sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        test_pass = wait_for_commit_status(sha, timeout_minutes=10)

        if test_pass is True:
            print(f"ALL TESTS PASSED on iteration {iteration}!")
            post_comment(pr_number, f"## 测试通过\n\n第 {iteration} 轮迭代后所有测试通过。")
            if MODE == "initial":
                print(f"Marking PR #{pr_number} as Ready for Review")
                mark_pr_ready(pr_number)
                post_comment(pr_number, f"## Ready for Review\n\nPR 已标记为 Ready for Review，请项目所有者 review。")
            else:
                post_comment(pr_number, f"## Rework 完成\n\nReview 反馈已处理，测试全部通过。")
            sys.exit(0)
        elif test_pass is None:
            post_comment(pr_number, f"## 超时\n\n第 {iteration} 轮迭代测试超时，请手动 review。")
            sys.exit(1)
        else:
            print(f"Tests failed on iteration {iteration}, retrying...")
            post_comment(pr_number, f"## 第 {iteration} 轮迭代\n\n测试未通过，继续迭代。")

    print(f"FAILED: exceeded max iterations ({MAX_ITERATIONS})")
    post_comment(pr_number, f"## 已达到最大迭代次数\n\n经过 {MAX_ITERATIONS} 轮迭代后测试仍未全过，请手动 review。")
    sys.exit(1)


if __name__ == "__main__":
    main()
