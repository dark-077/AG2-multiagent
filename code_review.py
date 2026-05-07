"""
AG2 Multi-Agent - 智能代码审查系统

使用 AG2 GroupChat 实现 4 个专项审查 Agent 并行工作：
  Linter Agent    → 代码风格 & 语法检查
  Security Agent  → 安全漏洞扫描
  Perf Agent      → 性能与资源分析
  Logic Agent     → 业务逻辑审查
  Reviewer Lead   → 统筹协调，汇总最终报告

运行方式:
    python code_review.py
    python code_review.py --mode groupchat
    python code_review.py --mode beta
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env
load_dotenv()

# AG2 Beta
import autogen.beta
from autogen.beta import Agent
from autogen.beta.config import OpenAIConfig
from autogen.beta.tools.subagents.subagent_tool import subagent_tool

# AG2 Legacy
from autogen import (
    ConversableAgent,
    GroupChat,
    GroupChatManager,
)

# ============================================================
# 配置
# ============================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "")

if not OPENAI_API_KEY and not ANTHROPIC_API_KEY:
    print("ERROR: No API key found! Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
    sys.exit(1)

USE_MODEL = "Qwen/Qwen2.5-72B-Instruct" if OPENAI_API_KEY else "claude-sonnet-4-20250514"
USE_API_KEY = OPENAI_API_KEY if OPENAI_API_KEY else ANTHROPIC_API_KEY

print(f"[OK] Using model: {USE_MODEL}")


# ============================================================
# 示例代码（供审查使用）
# ============================================================

SAMPLE_CODE = '''
def get_user_data(user_id, include_password=False):
    """获取用户数据"""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    result = cursor.fetchone()
    conn.close()

    if include_password:
        return result
    return {"id": result[0], "name": result[1], "email": result[2]}

def send_email(to, subject, body):
    import smtplib
    server = smtplib.SMTP("smtp.example.com", 25)
    server.login("user@example.com", "password123")
    msg = f"Subject: {subject}\\n\\n{body}"
    server.sendmail("user@example.com", to, msg)
    return True

for i in range(1000000):
    with open("log.txt", "a") as f:
        f.write(f"Processing item {i}\\n")
'''

SAMPLE_CODE_REVIEW_RESULT = """
【代码审查报告】

## 1. Linter Agent — 代码风格 & 语法
- [WARN] SQL 注入风险：`f"SELECT * FROM users WHERE id = {user_id}"` 直接拼接变量
- [WARN] `conn` 和 `cursor` 未使用 `with` 上下文管理器，可能泄漏
- [WARN] `result[0]` 等硬编码索引访问，应使用列名
- [WARN] 函数无类型注解、无文档参数描述

## 2. Security Agent — 安全漏洞
- [CRIT] **严重**：`f"SELECT * FROM users WHERE id = {user_id}"` SQL 注入漏洞
- [CRIT] **严重**：`password123` 明文硬编码密码
- [HIGH] **高危**：SMTP 认证使用明文密码，建议使用环境变量
- [WARN] 数据库文件路径硬编码，缺访问权限控制

## 3. Perf Agent — 性能 & 资源
- [CRIT] **严重**：循环内重复打开/关闭文件 `open("log.txt")` 100万次，应使用缓冲写入
- [WARN] `cursor.execute` 每次执行单独查询，无批量操作
- [WARN] `smtplib.SMTP` 连接未释放（无 `server.quit()`）

## 4. Logic Agent — 业务逻辑
- [WARN] `include_password=True` 时返回完整元组，包含密码字段，违反最小权限原则
- [WARN] `send_email` 函数无重试机制、无异常处理
- [WARN] 缺少输入验证（user_id 负数、空值等情况）

## 总结
| 严重程度   | 问题数 |
|------------|--------|
| [CRIT] 严重 | 4      |
| [WARN] 警告 | 8      |

建议优先修复 SQL 注入和明文密码问题。
"""


# ============================================================
# Agent 工厂函数（Legacy ConversableAgent）
# ============================================================

def create_reviewer_lead() -> ConversableAgent:
    system = """You are the Reviewer Lead — the orchestrator of a code review team.
Your team has 4 specialist agents:
  - Linter Agent:    code style, syntax, and best practices
  - Security Agent:  vulnerability scanning and security best practices
  - Perf Agent:       performance and resource usage analysis
  - Logic Agent:      business logic and architecture review

Your job:
1. When given code to review, coordinate all 4 agents to review in parallel
2. Wait for all agents to complete their review
3. Synthesize their findings into a final code review report
4. Prioritize issues by severity: CRITICAL > HIGH > MEDIUM > LOW

Be professional, thorough, and constructive. Format the final report clearly with sections for each agent's findings and a summary table."""
    return ConversableAgent(
        name="ReviewerLead",
        system_message=system,
        llm_config={
            "config_list": [{
                "model": USE_MODEL,
                "api_key": USE_API_KEY,
                "base_url": OPENAI_API_BASE or None,
            }],
            "temperature": 0.5,
        },
        max_consecutive_auto_reply=15,
        human_input_mode="NEVER",
        description="Code review team orchestrator",
    )


def create_linter_agent() -> ConversableAgent:
    system = """You are the Linter Agent — an expert in code style, syntax, and Python best practices.
Your responsibilities:
1. Check Python code for style violations (PEP 8)
2. Identify syntax errors and potential bugs
3. Flag anti-patterns and code smells
4. Suggest improvements for readability and maintainability

Always provide specific line references and corrected code examples when possible.
Use severity levels: CRITICAL, WARNING, INFO."""
    return ConversableAgent(
        name="LinterAgent",
        system_message=system,
        llm_config={
            "config_list": [{
                "model": USE_MODEL,
                "api_key": USE_API_KEY,
                "base_url": OPENAI_API_BASE or None,
            }],
            "temperature": 0.3,
        },
        max_consecutive_auto_reply=3,
        human_input_mode="NEVER",
        description="Code style and syntax checker",
    )


def create_security_agent() -> ConversableAgent:
    system = """You are the Security Agent — an expert in application security.
Your responsibilities:
1. Scan code for security vulnerabilities (SQL injection, XSS, etc.)
2. Check for hardcoded secrets, passwords, API keys
3. Verify authentication and authorization patterns
4. Flag insecure dependencies or configurations

Use OWASP Top 10 as a reference. Provide CVSS-like severity ratings.
Use severity levels: CRITICAL, HIGH, MEDIUM, LOW."""
    return ConversableAgent(
        name="SecurityAgent",
        system_message=system,
        llm_config={
            "config_list": [{
                "model": USE_MODEL,
                "api_key": USE_API_KEY,
                "base_url": OPENAI_API_BASE or None,
            }],
            "temperature": 0.3,
        },
        max_consecutive_auto_reply=3,
        human_input_mode="NEVER",
        description="Security vulnerability scanner",
    )


def create_perf_agent() -> ConversableAgent:
    system = """You are the Performance Agent — an expert in code performance optimization.
Your responsibilities:
1. Identify performance bottlenecks and anti-patterns
2. Check for inefficient loops, unnecessary I/O operations
3. Suggest algorithmic improvements
4. Flag resource leaks (file handles, connections, etc.)

Use time/space complexity analysis when relevant.
Use severity levels: CRITICAL, HIGH, MEDIUM, LOW."""
    return ConversableAgent(
        name="PerfAgent",
        system_message=system,
        llm_config={
            "config_list": [{
                "model": USE_MODEL,
                "api_key": USE_API_KEY,
                "base_url": OPENAI_API_BASE or None,
            }],
            "temperature": 0.3,
        },
        max_consecutive_auto_reply=3,
        human_input_mode="NEVER",
        description="Performance and resource analyzer",
    )


def create_logic_agent() -> ConversableAgent:
    system = """You are the Logic Agent — an expert in business logic and software architecture.
Your responsibilities:
1. Review code for logical errors and edge cases
2. Check input validation and error handling
3. Evaluate function/class design and separation of concerns
4. Flag violations of SOLID principles

Be constructive and suggest specific improvements.
Use severity levels: CRITICAL, HIGH, MEDIUM, LOW."""
    return ConversableAgent(
        name="LogicAgent",
        system_message=system,
        llm_config={
            "config_list": [{
                "model": USE_MODEL,
                "api_key": USE_API_KEY,
                "base_url": OPENAI_API_BASE or None,
            }],
            "temperature": 0.3,
        },
        max_consecutive_auto_reply=3,
        human_input_mode="NEVER",
        description="Business logic and architecture reviewer",
    )


# ============================================================
# GroupChat 模式
# ============================================================

def run_groupchat_review(code: str):
    """GroupChat 模式：ReviewerLead + 4 个专项 Agent"""
    print("\n" + "=" * 60)
    print("Code Review System — GroupChat Mode")
    print("=" * 60)

    # 创建所有 Agent
    lead = create_reviewer_lead()
    linter = create_linter_agent()
    security = create_security_agent()
    perf = create_perf_agent()
    logic = create_logic_agent()

    # 创建群聊（5个 Agent）
    group_chat = GroupChat(
        agents=[lead, linter, security, perf, logic],
        max_round=20,
        speaker_selection_method="round_robin",
        allow_repeat_speaker=False,
        enable_clear_history=True,
        send_introductions=True,
    )

    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config={
            "config_list": [{
                "model": USE_MODEL,
                "api_key": USE_API_KEY,
                "base_url": OPENAI_API_BASE or None,
            }],
        },
    )

    task = f"""Please review the following Python code by coordinating your team.
Each specialist (LinterAgent, SecurityAgent, PerfAgent, LogicAgent) should provide their findings.
After all reviews are in, synthesize everything into a final report.

Code to review:
```python
{code}
```"""

    print("\nStarting code review...\n")
    print("-" * 60)

    result = lead.initiate_chat(
        manager,
        message=task,
        clear_history=True,
    )

    print("-" * 60)
    print("\n[OK] Code review completed!\n")

    if hasattr(result, 'summary'):
        print("=" * 60)
        print("FINAL CODE REVIEW REPORT")
        print("=" * 60)
        print(result.summary)

    return result


# ============================================================
# Beta Agent-as-tool 模式
# ============================================================

async def run_beta_review_async(code: str):
    """Beta 模式：使用 AG2 Beta Agent-as-tool 进行代码审查"""
    print("\n" + "=" * 60)
    print("Code Review System — Beta Agent-as-tool Mode")
    print("=" * 60)

    config = OpenAIConfig(
        model=USE_MODEL,
        api_key=USE_API_KEY,
        base_url=OPENAI_API_BASE or None,
    )

    # Beta Agent 定义
    lead = Agent(
        name="ReviewerLead",
        config=config,
        system_message="""You are the Reviewer Lead for a code review team.
Coordinate 4 specialist agents to review code:
- LinterAgent: code style and syntax
- SecurityAgent: vulnerability scanning
- PerfAgent: performance analysis
- LogicAgent: business logic

After receiving code, ask each specialist for their findings, then synthesize a final report.""",
    )

    linter = Agent(
        name="LinterAgent",
        config=config,
        system_message="You are the Linter Agent. Review code for style, syntax, and best practices. Be concise and specific.",
    )

    security = Agent(
        name="SecurityAgent",
        config=config,
        system_message="You are the Security Agent. Scan for vulnerabilities, hardcoded secrets, and insecure patterns.",
    )

    perf = Agent(
        name="PerfAgent",
        config=config,
        system_message="You are the Performance Agent. Identify bottlenecks, resource leaks, and optimization opportunities.",
    )

    logic = Agent(
        name="LogicAgent",
        config=config,
        system_message="You are the Logic Agent. Review business logic, edge cases, and error handling.",
    )

    # 注册 subagent tools
    linter_tool = subagent_tool(linter, name="linter_review", description="Review code style and syntax")
    security_tool = subagent_tool(security, name="security_review", description="Scan for security vulnerabilities")
    perf_tool = subagent_tool(perf, name="perf_review", description="Analyze performance and resources")
    logic_tool = subagent_tool(logic, name="logic_review", description="Review business logic")

    tools = [linter_tool, security_tool, perf_tool, logic_tool]

    task = f"""Review this Python code using your specialist agents:

```python
{code}
```

Ask all 4 specialists for their findings, then provide a final synthesized report with severity ratings."""

    print("\nRunning Beta code review...\n")
    print("-" * 60)

    reply = await lead.ask(task, tools=tools)

    print("\n" + "-" * 60)
    print("\n[OK] Beta code review completed!\n")

    if reply and reply.body:
        print("=" * 60)
        print("FINAL CODE REVIEW REPORT")
        print("=" * 60)
        print(reply.body)

    return reply


def run_beta_review(code: str):
    return asyncio.run(run_beta_review_async(code))


# ============================================================
# 演示模式（直接输出预设报告，无需 API 调用）
# ============================================================

def run_demo_mode():
    """演示模式：展示代码审查系统的工作流程（无需 API）"""
    print("\n" + "=" * 60)
    print("Code Review System — DEMO Mode")
    print("=" * 60)
    print("\n演示模式：展示 4 Agent 并行审查流程")
    print("-" * 60)

    agents = ["LinterAgent", "SecurityAgent", "PerfAgent", "LogicAgent"]
    for agent in agents:
        print(f"  [{agent}] → 正在审查代码...")
    print()
    for agent in agents:
        print(f"  [{agent}] -> 审查完成 [OK]")
    print()

    print("ReviewerLead 正在汇总所有审查意见...")
    print()
    print("=" * 60)
    print("FINAL CODE REVIEW REPORT")
    print("=" * 60)
    print(SAMPLE_CODE_REVIEW_RESULT)

    return None


# ============================================================
# 主函数
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="AG2 智能代码审查系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
运行模式:
  demo      演示模式（无需 API，展示预设审查流程）
  groupchat 使用 AG2 Legacy GroupChat（需 API Key）
  beta      使用 AG2 Beta Agent-as-tool（需 API Key）
        """,
    )
    parser.add_argument(
        "--mode",
        choices=["demo", "groupchat", "beta"],
        default="demo",
        help="运行模式（默认: demo）",
    )
    parser.add_argument(
        "--code",
        type=str,
        default="",
        help="要审查的代码（可选，默认使用内置示例代码）",
    )
    args = parser.parse_args()

    # 使用传入代码或默认示例
    code = args.code if args.code else SAMPLE_CODE

    if args.code:
        print(f"\n[INFO] Using provided code (length: {len(args.code)} chars)")
    else:
        print("\n[INFO] Using built-in sample code")

    try:
        if args.mode == "beta":
            run_beta_review(code)
        elif args.mode == "groupchat":
            run_groupchat_review(code)
        else:
            run_demo_mode()
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
