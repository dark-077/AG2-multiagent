# AG2 Multi-Agent 示例 - 基础双智能体协作

本示例展示如何使用 AG2 构建一个最简单的 Lead + Critic 双智能体系统。

## 核心概念

| 角色 | 功能 |
|------|------|
| **Lead Agent** | 任务拆解、分配、总结 |
| **Critic Agent** | 审查反馈、质量把控 |

## 代码说明

```python
# 伪代码结构
lead = Agent(name="Lead", role="任务拆解")
critic = Agent(name="Critic", role="质量审查")

# Lead 提出方案 → Critic 审查 → Lead 改进 → ...
```

## 运行方式

```bash
python hello_multiagent.py
```

## 自定义

修改 `system_message` 和 `model_client` 来适配你的需求。
