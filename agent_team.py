"""
AG2 Multi-Agent - Lead + Critic 双智能体协作

使用 AG2 (formerly AutoGen) 0.12.x 构建多智能体系统

运行方式:
    # GroupChat 模式（默认）
    python agent_team.py
    python agent_team.py --mode groupchat

    # Beta Agent-as-tool 模式（展示 AG2 Beta 原生 Agent 能力）
    python agent_team.py --mode beta

    # 智能代码审查模式（Linter/Security/Perf/Logic 4 Agent 并行审查）
    python agent_team.py --mode review
    python code_review.py          # 直接运行（推荐）
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# AG2 Beta 组件
import autogen.beta
from autogen.beta import Agent
from autogen.beta.config import OpenAIConfig
from autogen.beta.tools.subagents.subagent_tool import subagent_tool

# AG2 Legacy 组件 (用于 GroupChat 多智能体协作)
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
    print("ERROR: No API key found!")
    print("Please set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env file")
    sys.exit(1)

USE_MODEL = "Qwen/Qwen2.5-72B-Instruct" if OPENAI_API_KEY else "claude-sonnet-4-20250514"
USE_API_KEY = OPENAI_API_KEY if OPENAI_API_KEY else ANTHROPIC_API_KEY

print(f"[OK] Using model: {USE_MODEL}")

# ============================================================
# Agent 定义
# ============================================================

def create_lead_agent() -> ConversableAgent:
    """Lead Agent - 任务拆解和执行"""

    lead_system_message = """You are a task decomposition expert (Lead Agent).
Your responsibilities:
1. Analyze user requests and break them into clear sub-tasks
2. Coordinate other agents to complete work
3. Integrate results and provide final answers

Communication style: Professional, concise, structured"""

    lead = ConversableAgent(
        name="Lead",
        system_message=lead_system_message,
        llm_config={
            "config_list": [
                {
                    "model": USE_MODEL,
                    "api_key": USE_API_KEY,
                    "base_url": OPENAI_API_BASE or None,
                }
            ],
            "temperature": 0.7,
        },
        max_consecutive_auto_reply=10,
        human_input_mode="NEVER",
        description="Task decomposition expert",
    )

    return lead


def create_critic_agent() -> ConversableAgent:
    """Critic Agent - 质量审查"""

    critic_system_message = """You are a quality review expert (Critic Agent).
Your responsibilities:
1. Review proposals or answers from Lead
2. Provide constructive feedback and improvement suggestions
3. Ensure output quality meets high standards
4. Identify potential logical flaws or errors

Communication style: Direct, objective, constructive"""

    critic = ConversableAgent(
        name="Critic",
        system_message=critic_system_message,
        llm_config={
            "config_list": [
                {
                    "model": USE_MODEL,
                    "api_key": USE_API_KEY,
                    "base_url": OPENAI_API_BASE or None,
                }
            ],
            "temperature": 0.5,
        },
        max_consecutive_auto_reply=5,
        human_input_mode="NEVER",
        description="Quality review expert",
    )

    return critic


# ============================================================
# 群聊系统
# ============================================================

def create_group_chat(lead: ConversableAgent, critic: ConversableAgent) -> GroupChat:
    """创建群聊系统"""
    group_chat = GroupChat(
        agents=[lead, critic],
        max_round=10,
        speaker_selection_method="round_robin",
        allow_repeat_speaker=False,
        enable_clear_history=True,
        send_introductions=True,
    )
    return group_chat


def create_group_chat_manager(group_chat: GroupChat) -> GroupChatManager:
    """创建群聊管理器"""
    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config={
            "config_list": [
                {
                    "model": USE_MODEL,
                    "api_key": USE_API_KEY,
                    "base_url": OPENAI_API_BASE or None,
                }
            ],
        },
    )
    return manager


# ============================================================
# 运行协作
# ============================================================

def run_groupchat_mode(task: str):
    """运行 GroupChat 模式：Lead + Critic 群聊协作"""
    print("\n" + "=" * 60)
    print("AG2 Multi-Agent: Lead + Critic GroupChat")
    print("=" * 60)
    print(f"\nTask: {task}\n")
    print("-" * 60)

    # 创建 Agents
    lead = create_lead_agent()
    critic = create_critic_agent()

    # 创建群聊
    group_chat = create_group_chat(lead, critic)
    manager = create_group_chat_manager(group_chat)

    # 发起对话
    print("Starting chat...\n")
    chat_result = lead.initiate_chat(
        manager,
        message=task,
        clear_history=True,
    )

    print("-" * 60)
    print("\n[OK] Chat completed!\n")

    if hasattr(chat_result, 'summary'):
        print("Result:")
        print(chat_result.summary)

    return chat_result


# ============================================================
# Beta Agent-as-tool 模式
# ============================================================

async def run_beta_mode_async(task: str):
    """
    Beta 模式：使用 AG2 Beta Agent 和 Agent-as-tool 模式
    
    展示 AG2 Beta 原生特性：
    1. autogen.beta.Agent 异步创建
    2. subagent_tool() 将 Agent 注册为工具
    3. Agent.ask() 异步方法调用
    4. 工具调用结果自动处理
    5. Beta Agent 的 reply.body 结构
    """
    print("\n" + "=" * 60)
    print("AG2 Multi-Agent: Beta Agent-as-tool Mode")
    print("=" * 60)
    print("\n[Beta 原生特性]")
    print("  1. autogen.beta.Agent 异步创建")
    print("  2. subagent_tool() Agent-as-tool 注册")
    print("  3. Agent.ask() 异步工具调用")
    print("  4. Beta reply.body 结构化返回")
    print("-" * 60)
    print(f"\nTask: {task}\n")

    # 创建 Beta Agent 配置（使用 OpenAIConfig 兼容硅基流动）
    config = OpenAIConfig(
        model=USE_MODEL,
        api_key=USE_API_KEY,
        base_url=OPENAI_API_BASE or None,
    )

    # 创建 Beta Agent - Lead（任务分解专家）
    lead = Agent(
        name="Lead",
        config=config,
        system_message="""You are a task decomposition expert (Lead Agent).
Your responsibilities:
1. Analyze user requests and break them into clear sub-tasks
2. When you need a review, use the review_with_critic tool to ask the Critic agent
3. Integrate results and provide final answers

Communication style: Professional, concise, structured""",
    )

    # 创建 Beta Agent - Critic（质量审查专家）
    critic = Agent(
        name="Critic",
        config=config,
        system_message="""You are a quality review expert (Critic Agent).
Your responsibilities:
1. Review proposals or answers from Lead
2. Provide constructive feedback and improvement suggestions
3. Ensure output quality meets high standards
4. Identify potential logical flaws or errors

Communication style: Direct, objective, constructive""",
    )

    # 使用 subagent_tool 将 Critic 注册为 Lead 的工具（Agent-as-tool 模式）
    # 这是 AG2 Beta 的核心特性之一
    review_tool = subagent_tool(
        critic,
        name="review_with_critic",
        description="Ask the Critic agent to review a proposal or answer and provide improvement suggestions",
    )

    print("Running Beta Agent-as-tool mode...")
    print("\n[Step 1] Lead Agent receives task...")
    print("-" * 60)

    # Lead 使用 ask() 方法发起任务，Critic 作为工具被调用
    # ask() 是 Beta Agent 的原生异步方法
    print("[Step 2] Lead Agent uses review_with_critic tool (subagent_tool)...")
    reply = await lead.ask(task, tools=[review_tool])

    print("\n[Step 3] Beta reply received:")
    print("-" * 60)
    print("\n[OK] Beta mode completed!\n")

    # Beta Agent 返回的 reply 是一个结构化对象，包含 body 属性
    if reply and hasattr(reply, 'body'):
        print("=" * 60)
        print("FINAL RESULT (Beta reply.body)")
        print("=" * 60)
        print(reply.body)

    return reply


def run_beta_mode(task: str):
    """运行 Beta Agent-as-tool 模式的同步入口"""
    return asyncio.run(run_beta_mode_async(task))


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="AG2 Multi-Agent Demo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
运行模式:
  groupchat (默认)  使用 AG2 Legacy GroupChat 实现 Lead + Critic 群聊协作
  beta              使用 AG2 Beta Agent-as-tool 模式（展示 Beta 原生 Agent 能力）
        """,
    )
    parser.add_argument(
        "--mode",
        choices=["groupchat", "beta", "review"],
        default="groupchat",
        help="运行模式 (默认: groupchat)",
    )
    args = parser.parse_args()

    mode_name_map = {
        "groupchat": "GroupChat",
        "beta": "Beta Agent-as-tool",
        "review": "Code Review (4-Agent)",
    }
    mode_name = mode_name_map.get(args.mode, "GroupChat")
    print("\n" + "=" * 60)
    print(f"AG2 Multi-Agent Demo: {mode_name} Mode")
    print("=" * 60 + "\n")

    # Code Review 模式跳转到 code_review.py
    if args.mode == "review":
        print("[INFO] Redirecting to code_review.py ...\n")
        import code_review
        code_review.main()
        return

    demo_tasks = [
        "Analyze the core features of AG2 framework and provide code examples",
        "Design a multi-agent system architecture",
        "Explain multi-agent collaboration with real-world applications",
    ]

    print("Demo tasks:")
    for i, task in enumerate(demo_tasks, 1):
        print(f"   {i}. {task}")
    print()
    print(f"Running mode: {args.mode}\n")

    # 使用第一个任务
    task = demo_tasks[0]

    try:
        if args.mode == "beta":
            run_beta_mode(task)
        else:
            run_groupchat_mode(task)
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
