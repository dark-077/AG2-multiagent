# C5-AG2 仓库提交物

## 项目信息

- **GitHub 仓库**: https://github.com/dark-077/AG2-multiagent
- **挑战**: C5-AG2 多智能体编程挑战
- **赛道**: multi-agent 多智能体
- **作者**: 黄荣康
- **提交日期**: 2026-05-06

## 项目 tagline

**基于 AG2 框架的多智能体协作系统 - 展示 Lead + Critic 双智能体协同完成任务的能力**

## 技术栈

- AG2 (formerly AutoGen) 0.12.x
- Python 3.11+
- OpenAI GPT-4o / Anthropic Claude

## 核心功能

1. **Lead Agent**: 任务拆解和执行专家
2. **Critic Agent**: 质量审查和反馈专家
3. **GroupChat**: 多智能体群聊协作系统

## 运行方式

```bash
# 安装依赖
pip install -r requirements.txt

# 配置 API 密钥
cp .env.example .env
# 编辑 .env 添加你的 API 密钥

# 运行演示
python agent_team.py
```

## 项目结构

```
AG2-multiagent/
├── README.md              # 项目说明
├── requirements.txt       # 依赖列表
├── agent_team.py         # Lead + Critic 双智能体
├── hello_multiagent.py   # 基础示例
├── .env.example          # API 密钥模板
└── .gitignore            # Git 忽略配置
```

---

*基于 C5-AG2 多智能体挑战*
