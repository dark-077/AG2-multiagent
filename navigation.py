"""
AG2 Multi-Agent - 实时导航与路线规划系统

使用 AG2 GroupChat 实现多 Agent 协作：
  RoutePlanner  → 总控协调
  WeatherAgent  → 查询各地天气
  TransportAgent → 交通方案比选
  BudgetAgent   → 预算分配
  ScheduleAgent → 生成行程表

运行方式:
    python navigation.py
    python navigation.py --mode demo      # 演示模式（无需 API）
    python navigation.py --mode groupchat  # GroupChat 模式（需 API Key）
    python navigation.py --mode beta       # Beta Agent-as-tool（需 API Key）
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
# 示例任务（供演示使用）
# ============================================================

SAMPLE_TASK = "北京 -> 上海 -> 杭州出差，5天，预算1万元"

SAMPLE_RESULT = """
============================================================
实时导航与路线规划报告
============================================================

## 行程概览
- 出发地：北京
- 目的地：上海 -> 杭州
- 天数：5天
- 预算：10000元

## 分段行程

### Day 1：北京 -> 上海
- 交通：[高铁 G7] 4.5小时 / 二等座 553元
- 住宿：上海外滩酒店 380元/晚
- 天气：多云 18-25°C

### Day 2-3：上海（商务）
- 会议：浦东新区 09:00-17:00
- 午餐：推荐南京路小吃 50元
- 天气：小雨 20-24°C

### Day 4：上海 -> 杭州
- 交通：[高铁 G30] 1小时 / 二等座 73元
- 住宿：杭州西湖酒店 320元/晚
- 天气：晴 22-28°C

### Day 5：杭州 -> 北京
- 交通：[飞机 CA1701] 2小时 / 经济舱 680元
- 天气：晴

## 预算分配
| 项目     | 金额  |
|----------|-------|
| 交通     | 1556元 |
| 住宿(4晚)| 1400元 |
| 餐饮     | 800元  |
| 其他     | 244元  |
| ----------|-------|
| 合计     | 4000元 |

## 建议
- 提前预订高铁，周末票紧张
- 杭州4月天气较好，拍照效果佳
- 阿里参观需提前3天预约
"""


# ============================================================
# Agent 工厂函数（Legacy ConversableAgent）
# ============================================================

def create_route_planner() -> ConversableAgent:
    """Route Planner - 总控协调"""
    system = """You are the Route Planner - the orchestrator of a travel planning team.
Your team has 4 specialist agents:
  - WeatherAgent:     query weather at destinations
  - TransportAgent:   compare transport options (train, flight, bus)
  - BudgetAgent:      allocate budget across categories
  - ScheduleAgent:    generate day-by-day itinerary

Your job:
1. Analyze the travel request (origin, destinations, days, budget)
2. Coordinate all agents to gather info
3. Synthesize into a complete travel plan
4. Format with clear sections for each day

Be efficient and prioritize practicality."""
    return ConversableAgent(
        name="RoutePlanner",
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
        description="Travel planning coordinator",
    )


def create_weather_agent() -> ConversableAgent:
    """Weather Agent - 天气查询"""
    system = """You are the Weather Agent - an expert at checking weather forecasts.
Your responsibilities:
1. Query weather for given cities and dates
2. Provide temperature ranges and conditions
3. Give packing suggestions based on weather
4. Flag extreme weather concerns

Be concise and practical. Always include temperature ranges."""
    return ConversableAgent(
        name="WeatherAgent",
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
        description="Weather forecaster",
    )


def create_transport_agent() -> ConversableAgent:
    """Transport Agent - 交通比选"""
    system = """You are the Transport Agent - an expert at comparing transport options.
Your responsibilities:
1. Research train, flight, bus options between cities
2. Compare time, cost, and comfort
3. Recommend best options for different budgets
4. Note booking tips and pitfalls

Be practical and cost-conscious. Provide specific options with prices."""
    return ConversableAgent(
        name="TransportAgent",
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
        description="Transport comparison expert",
    )


def create_budget_agent() -> ConversableAgent:
    """Budget Agent - 预算分配"""
    system = """You are the Budget Agent - an expert at travel budget planning.
Your responsibilities:
1. Allocate budget across categories (transport, hotel, food, misc)
2. Find cost-effective options without sacrificing quality
3. Flag if budget is unrealistic for the trip
4. Provide per-day cost guidelines

Be practical. Show breakdown in a clear table."""
    return ConversableAgent(
        name="BudgetAgent",
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
        description="Budget planning expert",
    )


def create_schedule_agent() -> ConversableAgent:
    """Schedule Agent - 行程生成"""
    system = """You are the Schedule Agent - an expert at creating day-by-day itineraries.
Your responsibilities:
1. Create balanced daily schedules
2. Include travel time between locations
3. Suggest meal times and break periods
4. Add local attraction recommendations

Be realistic about time. Don't over-schedule days."""
    return ConversableAgent(
        name="ScheduleAgent",
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
        description="Itinerary planner",
    )


# ============================================================
# GroupChat 模式
# ============================================================

def run_groupchat_planning(task: str):
    """GroupChat 模式：RoutePlanner + 4 个专项 Agent"""
    print("\n" + "=" * 60)
    print("Navigation Planning System — GroupChat Mode")
    print("=" * 60)

    # 创建所有 Agent
    planner = create_route_planner()
    weather = create_weather_agent()
    transport = create_transport_agent()
    budget = create_budget_agent()
    schedule = create_schedule_agent()

    # 创建群聊（5个 Agent）
    group_chat = GroupChat(
        agents=[planner, weather, transport, budget, schedule],
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

    request = f"""Please plan this trip by coordinating your team:

{task}

Each specialist (WeatherAgent, TransportAgent, BudgetAgent, ScheduleAgent) should provide their findings.
After all info is gathered, synthesize into a complete travel plan with day-by-day itinerary."""

    print(f"\nTask: {task}\n")
    print("Starting travel planning...\n")
    print("-" * 60)

    result = planner.initiate_chat(
        manager,
        message=request,
        clear_history=True,
    )

    print("-" * 60)
    print("\n[OK] Planning completed!\n")

    if hasattr(result, 'summary'):
        print("=" * 60)
        print("TRAVEL PLAN")
        print("=" * 60)
        print(result.summary)

    return result


# ============================================================
# Beta Agent-as-tool 模式
# ============================================================

async def run_beta_planning_async(task: str):
    """Beta 模式：使用 AG2 Beta Agent-as-tool"""
    print("\n" + "=" * 60)
    print("Navigation Planning System — Beta Agent-as-tool Mode")
    print("=" * 60)

    config = OpenAIConfig(
        model=USE_MODEL,
        api_key=USE_API_KEY,
        base_url=OPENAI_API_BASE or None,
    )

    # Beta Agent 定义
    planner = Agent(
        name="RoutePlanner",
        config=config,
        system_message="""You are the Route Planner for travel planning.
Coordinate 4 specialist agents:
- WeatherAgent: weather forecasts
- TransportAgent: transport options
- BudgetAgent: budget allocation
- ScheduleAgent: day-by-day itinerary

Gather info from all agents and produce a complete travel plan.""",
    )

    weather = Agent(
        name="WeatherAgent",
        config=config,
        system_message="You are the Weather Agent. Provide weather info for cities and dates.",
    )

    transport = Agent(
        name="TransportAgent",
        config=config,
        system_message="You are the Transport Agent. Compare transport options with prices and times.",
    )

    budget = Agent(
        name="BudgetAgent",
        config=config,
        system_message="You are the Budget Agent. Allocate budget and find cost-effective options.",
    )

    schedule = Agent(
        name="ScheduleAgent",
        config=config,
        system_message="You are the Schedule Agent. Create practical day-by-day itineraries.",
    )

    # 注册 subagent tools
    weather_tool = subagent_tool(weather, name="check_weather", description="Query weather for a city")
    transport_tool = subagent_tool(transport, name="compare_transport", description="Compare transport options")
    budget_tool = subagent_tool(budget, name="plan_budget", description="Allocate travel budget")
    schedule_tool = subagent_tool(schedule, name="generate_schedule", description="Generate day-by-day itinerary")

    tools = [weather_tool, transport_tool, budget_tool, schedule_tool]

    request = f"""Plan this trip:

{task}

Ask specialists for weather, transport, budget, and schedule info, then provide a complete plan."""

    print(f"\nTask: {task}\n")
    print("Running Beta travel planning...\n")
    print("-" * 60)

    reply = await planner.ask(request, tools=tools)

    print("\n" + "-" * 60)
    print("\n[OK] Beta planning completed!\n")

    if reply and reply.body:
        print("=" * 60)
        print("TRAVEL PLAN")
        print("=" * 60)
        print(reply.body)

    return reply


def run_beta_planning(task: str):
    return asyncio.run(run_beta_planning_async(task))


# ============================================================
# 演示模式（直接输出预设报告，无需 API 调用）
# ============================================================

def run_demo_mode(task: str):
    """演示模式：展示导航规划系统的工作流程（无需 API）"""
    print("\n" + "=" * 60)
    print("Navigation Planning System — DEMO Mode")
    print("=" * 60)
    print(f"\nTask: {task}\n")
    print("-" * 60)

    agents = ["WeatherAgent", "TransportAgent", "BudgetAgent", "ScheduleAgent"]
    for agent in agents:
        print(f"  [{agent}] -> 正在查询{agent.replace('Agent', '')}信息...")
    print()
    for agent in agents:
        print(f"  [{agent}] -> 查询完成 [OK]")
    print()

    print("RoutePlanner 正在整合所有信息生成行程表...")
    print()

    print("=" * 60)
    print("TRAVEL PLAN")
    print("=" * 60)
    print(SAMPLE_RESULT)

    return None


# ============================================================
# 主函数
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="AG2 实时导航与路线规划系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
运行模式:
  demo      演示模式（无需 API，展示预设规划流程）
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
        "--task",
        type=str,
        default=SAMPLE_TASK,
        help="旅行规划任务描述",
    )
    args = parser.parse_args()

    print(f"\n[INFO] Task: {args.task}")
    print(f"[INFO] Mode: {args.mode}\n")

    try:
        if args.mode == "beta":
            run_beta_planning(args.task)
        elif args.mode == "groupchat":
            run_groupchat_planning(args.task)
        else:
            run_demo_mode(args.task)
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
