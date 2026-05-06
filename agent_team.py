"""
AG2 Multi-Agent - Lead + Critic 双智能体协作

使用 AG2 (formerly AutoGen) 0.12.x 构建多智能体系统

运行方式:
    .venv\\Scripts\\python.exe agent_team.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# AG2 核心组件
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

def run_collaboration(task: str):
    """运行 Lead + Critic 协作"""
    print("\n" + "=" * 60)
    print("AG2 Multi-Agent: Lead + Critic Collaboration")
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
# 主函数
# ============================================================

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("AG2 Multi-Agent Demo: Lead + Critic")
    print("=" * 60 + "\n")

    demo_tasks = [
        "Analyze the core features of AG2 framework and provide code examples",
        "Design a multi-agent system architecture",
        "Explain multi-agent collaboration with real-world applications",
    ]

    print("Demo tasks:")
    for i, task in enumerate(demo_tasks, 1):
        print(f"   {i}. {task}")
    print()

    # 使用第一个任务
    task = demo_tasks[0]

    try:
        run_collaboration(task)
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
