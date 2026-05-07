# C5-AG2 拿来说明

## 项目信息

- **GitHub 仓库**: https://github.com/dark-077/AG2-multiagent
- **挑战**: C5-AG2 多智能体编程挑战
- **赛道**: multi-agent 多智能体

---

## Fork 来源

本项目为 **从零开始构建**，没有直接 Fork 特定仓库。

### 参考的资源和灵感来源：

1. **AG2 官方文档**
   - https://docs.ag2.ai/latest/
   - 提供了 AG2 框架的最新 API 文档和示例

2. **AG2 GitHub 仓库**
   - https://github.com/ag2ai/ag2
   - 参考了 agentchat 相关示例代码

3. **C5-AG2 挑战包**
   - 挑战规范定义了多智能体赛道的要求
   - 参考了 hello_multiagent.py 的基本结构

---

## 借鉴片段

### 1. 项目结构设计
- 参考挑战包中的 templates/ 目录结构
- 创建了 README.md, requirements.txt, .env.example 等标准文件

### 2. 双智能体架构
- Lead + Critic 模式参考了 AG2 官方示例
- 使用 GroupChat 进行多智能体协作

### 3. 代码模式
```python
# AG2 0.12.x 标准用法
from autogen import ConversableAgent, GroupChat, GroupChatManager

# 创建 Agent
lead = ConversableAgent(name="Lead", system_message=..., llm_config=...)

# 创建群聊
group_chat = GroupChat(agents=[lead, critic], max_round=10)

# 创建管理器
manager = GroupChatManager(groupchat=group_chat, llm_config=...)
```

---

## 原创内容

1. **黄荣康_C5-AG2_repo.md** - 仓库提交物说明
2. **黄荣康_C5-AG2_AI日志.md** - AI 迭代记录
3. **黄荣康_C5-AG2_拿来说明.md** - 本文档

---

##  Attribution 声明

本项目基于以下开源项目/资源构建：

- **AG2 (formerly AutoGen)** - Apache-2.0 License
  - https://github.com/ag2ai/ag2
  - AG2 是由 Chi Wang 和 Qingyun Wu 创建的开源多智能体框架

---

*拿来说明 - C5-AG2 多智能体挑战*
