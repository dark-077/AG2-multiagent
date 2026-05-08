# 黄荣康_C5-AG2_repo

## 仓库信息

| 项目 | 内容 |
|------|------|
| **GitHub 仓库** | https://github.com/dark-077/AG2-multiagent |
| **挑战** | C5-AG2 多智能体编程挑战 |
| **赛道** | multi-agent 多智能体 |
| **作者** | 黄荣康 |
| **提交日期** | 2026-05-08 |

---

## 项目亮点

### 1. 双模式协作系统
- **GroupChat 模式**：AG2 Legacy 群聊协作，Lead + Critic 轮询对话
- **Beta Agent-as-tool 模式**：AG2 Beta 原生特性，Agent 作为工具被调用

### 2. 国产 API 支持
- 完整支持硅基流动 API（base_url 配置）
- 开箱即用的 Qwen2.5-72B-Instruct 模型

### 3. 完整文档
- README.md：5 分钟上手指南
- ATTRIBUTION.md：借鉴来源标注
- AI_LOG.md：7 轮迭代记录
- DEMO_GUIDE.md：视频录制脚本

---

## 快速运行

```bash
# 克隆仓库
git clone https://github.com/dark-077/AG2-multiagent.git
cd AG2-multiagent

# 配置 API（复制 .env.example 为 .env）
cp .env.example .env
# 编辑 .env，填入 OPENAI_API_KEY

# 运行 GroupChat 模式
python agent_team.py --mode groupchat

# 运行 Beta Agent-as-tool 模式
python agent_team.py --mode beta
```

---

## 演示视频

> 视频链接占位符（待上传后补充）

<!--
视频链接：https://your-video-url.com/C5-AG2_demo.mp4
时长：约 75 秒
内容：GroupChat + Beta Agent-as-tool 双模式演示
-->

---

## 文件清单

| 文件 | 说明 |
|------|------|
| `agent_team.py` | 主程序，Lead + Critic 双智能体协作 |
| `navigation.py` | 导航规划系统（5 Agent 协作） |
| `code_review.py` | 代码审查系统（4 Agent 并行审查） |
| `demo_run.py` | 演示模式（无需 API） |
| `DEMO_GUIDE.md` | 视频录制脚本 |
| `README.md` | 项目说明 |
| `ATTRIBUTION.md` | 借鉴来源 |
| `AI_LOG.md` | 迭代日志 |

---

## 核心技术点

1. **AG2 Beta Agent-as-tool**：`subagent_tool()` 将 Agent 注册为工具
2. **异步协作**：`asyncio` + `Agent.ask()` 异步模式
3. **LLM 配置**：`OpenAIConfig` + `base_url` 支持国产 API

---

## 致谢

- **AG2 Team**：开源多智能体框架
- **硅基流动**：稳定的国内 AI API 服务
- **Elite20**：C5-AG2 挑战组织

---

*本文档为 C5-AG2 多智能体挑战提交物*