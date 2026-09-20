# AI研发提效专项——完整会话整理

> 说明：以下整理当前会话中可见的用户与助手内容，按讨论演进顺序归档。  
> 重点保留：AI提效总体方案、技术架构、知识进入模型、AI可承担的工作、第一阶段MVP、OpenSpec、CodeGraph、Business Knowledge、业务理解与安全变更、Business Knowledge 与 Spec 的关系。

---

# 1. 用户：现在公司内网有 OpenCode、DeepSeek V4、Skills、OpenSpec，怎么利用 AI 提效 200%+

## 用户原始问题

我现在在公司的内网，仅仅提供了opencode和deepseekv4以及一些skills，还有一些插件例如openspec。我现在怎么利用ai提效，目标是提效200%以上，目前我负责的这个系统规模很大，业务模块很多，关联性很强，但是缺少业务知识沉淀。

## 助手核心回答

核心不是单纯让 AI 多写代码，而是让 AI 承担：

- 找业务
- 找关联
- 找影响面
- 补测试
- 做文档
- 做审查
- 做知识沉淀

目标是把：

```text
需求
→ 理解业务
→ 定位系统
→ 分析影响范围
→ 设计方案
→ 编码
→ 测试
→ Review
→ 文档/知识沉淀
```

形成 AI 研发闭环。

### 关键判断

大型系统真正的瓶颈通常不是“编码速度”，而是：

- 业务理解成本
- 系统定位成本
- 影响分析成本
- 历史逻辑追溯
- 测试与 Review
- 业务知识依赖个人经验

### 建议建立 AI 知识层

业务知识不要只留在聊天记录里，应存在仓库中的文件里。

推荐：

```text
.ai/
├── system-overview.md
├── business-glossary.md
├── business-flows/
├── modules/
├── data-model/
├── architecture/
├── decisions/
└── rules/
```

第一阶段可以很简单：

```text
system-overview.md
business-glossary.md
modules/
business-flows/
```

### 四类 AI 角色

#### Scout
只负责找，不直接改：

- 找代码
- 找接口
- 找调用方
- 找数据库
- 找事件
- 找测试
- 找历史 commit

#### Architect
负责影响分析：

- 模块影响
- 调用链
- 数据影响
- 状态机
- MQ/Event
- 事务
- 兼容性
- 测试风险

#### Builder
负责：

- 编码
- 重构
- 测试
- 文档

#### Verifier
独立验证：

- 需求是否实现
- 边界条件
- 异常流程
- 兼容性
- 测试
- 回归风险
- Code Review

### 推荐工作流

```text
需求
↓
Scout
↓
系统地图
↓
Architect
↓
Impact Analysis
↓
OpenSpec / Spec
↓
Builder
↓
Test
↓
Verifier
↓
Knowledge Update
```

### 业务知识沉淀

建议建立：

- Business Glossary
- Business Flow
- Module Card
- Architecture Map
- 状态机
- 业务规则

例如 Module Card：

```markdown
# Payment Module

## Responsibility
负责支付流程和支付状态维护。

## Entry Points
- PaymentController
- PaymentMessageConsumer

## Main Tables
- payment
- payment_record

## Dependencies
- Order
- Account
- Risk

## Events
- PaymentCreated
- PaymentSucceeded
- PaymentFailed

## State Machine

CREATED
↓
PROCESSING
↓
SUCCESS
↓
REFUNDED

## Important Rules

1. SUCCESS 不允许重新支付
2. REFUNDED 不允许再次退款
3. 同一支付单必须幂等

## Known Risks

- duplicate callback
- timeout callback
- transaction + MQ consistency
```

### 不建议第一阶段直接做复杂 RAG

优先：

```text
Markdown
+
代码搜索
+
Git
+
结构化索引
+
OpenCode
+
DeepSeek
```

先解决：

> AI 能不能在正确的地方找到正确上下文。

---

# 2. 用户：要向领导汇报整个 AI 提效计划

## 用户要求

现在要向领导汇报整个AI提效的计划。

## 助手核心汇报框架

建议定位为：

# AI研发生产力升级专项

而不是简单的“AI编码工具推广”。

### 核心目标

> 以 AI 重构研发工作方式，推动研发整体交付效率提升 200%+。

注意：

200% 应作为挑战目标 / 专项目标，通过试点数据验证，而不是未经验证的承诺。

### 核心问题

1. 系统复杂度高
2. 业务知识没有形成组织资产
3. 研发流程有大量重复劳动
4. AI 目前更多被当作代码生成器

### 总体思路

从：

> AI写代码

升级到：

> AI参与整个研发生命周期

流程：

```text
业务需求
↓
AI需求理解
↓
AI系统侦察
↓
AI影响分析
↓
AI方案设计
↓
OpenSpec
↓
AI辅助实现
↓
AI测试
↓
AI Review
↓
AI知识沉淀
```

### 四层 AI 研发体系

#### 第一层：AI基础能力

- DeepSeek V4
- OpenCode
- Skills
- OpenSpec

#### 第二层：Agent

- Scout
- Architect
- Builder
- Verifier
- Knowledge

#### 第三层：Tool / Skill

- Code Search
- AST / Dependency
- Git
- DB
- API
- MQ
- Test
- Build
- OpenSpec

#### 第四层：Knowledge

- Code Knowledge
- Business Knowledge
- Engineering Knowledge

### 业务知识资产化

AI 需要访问：

- Business Glossary
- Business Flow
- Module Card
- System Map
- State Machine
- Business Rules

### 关键理念

> 模型负责推理，知识层负责企业私有上下文，Agent负责工具调用与执行。

### 指标体系

#### 效率指标

- 单需求耗时
- 分析耗时
- 编码耗时
- 测试耗时
- Review耗时
- 人均有效交付量

#### 质量指标

- 一次通过率
- Review返工率
- 测试覆盖
- 回归缺陷
- 线上缺陷

#### 知识资产指标

- 核心业务流程覆盖率
- 核心模块知识覆盖
- 业务术语覆盖
- 模块关系覆盖
- AI知识更新次数

### 试点

不要一开始全系统铺开。

选一个：

- 需求多
- 业务复杂
- 关联性强
- 知识不足
- 测试基础较好
- 容易量化

的核心业务域。

---

# 3. 用户：领导比较关注技术方案怎么实现

## 助手核心调整

汇报需要重点讲：

- 数据从哪里来
- AI如何获取上下文
- Agent如何协作
- 如何控制误改
- 如何验证效果
- 第一阶段具体做什么

### 总体技术架构

```text
开发人员
  ↓
OpenCode
  ↓
AI Agent Orchestrator
  ├── Scout
  ├── Architect
  ├── Builder
  ├── Verifier
  └── Knowledge
  ↓
Tool / Skill
  ├── Code Search
  ├── AST / Dependency
  ├── Git
  ├── DB / API / MQ
  ├── Build / Test
  └── OpenSpec
  ↓
Knowledge
  ├── Code Knowledge
  ├── Business Knowledge
  └── Engineering Knowledge
  ↓
DeepSeek V4
```

### 模型和周边能力的职责划分

| 能力 | 主要负责 |
|---|---|
| 自然语言理解 | DeepSeek |
| 代码理解 | DeepSeek + Code Search |
| 调用链分析 | Tool / AST |
| 模块关系 | Dependency Index |
| Git历史 | Git Tool |
| 数据库关系 | Schema Tool |
| 业务知识 | Knowledge Base |
| 工作流程 | Agent |
| 研发规范 | Skills |
| 变更控制 | OpenSpec |
| 代码执行 | OpenCode |
| 测试验证 | Build / Test |
| 风险控制 | Policy / Permission |
| 效果评估 | Evaluation Framework |

关键观点：

> 大模型只是推理引擎，不是整个 AI 研发系统。

### 知识层

第一阶段：

```text
.ai/
├── glossary/
├── business/
├── modules/
├── architecture/
└── rules/
```

正式知识先用 Git + Markdown 管理。

### Tool 层

建议提供：

```text
search_code()
search_symbol()
find_callers()
find_callees()
search_git()
get_diff()
get_db_schema()
find_api()
find_mq()
run_test()
run_build()
```

### Graph / Retrieval

理想状态：

```text
关键词检索
+
语义检索
+
结构图检索
```

但第一阶段不必直接搞复杂向量数据库和 Graph RAG。

### Agent

四个核心：

- Scout
- Architect
- Builder
- Verifier

### OpenSpec

放在：

```text
Scout
↓
Impact Analysis
↓
OpenSpec
↓
Implementation
↓
Verification
```

OpenSpec 是大型系统 AI 修改代码的“变更控制层”。

---

# 4. 用户：知识怎么进入模型，具体怎么做？

## 助手核心回答

先澄清：

> “知识进入模型”不等于“把知识训练进 DeepSeek”。

第一阶段不需要 Fine-tuning。

更现实的是：

> 模型不变，知识放在模型外面；每次任务来了，通过检索 + Tool Calling，把和当前任务相关的知识动态放进上下文。

即：

```text
User Task
↓
Retrieval / Tools
↓
Business Knowledge
Code Index
System Graph
↓
Relevant Context
↓
DeepSeek V4
```

### 四种方式

| 方式 | 第一阶段 |
|---|---|
| Prompt | ✅ |
| RAG / Retrieval | ✅ |
| Tool Calling | ✅ |
| Fine-tuning | ❌ |

### 例子

用户：

> 把订单取消时间从30分钟改成20分钟。

AI首先查询：

```text
search_code("30分钟")
search_code("order cancel")
search_config("cancel timeout")
search_callers("OrderCancel")
search_git_history("cancel timeout")
search_business_knowledge("订单取消")
```

得到：

```text
普通订单30分钟未支付自动取消
VIP订单60分钟
活动订单15分钟
Order
Payment
Inventory
Notification
OrderTimeoutJob
OrderService.cancelOrder()
OrderCancelledEvent
```

然后这些信息组成 Context：

```text
SYSTEM:
你是订单系统研发Agent。

BUSINESS KNOWLEDGE:
普通订单30分钟未支付自动取消。
VIP 60分钟。
活动15分钟。

CODE KNOWLEDGE:
OrderTimeoutJob.java
OrderService.cancelOrder()

EVENT:
OrderCancelledEvent

USER REQUEST:
把订单取消时间从30分钟改成20分钟。
```

### Context Builder

最终架构：

```text
Business Knowledge
+
Code Knowledge
+
Graph
+
User Requirement
+
History
↓
Context Builder
↓
DeepSeek V4
```

这一步就是“知识真正进入模型”的地方。

---

# 5. 用户：哪些事情是靠 AI 就能做好的？

## 助手核心结论

要分四档：

### 第一档：AI基本可以直接做好

- 代码搜索
- 方法/类解释
- 调用链整理
- Git历史总结
- CRUD代码生成
- 单元测试生成
- SQL编写
- DTO/VO/Mapper
- 重复代码重构
- 日志分析
- 编译错误修复
- 静态检查问题修复
- 文档生成
- Release Note

### 第二档：AI可以做大部分，人确认

- Impact Analysis
- 需求→技术方案
- OpenSpec生成
- Code Review
- 日志定位
- 历史知识检索
- 文档和知识沉淀
- 研发流程编排

### 第三档：AI分析，人决策

- 业务规则判断
- 核心架构设计
- 大范围重构
- 数据迁移方案
- 关键一致性取舍

### 第四档：不应让AI独立负责

- 重大业务规则最终决策
- 核心架构最终决策
- 高风险生产变更
- 破坏性数据库操作
- 安全策略最终决策
- 线上事故最终定责

### 一个判断标准

适合 AI 全自动的任务通常满足：

```text
输入明确
+
规则明确
+
输出明确
+
能自动验证
```

---

# 6. 用户：把关键汇报内容总结为一个 HTML

## 助手生成

已生成：

[AI研发提效专项技术方案_领导汇报版.html](sandbox:/mnt/data/AI研发提效专项技术方案_领导汇报版.html)

核心内容：

1. 核心判断
2. 总体技术架构
3. 知识如何进入模型
4. AI能做什么 / 人做什么
5. 标准AI研发闭环
6. 业务知识持续沉淀
7. 第一阶段MVP
8. 分阶段路线
9. 效果验证
10. 风险治理
11. 管理层需要支持的事项

---

# 7. 用户：第一个阶段具体怎么实现，Spec 文档内容有没有什么要求？

## 助手核心方案

第一阶段目标：

> 选择一个核心业务域，让一个真实需求从“需求输入”一直跑到“Spec → 代码 → 测试 → Review → 知识沉淀”。

例如：

```text
需求：
订单超时取消由30分钟调整为20分钟
↓
AI理解
↓
找订单模块、超时任务、配置、状态机、DB、MQ、测试、Git
↓
Impact Analysis
↓
OpenSpec
↓
人工确认
↓
AI修改
↓
测试
↓
Verifier
↓
Knowledge Update
```

### 推荐目录

```text
project/
├── .ai/
│   ├── project.md
│   ├── glossary/
│   ├── business/
│   ├── modules/
│   ├── architecture/
│   └── rules/
│
├── openspec/
│   ├── specs/
│   └── changes/
│       └── 2026-xxx-order-timeout/
│           ├── proposal.md
│           ├── specs/
│           ├── design.md
│           └── tasks.md
│
└── src/
```

### `.ai/` 与 `openspec/` 分工

```text
.ai/
= 当前系统是什么

openspec/
= 这次准备改什么
```

### 第一阶段三大核心 Skill

#### Understand

输出：

- 需求理解
- 相关业务规则
- 相关模块
- 相关代码
- 未知信息
- 需要确认的问题

#### Trace

输入：

```text
/trace OrderService.cancelOrder
```

输出：

- 入口
- 调用者
- 被调用者
- 数据库
- Event
- 测试
- 历史变更

#### Impact

输出：

- Direct Impact
- Indirect Impact
- DB Impact
- API Impact
- MQ / Event Impact
- Test Impact
- Risk

---

# 8. Spec 文档应该包含什么？

建议内部规范至少包含：

```markdown
# Change: XXX

## 1. Background
为什么做。

## 2. Goal
最终达到什么。

## 3. Scope
包含什么，不包含什么。

## 4. Requirements

### Requirement: XXX

系统 SHALL ...

#### Scenario: XXX

- WHEN ...
- AND ...
- THEN ...

## 5. Business Rules

BR-001 ...
BR-002 ...

## 6. Impact Analysis

### Modules
### Code
### Database
### API
### MQ/Event
### Cache
### Scheduler
### Tests

## 7. Technical Design

### Option A
...

### Decision
...

### Reason
...

## 8. Acceptance Criteria

AC-001 ...
AC-002 ...

## 9. Risks

RISK-001 ...

## 10. Open Questions

Q-001 ...
```

### Spec的重要原则

不要写成：

> “把某个 Java 文件第235行的30改成20”。

而应该描述：

> **系统行为改成什么样。**

例如：

```text
Requirement:
系统 SHALL 在普通订单创建后20分钟仍未支付时，
自动将订单状态变更为 CANCELLED。

Scenario:
WHEN 普通订单创建时间超过20分钟
AND 支付状态不是 SUCCESS
THEN 订单进入 CANCELLED
AND 发布 OrderCancelledEvent
```

### Spec 分级

#### L1 简单需求

- Requirement
- Scenario
- Acceptance

#### L2 中等需求

增加：

- Impact
- Technical Design
- Test

#### L3 高风险需求

完整：

- Scope
- Impact
- Design
- Test
- 人工审批

---

# 9. 用户：这些都可以用 AI 实现吗？

## 助手结论

大部分可以。

但要区分：

### AI能否开发这些东西

> 大部分可以。

### 运行后是否应该完全自动

> 不可以。

尤其：

- 业务事实
- 架构决策
- 权限
- 生产变更
- 最终验收

需要人工。

### 可以 AI 实现的

| 建设内容 | AI可否开发 | 人负责 |
|---|---|---|
| `.ai/`知识目录 | ✅ | 定规范 |
| `project.md` | ✅ | 校验 |
| Business Glossary | ✅ 初稿 | 业务确认 |
| Business Flow | ✅ 初稿 | 业务确认 |
| Module Card | ✅ | 抽查 |
| Code Search | ✅ | 验收 |
| Trace | ✅ | 验收 |
| Impact | ✅ | 最终判断 |
| OpenSpec模板 | ✅ | 定规则 |
| Builder | ✅ | 控权限 |
| Verifier | ✅ | 最终验收 |
| Knowledge Update | ✅ | 确认事实 |
| Benchmark | ✅ | 定指标 |

### 重要原则

> AI可以挖知识，但不能凭空创造企业事实。

---

# 10. 用户：每一项怎么用 AI 实现？

## 助手建议统一模型

任何一个 AI 能力，都按：

```text
用户任务
↓
Skill / Agent
↓
Tools
↓
Knowledge / Context
↓
DeepSeek V4
```

### `.ai/`知识体系

让 OpenCode：

```text
扫描代码仓库
识别：
目录
业务模块
核心Controller/Service/Repository
数据库
MQ/Event
定时任务
核心配置
模块依赖
README / 文档
Git历史
```

自动生成：

```text
.ai/
├── project.md
├── modules/
├── business/
├── glossary/
└── architecture/
```

### Business Glossary

从：

```text
代码
+
需求文档
+
数据库
+
接口
+
测试
+
Git
```

提取：

- 业务术语
- 代码术语
- 数据库术语
- 历史叫法
- 定义
- 证据
- Confidence

### Business Flow

AI搜索：

- Controller
- Service
- Event
- 状态字段
- DB
- Test

生成：

```text
创建订单
↓
待支付
↓
支付成功
↓
履约
↓
完成
```

同时找异常：

- 支付失败
- 支付超时
- 重复支付
- 订单取消
- 退款
- 消息失败

### Module Card

自动分析：

- 职责
- Entry Points
- Core Classes
- Core Tables
- Dependencies
- Events
- State Machine
- Business Rules
- Tests
- Known Risks

### Code Search

用：

```text
ripgrep / grep
```

实现：

```text
search_code
```

### Symbol Search

使用：

- AST
- LSP
- Tree-sitter
- 语言专用解析能力

### Trace

通过：

```text
search_symbol
find_definition
find_callers
find_callees
find_db
find_events
find_tests
search_git_history
```

最终形成：

- 入口
- 调用者
- 被调用者
- 数据
- Event
- 测试
- 历史

### Impact

组合：

```text
Graph Traversal
+
Semantic Reasoning
+
Business Knowledge
```

流程：

```text
find_symbol
find_callers
find_callees
find_db_usage
find_event_producers
find_event_consumers
find_config
find_scheduler
find_tests
search_business_knowledge
↓
DeepSeek
↓
Impact Analysis
```

### OpenSpec

流程：

```text
需求
↓
Understand
↓
Trace
↓
Impact
↓
OpenSpec
```

生成：

- proposal
- spec
- design
- tasks

### Builder

输入：

```text
Requirement
+
Spec
+
Impact
+
Relevant Code
+
Business Knowledge
```

循环：

```text
Plan
→
Edit
→
Test
→
Fix
→
Test
```

### Verifier

输入：

```text
Spec
Git Diff
测试结果
相关代码
```

检查：

- Spec是否实现
- 是否漏改
- 是否过度修改
- 异常流程
- 边界条件
- 并发
- 事务
- 测试

### Knowledge Update

每次 Git 提交：

```text
Git Diff
↓
Knowledge Agent
↓
判断：
业务规则？
状态机？
新事件？
接口？
模块依赖？
数据库？
↓
生成Knowledge Update Proposal
↓
人工确认
↓
写入.ai/
```

### Benchmark

准备历史需求：

```text
需求
最终修改文件
真实影响模块
最终方案
测试
开发时间
```

让AI重新执行，与真实结果比较：

- Impact Recall
- File Recall
- Test Recall
- First Pass Success
- Time Saved

---

# 11. 用户：我还有 Code Graph

## 助手重新判断

Code Graph 会极大简化第一阶段。

之前规划的：

- AST
- Dependency Graph
- Trace
- Call Graph

如果 Code Graph 已经提供，就不需要重新造。

架构应该变成：

```text
OpenCode
↓
DeepSeek V4
↓
CodeGraph
↓
Business Knowledge
↓
Git
↓
Context Builder
↓
OpenSpec
↓
Builder / Verifier
```

核心理念：

> Code Graph 解决“系统实际上怎么连接”，Business Knowledge 解决“这些连接在业务上意味着什么”，DeepSeek 负责把两者结合起来推理。

---

# 12. 用户澄清：Code Graph 是 GitHub 上的开源项目

## 助手进一步调整

如果指的是 GitHub 上的 `codegraph-ai/CodeGraph`，那么它本身已经提供：

- symbol search
- callers / callees
- dependency graph
- call graph
- implementors
- related tests
- impact analysis
- get_ai_context
- get_edit_context
- pr_context
- memory_store
- memory_search
- memory_context
- 文档检索

并通过 MCP 面向 Agent 提供能力。

因此：

> **不要再自己造代码理解基础设施。**

### 直接复用 CodeGraph

Trace：

```text
CodeGraph
↓
callers / callees / graph traversal
↓
DeepSeek解释
```

Impact：

```text
CodeGraph analyze_impact
+
Business Knowledge
+
Git
+
DeepSeek
```

Edit Context：

```text
get_edit_context
```

PR Review：

```text
pr_context
```

### CodeGraph + Business Knowledge

CodeGraph可以告诉：

```text
OrderService.cancel()
↓
InventoryService.release()
↓
OrderCancelledEvent
```

Business Knowledge 告诉：

> 为什么 Cancel 必须 Release Inventory？

所以：

```text
Code Graph
+
Business Knowledge
```

才构成真正的业务上下文。

---

# 13. 用户：AI理解了代码以后，如何理解业务，并基于业务安全地完成一次变更？

## 助手核心回答

关键是建立：

# Business Context / Business Knowledge Layer

完整链路：

```text
用户需求
↓
Business Context Engine
↓
Business KB + CodeGraph + Git
↓
DeepSeek
↓
Business Understanding
↓
Impact Analysis
↓
OpenSpec
↓
人工确认/审批
↓
Builder
↓
Test + Verify
↓
Knowledge Update
```

### AI理解业务的5层

```text
业务术语
↓
业务规则
↓
业务流程
↓
业务状态 / 状态机
↓
跨模块业务约束
```

### Business Knowledge对象

建议至少：

```text
BusinessTerm
BusinessRule
BusinessFlow
StateMachine
BusinessInvariant
BusinessModule
```

### 知识来源

```text
需求文档
产品文档
接口文档
数据库
测试
代码
Git/PR
OpenSpec
人工确认
```

每条知识都应该有：

```text
source
evidence
confidence
status
```

例如：

```yaml
rule: "普通订单30分钟未支付自动取消"

status: CONFIRMED

source:
  - product_requirement
  - OrderTimeoutJob
  - OrderTimeoutTest

confidence: HIGH

evidence:
  - OrderTimeoutJob.java:120
  - OrderTimeoutTest.java:85
  - requirements/order-timeout.md
```

### 强制区分

```text
FACT
INFERENCE
UNKNOWN
```

示例：

```text
FACT:
OrderTimeoutJob 每5分钟运行一次。

FACT:
timeout = 30min。

INFERENCE:
订单实际取消时间可能是30~35分钟。

UNKNOWN:
业务是否允许这个延迟。
```

### Business Understanding 中间产物

可以生成：

```markdown
# Business Understanding

## User Intent
将普通订单支付超时时间从30分钟调整为20分钟。

## Confirmed Rules
1. 普通订单超时自动取消。
2. VIP规则不变。
3. 活动订单规则不变。
4. 取消后释放库存。
5. 取消事件幂等。

## Current Behavior
普通订单：
30分钟未支付 → CANCELLED

## Expected Behavior
普通订单：
20分钟未支付 → CANCELLED

## Unknown
1. 是否修改数据库配置？
2. 是否影响已有订单？
3. 是否立即处理已经超过20分钟的订单？
```

### OpenSpec成为变更契约

Spec不是：

> 改哪一行代码

而是：

> 系统改完后应该表现成什么样。

### 安全变更核心

Builder不能自由发挥。

应该：

```text
OpenSpec
↓
CodeGraph.get_edit_context
↓
CodeGraph.analyze_impact
↓
Builder
```

最后三层验证：

1. 代码验证
2. Spec验证
3. 业务回归验证

### Change Contract

建议形成：

```yaml
change: change-order-timeout

intent:
  "普通订单取消时间从30分钟改为20分钟"

scope:
  include:
    - Order
    - OrderConfig
  exclude:
    - VIP
    - PromotionOrder
    - PaymentSuccess

business_rules:
  - BR-001
  - BR-002
  - BR-003

expected_impact:
  modules:
    - Order
    - Inventory
  events:
    - OrderCancelledEvent

acceptance:
  - AC-001
  - AC-002
  - AC-003

risk:
  - concurrent_cancel
  - existing_orders
```

最终形成：

```text
需求
↓
业务理解
↓
影响分析
↓
变更契约
↓
受控实施
↓
独立验证
↓
知识回流
```

---

# 14. 用户：把刚刚这个过程也形成汇报 HTML

## 助手生成

[AI业务理解与安全变更闭环_领导汇报版.html](sandbox:/mnt/data/AI业务理解与安全变更闭环_领导汇报版.html)

重点包括：

- 四层事实模型
- Business Context Engine
- CodeGraph + Business Knowledge + Git
- Business Understanding
- OpenSpec 变更契约
- Builder
- 三层 Verifier
- Knowledge Flywheel
- AI Change Engineering

---

# 15. 用户：Business Knowledge 怎么用 AI 生成？Business Knowledge 怎么和 Spec 关联？也做 HTML

## 助手生成两份

### 1）Business Knowledge AI生成方案

[Business_Knowledge_AI生成方案_领导汇报版.html](sandbox:/mnt/data/Business_Knowledge_AI生成方案_领导汇报版.html)

重点：

```text
CodeGraph / 代码 / 文档 / 测试 / Git / Spec
↓
Knowledge Agent
↓
Candidate
↓
Evidence
↓
Human Review
↓
Confirmed Business Knowledge
↓
持续沉淀
```

并设计了：

- BusinessTerm
- BusinessRule
- BusinessFlow
- State / Invariant
- Evidence
- Confidence
- UNKNOWN / CANDIDATE / CONFIRMED
- Git + Markdown正式知识
- AI Memory
- Knowledge Flywheel

### 2）Business Knowledge 与 Spec 关联方案

[Business_Knowledge与Spec关联方案_领导汇报版.html](sandbox:/mnt/data/Business_Knowledge与Spec关联方案_领导汇报版.html)

核心：

```text
Business Knowledge
= 当前业务事实

OpenSpec
= 本次业务变更契约

CodeGraph
= 当前代码事实

Verifier
= 验证事实、契约和实际改动的一致性
```

建议使用：

### Knowledge ID

例如：

```text
BK-ORDER-001
普通订单支付超时规则

BK-ORDER-007
订单取消后的库存释放规则

BK-ORDER-011
已支付订单禁止自动取消
```

Spec 不复制规则，而是引用：

```text
## Business Context

References:
- BK-ORDER-001
- BK-ORDER-007
- BK-ORDER-011
```

然后：

```text
Knowledge
↓
Spec
↓
Implementation
↓
Verification
↓
Knowledge Update
```

形成双向闭环。

---

# 16. 当前最终推荐的整体方案

你当前拥有：

```text
DeepSeek V4
OpenCode
Skills
OpenSpec
CodeGraph
```

因此不需要重复建设大量底层能力。

## 现有基础设施负责

### DeepSeek V4
负责：

- 自然语言理解
- 代码推理
- 业务推理
- 方案生成
- 变更计划
- Knowledge候选生成

### OpenCode
负责：

- AI开发入口
- Agent执行
- Tool/Skill使用
- 代码修改
- 测试执行

### CodeGraph
负责：

- 代码结构事实
- Symbol
- Caller / Callee
- Dependency
- Impact
- Edit Context
- PR Context
- Code Memory

### OpenSpec
负责：

- proposal
- spec
- design
- tasks
- Change Contract

### Business Knowledge Layer
需要你们重点建设：

- BusinessTerm
- BusinessRule
- BusinessFlow
- StateMachine
- BusinessInvariant
- BusinessModule
- Knowledge ID
- Evidence
- Version
- 状态治理

---

# 17. 第一阶段最终推荐架构

```text
                         ┌───────────────┐
                         │   用户需求     │
                         └───────┬───────┘
                                 │
                                 ▼
                    ┌────────────────────┐
                    │ Business Context   │
                    │      Engine        │
                    └─────────┬──────────┘
                              │
               ┌──────────────┼──────────────┐
               │              │              │
               ▼              ▼              ▼
         Business KB       CodeGraph        Git
         业务事实           代码事实         历史事实
               │              │              │
               └──────────────┼──────────────┘
                              ▼
                         DeepSeek V4
                              │
                              ▼
                    Business Understanding
                              │
                              ▼
                       Impact Analysis
                              │
                              ▼
                         OpenSpec
                              │
                        人工确认/审批
                              │
                              ▼
                           Builder
                              │
                              ▼
                     Build / Test / Diff
                              │
                              ▼
                          Verifier
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
              Pass / Reject       Knowledge Update
```

---

# 18. 第一阶段具体工作优先级

因为已有 CodeGraph，应该砍掉：

```text
❌ 自建 AST
❌ 自建 Call Graph
❌ 自建 Dependency Graph
❌ 自建底层代码理解平台
```

重点投入：

## P0

```text
1. Business Knowledge
2. CodeGraph 与 OpenCode/MCP的深度接入
3. Business Context Engine
4. Understand
5. Impact Workflow
6. OpenSpec Workflow
7. Builder
8. Verifier
```

## P1

```text
9. Knowledge Update
10. Knowledge ID / Version
11. Evidence
12. Benchmark
```

## P2

```text
13. Hybrid Retrieval
14. Embedding / Reranker
15. Knowledge Graph
16. 更复杂的Agent协作
```

---

# 19. 最核心的领导汇报语言

可以用以下几句话概括整个方案：

> **不是让AI直接改代码，而是让AI先理解业务、识别影响、形成变更契约，再在受控范围内实施，并通过独立验证证明实际修改符合业务意图。**

> **CodeGraph解决AI对代码世界的理解，Business Knowledge解决AI对业务世界的理解，OpenSpec解决业务意图到技术变更的契约问题，Verifier解决实际结果与契约的一致性问题。**

> **模型负责推理，知识层负责企业私有上下文，Agent负责执行流程，工程工具负责提供确定性事实。**

最终目标：

# AI Change Engineering

即：

> 从 AI Coding 升级到 AI 能够安全地完成一次业务变更。

---

# 20. 当前生成的汇报文件

### 总体方案

[AI研发提效专项技术方案_领导汇报版.html](sandbox:/mnt/data/AI研发提效专项技术方案_领导汇报版.html)

### 业务理解与安全变更

[AI业务理解与安全变更闭环_领导汇报版.html](sandbox:/mnt/data/AI业务理解与安全变更闭环_领导汇报版.html)

### Business Knowledge 自动生成

[Business_Knowledge_AI生成方案_领导汇报版.html](sandbox:/mnt/data/Business_Knowledge_AI生成方案_领导汇报版.html)

### Business Knowledge 与 Spec 关联

[Business_Knowledge与Spec关联方案_领导汇报版.html](sandbox:/mnt/data/Business_Knowledge与Spec关联方案_领导汇报版.html)

