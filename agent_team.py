"""
AG2 Multi-Agent 示例 - Lead + Critic 双智能体协作

本示例展示如何使用 AG2 (formerly AutoGen) 0.12.x 构建多智能体系统。

架构：
- Lead Agent: 任务拆解和执行
- Critic Agent: 质量审查和反馈

运行方式:
    python agent_team.py

依赖:
    - ag2>=0.12.0
    - python-dotenv
    - openai (或其他 LLM 客户端)
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# AG2 核心组件 (AG2 0.12.x)
from autogen import (
    ConversableAgent,
    GroupChat,
    GroupChatManager,
)

# ============================================================
# 配置
# ============================================================

# 检查 API 密钥
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

if not OPENAI_API_KEY and not ANTHROPIC_API_KEY:
    print("❌ 错误: 未找到 API 密钥!")
    print("📝 请在 .env 文件中设置 OPENAI_API_KEY 或 ANTHROPIC_API_KEY")
    print("   参考 .env.example")
    sys.exit(1)

# 选择模型
USE_MODEL = "gpt-4o" if OPENAI_API_KEY else "claude-sonnet-4-20250514"
USE_API_KEY = OPENAI_API_KEY if OPENAI_API_KEY else ANTHROPIC_API_KEY

print(f"✅ 使用模型: {USE_MODEL}")

# ============================================================
# Agent 定义
# ============================================================

def create_lead_agent() -> ConversableAgent:
    """创建 Lead Agent - 任务拆解和执行"""

    lead_system_message = """你是一个任务拆解专家 (Lead Agent)。
你的职责：
1. 接收用户任务后，进行清晰的任务拆解
2. 将复杂任务分解为可执行的子任务
3. 协调其他 Agent 完成工作
4. 整合结果，给出最终回答

工作方式：
- 使用结构化方式拆解任务
- 明确每个子任务的责任和预期输出
- 确保最终回答完整、准确、有用

沟通风格：专业、简洁、结构化"""

    lead = ConversableAgent(
        name="Lead",
        system_message=lead_system_message,
        llm_config={
            "config_list": [
                {
                    "model": USE_MODEL,
                    "api_key": USE_API_KEY,
                }
            ],
            "temperature": 0.7,
        },
        max_consecutive_auto_reply=10,
        human_input_mode="NEVER",  # 不需要人工输入
        description="任务拆解专家，负责分析和分解复杂任务",
    )

    return lead


def create_critic_agent() -> ConversableAgent:
    """创建 Critic Agent - 质量审查"""

    critic_system_message = """你是一个质量审查专家 (Critic Agent)。
你的职责：
1. 审查 Lead 提出的方案或回答
2. 提供建设性的反馈和改进建议
3. 确保输出质量达到高标准
4. 识别潜在的逻辑漏洞或错误

工作方式：
- 客观、中立地评估方案
- 提出具体、可操作的改进建议
- 确认方案的优势和价值
- 必要时要求 Lead 重新考虑

沟通风格：直接、客观、有建设性"""

    critic = ConversableAgent(
        name="Critic",
        system_message=critic_system_message,
        llm_config={
            "config_list": [
                {
                    "model": USE_MODEL,
                    "api_key": USE_API_KEY,
                }
            ],
            "temperature": 0.5,  # 更低的温度，保持客观
        },
        max_consecutive_auto_reply=5,
        human_input_mode="NEVER",
        description="质量审查专家，负责评估和改进方案质量",
    )

    return critic


# ============================================================
# 群聊系统
# ============================================================

def create_group_chat(lead: ConversableAgent, critic: ConversableAgent) -> GroupChat:
    """创建群聊系统"""

    group_chat = GroupChat(
        agents=[lead, critic],
        max_round=10,  # 最多 10 轮对话
        speaker_selection_method="auto",  # 自动选择下一个发言者
        enable_clear_history=True,
        send_introductions=True,  # 发送自我介绍
    )

    return group_chat


def create_group_chat_manager(
    group_chat: GroupChat,
) -> GroupChatManager:
    """创建群聊管理器"""

    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config={
            "config_list": [
                {
                    "model": USE_MODEL,
                    "api_key": USE_API_KEY,
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
    print("🤖 AG2 Multi-Agent: Lead + Critic 协作")
    print("=" * 60)
    print(f"\n📋 任务: {task}\n")
    print("-" * 60)

    # 创建 Agents
    lead = create_lead_agent()
    critic = create_critic_agent()

    # 创建群聊
    group_chat = create_group_chat(lead, critic)

    # 创建管理器
    manager = create_group_chat_manager(group_chat)

    # 初始化群聊
    # 使用 manager 发起对话，初始消息发送给 lead
    chat_result = lead.initiate_chat(
        manager,
        message=task,
        clear_history=True,
    )

    print("-" * 60)
    print("\n✅ 对话完成!\n")

    # 打印结果摘要
    if hasattr(chat_result, 'summary'):
        print("📝 最终结果:")
        print(chat_result.summary)

    return chat_result


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数 - 演示入口"""

    print("\n" + "=" * 60)
    print("🤖 AG2 Multi-Agent Demo: Lead + Critic")
    print("=" * 60 + "\n")

    # 演示任务
    demo_tasks = [
        "分析 AG2 框架的核心功能，并给出代码示例",
        "设计一个多智能体系统的架构方案",
        "解释什么是多智能体协作，并列举实际应用场景",
    ]

    print("📚 演示任务列表:")
    for i, task in enumerate(demo_tasks, 1):
        print(f"   {i}. {task}")
    print()

    # 运行演示
    task = demo_tasks[0]  # 默认选择第一个任务

    try:
        run_collaboration(task)
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        print("\n💡 提示:")
        print("   1. 检查 API 密钥是否正确")
        print("   2. 检查网络连接")
        print("   3. 查看 above error message 获取更多信息")
        raise


if __name__ == "__main__":
    main()
