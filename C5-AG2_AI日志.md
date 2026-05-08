# C5-AG2 AI 迭代日志

## 项目信息

- **GitHub 仓库**: https://github.com/dark-077/AG2-multiagent
- **挑战**: C5-AG2 多智能体编程挑战
- **赛道**: multi-agent 多智能体

---

## AI 迭代记录

### 第 1 轮：项目初始化

**问题/任务**: 创建 AG2 多智能体项目结构

**AI 行为**:
- 使用 CodeBuddy AI 助手协助创建项目
- 初始化 GitHub 仓库 AG2-multiagent
- 创建基础项目结构（README.md, requirements.txt 等）

**结果**:
- ✅ 成功创建本地项目
- ✅ 推送到 GitHub
- ✅ 项目结构清晰

**反思**: 项目初始化顺利，GitHub 仓库创建遇到一些操作问题后解决

---

### 第 2 轮：完善 agent_team.py

**问题/任务**: 使用 AG2 0.12.x API 完善多智能体代码

**AI 行为**:
- 分析 AG2 0.12.x 最新 API 结构
- 阅读 autogen\agentchat\ 目录下的源码
- 理解 ConversableAgent、GroupChat、GroupChatManager 的用法

**结果**:
- ✅ 成功理解 AG2 0.12.x API
- ✅ 编写了 Lead + Critic 双智能体协作代码
- ✅ 代码包含完整的错误处理和配置检查

**反思**: AG2 0.12.x API 与旧版本有较大变化，需要参考官方文档和源码

---

### 第 3 轮：测试运行

**问题/任务**: 测试 agent_team.py 是否能正常运行

**AI 行为**:
- 检查 API 密钥配置
- 发现 OpenAI API 密钥为占位符，无法使用
- 改用硅基流动 API（国内 AI 服务商，支持 Qwen/DeepSeek 等模型）
- 修改 .env 配置，添加 OPENAI_API_BASE
- 修改 agent_team.py 所有 llm_config，添加 base_url 参数
- 运行 python agent_team.py 测试

**结果**:
- ✅ API 连接成功
- ✅ 硅基流动 Qwen2.5-72B 模型调用正常
- ✅ Lead + Critic 群聊协作正常运行
- ⚠️ 出现 GroupChat 警告（已修复为 round_robin 模式）

**反思**: 硅基流动是 OpenAI API 的良好替代方案，国内访问稳定，费用较低。配置时需要添加 base_url 参数指向硅基流动端点。

---

### 第 4 轮：优化群聊模式

**问题/任务**: 修复 GroupChat 警告，优化 agent 协作模式

**AI 行为**:
- 分析运行时警告：GroupChat is underpopulated
- 将 speaker_selection_method 从 "auto" 改为 "round_robin"
- 添加 allow_repeat_speaker=False 配置
- 修复 docstring 中的转义字符警告
- 移除文件名中的个人名字（黄荣康 → 通用命名）
- 提交并推送到 GitHub

**结果**:
- ✅ 群聊警告消除
- ✅ 3 个文件重命名完成
- ✅ 代码优化并推送

**反思**: round_robin 模式适合双 Agent 协作，避免同一 Agent 连续发言。文件名应保持通用性，便于项目分享。

---

### 第 5 轮：GitHub 整理

**问题/任务**: 整理仓库文件，移除个人信息

**AI 行为**:
- 使用 git mv 重命名文件
- 移除文件名中的"黄荣康"
- 提交更改到 main 分支
- 推送到 origin/main

**结果**:
- ✅ 完成文件重命名
- ✅ 提交推送成功

**反思**: 保持仓库文件名的通用性，便于开源分享和团队协作。

---

### 第 6 轮：添加 Beta Agent-as-tool 模式

**问题/任务**: 提升 AG2 Beta 组件的实际利用程度，展示 Agent-as-tool 高级特性

**AI 行为**:
- 分析 AG2 0.12.2 的 autogen.beta 源码结构，理解 Agent 类和 subagent_tool API
- 发现 `subagent_tool()` 可将一个 Beta Agent 注册为另一个 Agent 的工具函数
- 学习 Agent.ask() 异步方法和 tools 参数传递方式
- 阅读 autogen/beta/tools/subagents/subagent_tool.py 和 run_task.py 源码
- 在 agent_team.py 中添加 `--mode beta` 命令行参数，不破坏现有 GroupChat 逻辑
- 新增 `run_beta_mode()` 函数，使用 Beta Agent 原生 API 创建 Lead + Critic
- 使用 `subagent_tool()` 将 Critic 注册为 Lead 的工具（Agent-as-tool 模式）
- 更新 README.md，增加硅基流动配置说明、5分钟上手指南
- 补充 .env.example 的 OPENAI_API_BASE 示例
- 更新 ATTRIBUTION.md 记录 Beta Agent-as-tool 借鉴来源
- 创建 DEMO_GUIDE.md 视频录制脚本

**结果**:
- ✅ `--mode beta` 参数正常工作，不破坏现有功能
- ✅ Beta Agent-as-tool 模式展示 AG2 原生 Agent 协作能力
- ✅ Legacy GroupChat + Beta Agent-as-tool 双模式并存
- ✅ README 包含完整国产 API 配置说明
- ✅ .env.example 直接包含硅基流动配置模板
- ✅ DEMO_GUIDE.md 提供 60-90 秒视频录制脚本

**反思**: AG2 Beta 的 Agent-as-tool 模式与 Legacy GroupChat 代表了两种不同的多智能体协作范式：GroupChat 是平等对话，Agent-as-tool 是主从协作。两者各有适用场景，同时展示可体现对 AG2 框架的深入理解。subagent_tool API 设计简洁，将 agent 注册为 tool 后，Lead 在 ask() 时自动判断是否需要调用子 agent。

### 第 7 轮：Beta 模式增强与文档完善

**问题/任务**: 增强 Beta Agent-as-tool 模式展示，创建提交文件模板

**AI 行为**:
- 增强 agent_team.py 的 beta 模式，添加更详细的 Beta 原生特性展示
- 添加注释说明 AG2 Beta 的四大核心特性
- 创建 DEMO_GUIDE.md 视频录制指南
- 创建黄荣康_C5-AG2_repo.md 提交文件模板

**结果**:
- ✅ Beta 模式增加特性说明注释
- ✅ DEMO_GUIDE.md 提供完整视频脚本
- ✅ 提交文件模板就绪

**反思**: 文档完善和视频准备是提交前的重要步骤，清晰的演示脚本可大幅提升视频录制效率。

## 总结

| 阶段 | 状态 | 说明 |
|------|------|------|
| 项目初始化 | ✅ 完成 | 仓库创建，结构清晰 |
| Agent 开发 | ✅ 完成 | Lead + Critic 双智能体 |
| API 测试 | ✅ 完成 | 硅基流动 API 成功运行 |
| 群聊优化 | ✅ 完成 | round_robin 模式 |
| GitHub 整理 | ✅ 完成 | 文件重命名 |
| Beta Agent-as-tool | ✅ 完成 | 添加 --mode beta 参数，展示 Agent-as-tool 模式 |
| Demo 录制 | ⏳ 待做 | 录制 60-90 秒演示视频 |

---

*AI 迭代日志 - C5-AG2 多智能体挑战*
