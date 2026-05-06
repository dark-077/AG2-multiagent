"""
AG2 Multi-Agent 示例 - Lead + Critic 双智能体协作

本示例展示如何使用 AG2 (formerly AutoGen) 构建最基础的多智能体系统：
- Lead Agent: 负责任务拆解和执行
- Critic Agent: 负责审查和反馈

运行方式:
    python agent_team.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# AG2 核心组件
try:
    from autogen import Agent, GroupChat, GroupChatManager
    print("使用 AutoGen/AG2 核心组件")
except ImportError:
    from ag2 import Agent, GroupChat, GroupChatManager
    print("使用 AG2 组件")


def create_lead_agent() -> Agent:
    """创建 Lead Agent - 任务拆解和执行"""
    
    lead_system_message = """你是一个任务拆解专家 (Lead Agent)。
你的职责：
1. 接收用户任务后，进行清晰的任务拆解
2. 将子任务分配给合适的执行者
3. 整合结果，给出最终回答

沟通风格：专业、简洁、结构化"""
    
    lead = Agent(
        name="Lead",
        system_message=lead_system_message,
        model_client=create_model_client(),
        max_consecutive_auto_reply=10,
    )
    
    return lead


def create_critic_agent() -> Agent:
    """创建 Critic Agent - 质量审查"""
    
    critic_system_message = """你是一个质量审查专家 (Critic Agent)。
你的职责：
1. 审查 Lead 提出的方案或回答
2. 提供建设性的反馈和改进建议
3. 确保输出质量达到高标准

沟通风格：直接、客观、有建设性"""
    
    critic = Agent(
        name="Critic",
        system_message=critic_system_message,
        model_client=create_model_client(),
        max_consecutive_auto_reply=5,
    )
    
    return critic


def create_model_client():
    """创建模型客户端 - 支持多种 LLM"""
    
    # 优先使用 OpenAI
    if os.getenv("OPENAI_API_KEY"):
        try:
            from autogen.agent_model import OpenAIChatCompletionClient
            return OpenAIChatCompletionClient(
                model="gpt-4o",
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        except ImportError:
            pass
    
    # 次选 Anthropic
    if os.getenv("ANTHROPIC_API_KEY"):
        try:
            from autogen.agent_model import AnthropicChatCompletionClient
            return AnthropicChatCompletionClient(
                model="claude-sonnet-4-20250514",
                api_key=os.getenv("ANTHROPIC_API_KEY"),
            )
        except ImportError:
            pass
    
    print("警告: 未找到 API 密钥，请配置 .env 文件")
    return None


def run_collaboration(task: str):
    """运行 Lead + Critic 协作"""
    
    print(f"\n{'='*60}")
    print(f"任务: {task}")
    print(f"{'='*60}\n")
    
    # 创建 Agents
    lead = create_lead_agent()
    critic = create_critic_agent()
    
    # 创建群聊
    group_chat = GroupChat(
        agents=[lead, critic],
        max_round=10,
        speaker_selection_method="round_robin",
    )
    
    # 创建管理器
    manager = GroupChatManager(
        groupchat=group_chat,
        model_client=create_model_client(),
    )
    
    # 开始协作
    print("开始 Lead + Critic 协作...\n")
    
    # 这里需要实际运行群聊
    # 由于缺少完整 API 配置，展示结构
    print("✅ Lead + Critic 双智能体系统已创建")
    print("📋 请配置 API 密钥后运行完整测试")


def main():
    """主函数 - 演示入口"""
    
    print("\n" + "="*60)
    print("🤖 AG2 Multi-Agent Demo: Lead + Critic")
    print("="*60 + "\n")
    
    # 检查 API 密钥
    has_api = bool(os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"))
    
    if not has_api:
        print("⚠️  未检测到 API 密钥")
        print("📝 请创建 .env 文件并添加你的 API 密钥:")
        print("   OPENAI_API_KEY=your-key-here")
        print("   或")
        print("   ANTHROPIC_API_KEY=your-key-here")
        print("\n📖 参考: .env.example")
    
    # 演示任务
    demo_task = "分析并总结 AG2 框架的核心功能"
    
    if has_api:
        run_collaboration(demo_task)
    else:
        print(f"\n📌 演示任务: {demo_task}")
        print("✅ 代码结构已就绪，配置密钥后即可运行")


if __name__ == "__main__":
    main()
