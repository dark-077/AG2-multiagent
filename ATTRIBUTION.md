# C5-AG2 ATTRIBUTION

## Fork 来源

本项目为 **从零创建** 的 AG2 多智能体项目，未直接 fork 现有仓库。

项目启发自以下资源：

| 资源 | 来源 | 用途 |
|------|------|------|
| AG2 官方文档 | https://docs.ag2.ai/ | API 参考和最佳实践 |
| AG2 Beta Examples | `references/ag2_docs/20_beta_example_hello_agent.mdx` | 单 Agent 基础架构 |
| AG2 Beta Research Squad | `references/ag2_docs/21_beta_example_research_squad.mdx` | 多 Agent 协作模式 |
| C5-AG2 Hackathon Starter | 挑战包自带 | 挑战规则和评分标准 |

---

## 借鉴片段

### 1. Agent 系统设计

**来源**: `references/ag2_docs/21_beta_example_research_squad.mdx`

Lead + Critic 双 Agent 协作模式借鉴自 research_squad 示例中的角色分工设计：

```
+--------------------------------+
| Agent | Role | Model | Tools |
|-------|------|-------|-------|
| Lead | Decomposes task, routes, integrates | Qwen2.5-72B | (none) |
| Critic | Adversarial review | Qwen2.5-72B | (none) |
+--------------------------------+
```

本项目将 Researcher 替换为 Lead + Critic 协作模式，符合 multi-agent track 要求。

### 2. GroupChat 配置

**来源**: AG2 legacy GroupChat 文档

群聊系统配置借鉴自 AG2 的 GroupChat 实现：

```python
group_chat = GroupChat(
    agents=[lead, critic],
    max_round=10,
    speaker_selection_method="round_robin",
    allow_repeat_speaker=False,
)
```

### 3. API 配置模式

**来源**: `references/ag2_docs/14_beta_model_configuration.mdx`

使用 `base_url` 参数支持 OpenAI 兼容 API 端点（包括硅基流动等国内服务商）：

```python
llm_config={
    "config_list": [
        {
            "model": "Qwen/Qwen2.5-72B-Instruct",
            "api_key": USE_API_KEY,
            "base_url": "https://api.siliconflow.cn/v1",
        }
    ],
}
```

---

## 自主开发部分

以下部分为本项目原创：

| 模块 | 说明 |
|------|------|
| Lead Agent 系统提示词 | 结合任务拆解专家角色定制 |
| Critic Agent 系统提示词 | 结合质量审查专家角色定制 |
| 群聊 round_robin 模式优化 | 针对双 Agent 场景优化 |
| 硅基流动 API 集成 | 国内服务商适配 |

---

## 致谢

- **AG2 Team** (Qingyun Wu, Vasiliy Radostev) - AG2 框架开发
- **Elite20** - C5-AG2 挑战策划和规则设计
- **硅基流动** - 提供稳定的国内 AI API 服务

---

*本 ATTRIBUTION.md 按照 C5-AG2 挑战要求编写，确保所有借鉴内容均有明确来源标注。*
