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
- 硅基流动 API (SiliconFlow) - Qwen2.5-72B-Instruct
- 支持 OpenAI API 兼容格式（只需配置 base_url）

## 核心功能

1. **Lead Agent**: 任务拆解和执行专家
   - 分析用户请求并分解为子任务
   - 协调其他 Agent 完成工作
   - 整合结果并提供最终答案

2. **Critic Agent**: 质量审查和反馈专家
   - 评审 Lead 的提案或答案
   - 提供建设性反馈和改进建议
   - 确保输出质量符合高标准

3. **GroupChat**: 多智能体群聊协作系统
   - 采用 round_robin 发言模式
   - 支持最多 10 轮对话
   - 自动选择下一个发言者

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
# 编辑 .env 文件，填入你的 API 密钥：
# OPENAI_API_KEY=your-api-key
# OPENAI_API_BASE=https://api.siliconflow.cn/v1

# 运行演示
.venv\Scripts\python.exe agent_team.py
```

## 项目结构

```
AG2-multiagent/
├── README.md              # 项目说明
├── requirements.txt       # 依赖列表
├── agent_team.py         # Lead + Critic 双智能体协作
├── code_review.py        # 智能代码审查系统（4 Agent 并行）
├── DEMO_GUIDE.md         # 演示指南（含视频录制脚本）
├── hello_multiagent.py   # 基础示例
├── simple_test.py        # 简单测试脚本
├── check_deps.py         # 依赖检查脚本
├── .env                   # API 密钥配置（不提交）
├── .env.example           # API 密钥模板
├── C5-AG2_AI日志.md       # AI 迭代日志
├── C5-AG2_拿来说明.md     # 项目说明文档
└── .gitignore            # Git 忽略配置
```

## 特色亮点

### 🤝 人机共生协作模式
- Lead Agent 负责任务拆解和协调
- Critic Agent 提供质量审查
- 模拟真实工作中的上下级协作流程

### 🔄 群聊协作机制
- AG2 GroupChat 实现多 Agent 自动对话
- round_robin 模式确保公平发言
- 支持历史记录管理和上下文理解

### 🌏 国产 API 兼容
- 支持硅基流动等国内 AI 服务商
- OpenAI API 兼容格式，易于切换
- 适合国内开发者使用

## 应用场景

- 智能客服：Lead 处理请求 + Critic 质量把控
- 代码审查：Lead 生成方案 + Critic 审查反馈
- 文档撰写：Lead 负责写作 + Critic 审核润色
- 教学辅导：Lead 讲解知识 + Critic 补充纠正

---

## Demo 演示（代码审查系统）

### 运行方式

```bash
# 演示模式（无需 API，直接看效果）
python code_review.py --mode demo

# GroupChat 模式（需 API Key）
python code_review.py --mode groupchat

# Beta Agent-as-tool 模式（需 API Key）
python code_review.py --mode beta

# 从 agent_team.py 入口
python agent_team.py --mode review
```

### 演示模式输出示例

```
============================================================
Code Review System — DEMO Mode
============================================================

演示模式：展示 4 Agent 并行审查流程
------------------------------------------------------------
  [LinterAgent]    -> 审查代码风格和语法
  [SecurityAgent]  -> 扫描安全漏洞
  [PerfAgent]      -> 分析性能问题
  [LogicAgent]     -> 审查业务逻辑

ReviewerLead 正在汇总所有审查意见...

============================================================
FINAL CODE REVIEW REPORT
============================================================

【代码审查报告】

## 1. Linter Agent — 代码风格 & 语法
- [WARN] SQL 注入风险：直接拼接变量
- [WARN] conn 和 cursor 未使用 with 上下文管理器
- [WARN] 硬编码索引访问，应使用列名
- [WARN] 函数无类型注解

## 2. Security Agent — 安全漏洞
- [CRIT] SQL 注入漏洞
- [CRIT] password123 明文硬编码密码
- [HIGH] SMTP 认证使用明文密码
- [WARN] 数据库文件路径硬编码

## 3. Perf Agent — 性能 & 资源
- [CRIT] 循环内重复打开/关闭文件 100万次
- [WARN] 无批量操作
- [WARN] SMTP 连接未释放

## 4. Logic Agent — 业务逻辑
- [WARN] include_password=True 时返回密码字段
- [WARN] send_email 无重试机制
- [WARN] 缺少输入验证

## 总结
| 严重程度   | 问题数 |
| [CRIT] 严重 | 4      |
| [WARN] 警告 | 8      |
```

### 核心架构

```
代码审查流程：

用户提交代码
     │
     ▼
┌─────────────────────────────────────────┐
│           ReviewerLead（统筹）           │
├─────────────────────────────────────────┤
│  LinterAgent  │ SecurityAgent │ PerfAgent │ LogicAgent │
│  代码风格     │ 安全漏洞      │ 性能分析   │ 业务逻辑   │
└─────────────────────────────────────────┘
     │
     ▼
  最终审查报告（带严重程度分级）
```

### 功能特性

- **4 专项 Agent 并行审查**：Linter / Security / Perf / Logic 各司其职
- **3 种运行模式**：Demo（无需API）/ GroupChat / Beta Agent-as-tool
- **严重程度分级**：[CRIT] 严重 / [HIGH] 高危 / [WARN] 警告
- **实际应用**：可用于 PR review、代码质量检测、安全扫描

---

*基于 C5-AG2 多智能体挑战*
