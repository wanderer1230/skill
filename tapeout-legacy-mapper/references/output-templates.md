# 输出规范

## 目录布局

```
tapeout-knowledge/
├── README.md              最后写:导读 + 如何维护
├── 00_repo_map.md         S0
├── 01_objects.md          S2  逐业务对象:状态/规则/入口/产物
├── 02_dataflow.md         S3  数据流对账(四象限)
├── 03_main_flow.md        S4  主流程
├── 04_open_questions.md   S4  待确认清单
├── _seed/
│   ├── business_map.md    用户口述的业务地图(S0)
│   └── anchors.txt        锚点文件(S1)
└── _raw/                  probe 原始输出,不给人读,供复查与增量更新
    ├── recon.json
    └── probe.json
```

`_raw/` 和 `_seed/` 必须保留。`_raw` 让结论可复查;`_seed` 让下次梳理不用重新采集用户认知,只需在锚点文件上增补,是增量更新的前提。

## Front matter

每个文件顶部:

```yaml
---
generated_at: 2026-08-18
snapshot: "codebase mtime max 2026-07-30"
step: S3
scope: <本次梳理限定的范围,如"仅主线:数据提交→光罩订单">
confidence_summary:
  confirmed: 34
  inferred: 12
  user_asserted: 9
  guessed_deferred: 8
---
```

`snapshot` 是文档能活下去的前提:代码演进后,靠它判断这份文档过期到什么程度。不用 git 时记录梳理日期 + 代码库根目录下最新文件的 mtime(probe recon 的 `staleness_by_dir` 里有),两者一起足以判断新鲜度。

## 证据锚点格式

| 证据类型 | 写法 |
|---|---|
| 源文件 | `path/to/File.java:213` |
| 编排文件节点 | `path/to/Flow.logic#node47` 或 `#节点名` |
| 数据库 | `TABLE_NAME.COLUMN_NAME` |
| SQL 映射 | `path/to/Mapper.xml#statementId` |
| 配置 | `path/to/app.properties:key` |
| 前序产物结论 | `→01#批次` / `→02#F7` |

**每条正文结论都要有至少一个锚点。** 没有锚点的句子只能出现在明确标注的"推测"小节或 06 里。

## 置信度标注

行内用 `[C]` `[I]` `[U]` `[G]`,表格里单列。

- `[C] confirmed` —— 读过实现,证据直接支持
- `[I] inferred` —— 多处间接证据合理推断,**必须同时注明推断链**,例如"由字段名+错误文案+调用方共同推断"
- `[U] user-asserted` —— 来自用户业务地图,代码尚未印证。不是质疑用户,而是让后来人知道哪些结论有代码兜底、哪些依赖某次口述 —— 半年后这个区别非常重要
- `[G] guessed` —— 只有命名线索 → **不进正文,进 04_open_questions**

`[I]` 的推断链不能省。半年后有人质疑某条结论时,推断链决定了它是可以复核的假设,还是一句无法追溯的断言。

## Mermaid 使用

状态机用 `stateDiagram-v2`,流程用 `flowchart TD`,边界用 `flowchart LR`。

约定:
- 实线 = `confirmed`,虚线 = `inferred`
- `guessed` 的边**不画**
- 节点标签用业务名,技术名放在注释或表格里
- 图必须配一张明细表——图给直觉,表给证据。只有图没有表的产物是不可复核的

图的规模控制在 15 个节点以内。超了就拆分层:一张总图 + 若干张子图。塞满 40 个节点的图没人看得懂,等于没画。

## README.md 该写什么

S4 最后写,是给人的入口:

1. 这份文档覆盖了什么、**没覆盖什么**(scope 边界要写死)
2. 各文件导读:新人该按什么顺序读
3. 置信度总览与主要盲区
4. **维护约定** —— 改代码时怎么同步改文档;建议把这套文档放进代码仓库,与代码同一次提交
5. 生成方式:用了什么 skill、什么 commit,怎么增量重跑

## 语言

中文为主。术语首次出现时给出「中文(English / 代码标识)」三元组,之后可只用中文。产物里的代码标识**保持原样**,不要翻译或美化——它们是搜索代码时的检索键,改动会让文档失去可操作性。
