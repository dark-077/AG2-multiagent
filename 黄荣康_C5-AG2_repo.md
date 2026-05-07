# C5-AG2 仓库提交物

## 项目信息

- **GitHub 仓库**: https://github.com/dark-077/AG2-multiagent
- **挑战**: C5-AG2 多智能体编程挑战
- **赛道**: multi-agent 多智能体
- **作者**: 黄荣康
- **提交日期**: 2026-05-07

## 项目 tagline

**AG2 Multi-Agent: 双模式智能体协作系统 — 从 Legacy GroupChat 到 Beta Agent-as-tool**

基于 AG2 (formerly AutoGen) 构建的多智能体协作系统。同时支持两种运行模式：
- `--mode groupchat`: 使用 AG2 Legacy GroupChat 实现 Lead + Critic 平等对话协作
- `--mode beta`: 使用 AG2 Beta Agent 原生 Agent-as-tool 模式，Critic 作为 Lead 的 sub-tool

## 技术栈

- AG2 (formerly AutoGen) 0.12.x（含 Beta 组件）
- Python 3.11+
- 硅基流动 API (SiliconFlow) - Qwen2.5-72B-Instruct
- 支持 OpenAI API 兼容格式（只需配置 base_url）

## 核心功能

### 双模式运行

| 特性 | GroupChat 模式 | Beta Agent-as-tool 模式 |
|------|---------------|------------------------|
| 底层 API | `ConversableAgent` + `GroupChat` | `autogen.beta.Agent` |
| 协作方式 | 平等对话（round_robin） | 主从协作（Lead 调用 Critic） |
| 运行命令 | `python agent_team.py` | `python agent_team.py --mode beta` |

### 1. Lead Agent
- 任务拆解和执行专家
- 分析用户请求并分解为子任务
- 协调其他 Agent 完成工作
- 整合结果并提供最终答案

### 2. Critic Agent
- 质量审查和反馈专家
- 评审 Lead 的提案或答案
- 提供建设性反馈和改进建议
- 确保输出质量符合高标准

### 3. 国产 API 兼容
- 支持硅基流动等国内 AI 服务商
- OpenAI API 兼容格式，易于切换
- 适合国内开发者使用

## 运行方式

```bash
# 克隆仓库
git clone https://github.com/dark-077/AG2-multiagent.git
cd AG2-multiagent

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境 (Windows)
.venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置 API 密钥
cp .env.example .env
# 编辑 .env 文件，填入你的 API 密钥

# 运行 GroupChat 模式
python agent_team.py

# 运行 Beta Agent-as-tool 模式
python agent_team.py --mode beta
```

## 演示视频

> ⏳ 演示视频录制中...
>
> 完成后将在此处添加视频链接。

<!--
视频上传后请替换此占位符：
[演示视频下载链接](your-video-link-here)
-->

## 项目结构

```
AG2-multiagent/
├── README.md              # 项目说明
├── requirements.txt       # 依赖列表
├── agent_team.py          # Lead + Critic 双智能体协作（双模式）
├── hello_multiagent.py    # 基础示例
├── .env                   # API 密钥配置（不提交）
├── .env.example           # API 密钥模板
├── ATTRIBUTION.md         # 借鉴来源说明
├── C5-AG2_AI日志.md       # AI 迭代日志
├── C5-AG2_拿来说明.md     # 项目说明文档
└── DEMO_GUIDE.md          # 演示视频录制指南
```

## 特色亮点

### 🤝 双模式人机协作
- GroupChat 模式：平等对话，模拟团队内部协作
- Beta 模式：主从协作，模拟上下级工作流

### 🔄 AG2 框架深度利用
- Legacy GroupChat + Beta Agent 双 API 同时使用
- subagent_tool Agent-as-tool 原生模式
- 对比展示 AG2 框架的演进与灵活性

### 🌏 国产 API 优先
- 默认配置硅基流动，国内零门槛使用
- 注册即送额度，无需科学上网

## 应用场景

- 智能客服：Lead 处理请求 + Critic 质量把控
- 代码审查：Lead 生成方案 + Critic 审查反馈
- 文档撰写：Lead 负责写作 + Critic 审核润色
- 教学辅导：Lead 讲解知识 + Critic 补充纠正

---

*基于 C5-AG2 多智能体挑战*
