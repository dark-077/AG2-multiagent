# C5-AG2 Demo 视频脚本

> 时长：60-90 秒
> 主题：AG2 Multi-Agent Lead + Critic 协作演示

---

## 开场 (0:00-0:05) 🎬

**画面**：屏幕录制开始，VS Code 打开 `agent_team.py`

**配音**：
> "大家好，我是黄荣康。今天展示 C5-AG2 多智能体挑战作品：基于 AG2 框架的 Lead + Critic 双智能体协作系统。"

**切换**：展示 README.md 项目介绍

---

## 演示一：GroupChat 模式 (0:05-0:30) 💬

**画面**：终端运行 `python agent_team.py --mode groupchat`

**配音**：
> "首先看 GroupChat 模式。这是 AG2 Legacy 的群聊协作，Lead 和 Critic 以轮询方式对话。"

**展示**：
```
[OK] Using model: Qwen/Qwen2.5-72B-Instruct
...
Lead: 分析任务并拆解...
Critic: 提供审查意见...
...
[OK] Chat completed!
```

**配音**：
> "Critic 对 Lead 的分析进行质量审查，指出逻辑漏洞，Lead 根据反馈优化。这种对话循环直到达成共识。"

---

## 演示二：Beta Agent-as-tool 模式 (0:30-0:55) ⚡

**画面**：终端运行 `python agent_team.py --mode beta`

**配音**：
> "然后看 Beta Agent-as-tool 模式，这是 AG2 Beta 的核心特性。"

**展示**：
```
[Beta 原生特性]
  1. autogen.beta.Agent 异步创建
  2. subagent_tool() Agent-as-tool 注册
  3. Agent.ask() 异步工具调用
  ...
```

**配音**：
> "这里 Lead 将 Critic 注册为自己的工具。遇到需要审查的场景，Lead 自动调用 review_with_critic 工具。这代表了一种主从协作范式，与 GroupChat 的平等对话形成对比。"

---

## 技术亮点 (0:55-1:15) 🔥

**画面**：代码结构展示

**配音**：
> "技术亮点：
> 1. 支持硅基流动 API，国内可直接访问
> 2. 双模式并存：通过 `--mode` 参数自由切换
> 3. 完整错误处理和配置检查
> 4. Agent-as-tool 展示 Beta 原生协作能力"

**切换**：展示最终输出

---

## 结尾 (1:15-1:30) 🎬

**画面**：GitHub 仓库页面

**配音**：
> "项目已开源，仓库地址在 README 中。欢迎 star 和 Fork，感谢观看！"

---

## 录制清单

- [ ] 开场白台词
- [ ] GroupChat 运行输出
- [ ] Beta 模式运行输出
- [ ] 代码结构截图
- [ ] GitHub 仓库截图
- [ ] 配音/字幕

## 推荐工具

- **录屏**：OBS Studio / Windows Game Bar
- **剪辑**：CapCut /剪映
- **配音**：可先录音后同步

---

*脚本版本：v1.0 | 更新日期：2026-05-08*