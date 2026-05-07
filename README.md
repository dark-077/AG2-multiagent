# 🧠 AG2 Multi-Agent Project

> **C5-AG2 多智能体挑战 · multi-agent 赛道**  
> 基于 AG2 (formerly AutoGen) 构建的 Lead + Critic 双智能体协作系统，支持 GroupChat 和 AG2 Beta Agent-as-tool 两种运行模式。

## 📋 项目概述

| 项目 | 内容 |
|------|------|
| 挑战 | C5-AG2 多智能体编程挑战 |
| 赛道 | multi-agent 多智能体 |
| 框架 | AG2 (formerly AutoGen) 0.12.x |
| GitHub | https://github.com/dark-077/AG2-multiagent |
| 运行模式 | GroupChat（Legacy） / Beta Agent-as-tool |
| 作者 | 黄荣康 |

## 🎯 项目目标

基于 AG2 框架，构建一个多智能体协作系统，展示多个 AI Agent 协同完成复杂任务的能力。包含两种运行模式：

1. **GroupChat 模式** (`--mode groupchat`)：默认模式，使用 AG2 Legacy GroupChat 实现 Lead + Critic 群聊协作
2. **Beta 模式** (`--mode beta`)：使用 AG2 Beta Agent 原生能力，演示 Agent-as-tool 高级特性

## 🤖 技术栈

- **AG2 0.12.x**: 开源多智能体框架（含 Beta 组件）
- **Python 3.11+**: 编程语言
- **LLM**: 硅基流动 (SiliconFlow) Qwen2.5-72B-Instruct / OpenAI 兼容 API

## 📁 项目结构

```
AG2-multiagent/
├── README.md              # 项目说明（本文档）
├── requirements.txt       # 依赖包
├── agent_team.py          # Lead + Critic 多智能体协作（支持 --mode 切换）
├── hello_multiagent.py    # 基础双智能体示例
├── .env                   # API 密钥配置（不提交）
├── .env.example           # API 密钥模板
├── .gitignore             # Git 忽略配置
├── C5-AG2_AI日志.md       # AI 迭代日志
├── C5-AG2_拿来说明.md     # 项目说明文档
└── C5-AG2_repo.md         # 仓库提交物说明
```

## 🚀 5 分钟上手指南

### 1. 克隆仓库

```bash
git clone https://github.com/dark-077/AG2-multiagent.git
cd AG2-multiagent
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
# source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 API 密钥

复制 `.env.example` 为 `.env`，填入你的 API 密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 如果你使用硅基流动（国内推荐，无需科学上网）
OPENAI_API_KEY=sk-your-siliconflow-api-key
OPENAI_API_BASE=https://api.siliconflow.cn/v1

# 或者使用标准 OpenAI API
# OPENAI_API_KEY=sk-your-openai-api-key
# OPENAI_API_BASE=
```

> **💡 提示**：硅基流动注册即送免费额度，支持 Qwen/DeepSeek/GPT 兼容模型，国内可直接访问。  
> 注册地址：https://siliconflow.cn

### 5. 运行演示

```bash
# GroupChat 模式（默认）
python agent_team.py

# 或显式指定模式
python agent_team.py --mode groupchat

# Beta Agent-as-tool 模式
python agent_team.py --mode beta
```

## 📚 学习资源

- [AG2 官方文档](https://docs.ag2.ai/latest/)
- [AG2 GitHub](https://github.com/ag2ai/ag2)
- [AG2 Hackathon](https://ag2-hackathon.vercel.app)

## 📝 提交物

- [ ] `姓名_C5-AG2_repo.md` - 仓库链接 + tagline
- [ ] `姓名_C5-AG2_AI日志.md` - AI 迭代记录
- [ ] `姓名_C5-AG2_拿来说明.md` - Fork 来源说明
- [ ] `姓名_C5-AG2_demo.mp4` - 演示视频

## 👤 作者

- GitHub: [@dark-077](https://github.com/dark-077)
- 赛道: Multi-Agent 多智能体

---

*Built with ❤️ using AG2*
