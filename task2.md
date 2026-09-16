《第二章：智能体发展史》习题解答（第 1、2、4、5、6、7 题）

第 1 题：物理符号系统假说

1.1 “充分性论断”和“必要性论断”的含义

物理符号系统假说（Physical Symbol System Hypothesis, PSSH）把智能解释为对符号结构的表示、组合、搜索和变换。

充分性论断：只要一个系统是具备足够表达和操作能力的物理符号系统，它原则上就拥有产生通用智能行为所需的手段。形式化地说，可理解为“物理符号系统 ⇒ 有可能实现通用智能”。这里的“充分”是对能力条件的判断，并不表示任意一套符号规则都会自动产生智能。
必要性论断：任何能够表现出通用智能的物理系统，本质上都必须是某种物理符号系统。形式化地说，可理解为“通用智能 ⇒ 必然包含物理符号系统”。这是更强的排他性主张，因为它认为不存在完全绕开符号表示与操作的通用智能。

两者不可混淆：充分性回答“符号系统能不能实现智能”，必要性回答“智能是否只能由符号系统实现”。

结合本章内容，说明符号主义智能体在实践中遇到的哪些问题对该假说的"充分性"提出了挑战？

符号系统在封闭、规则清晰的领域表现出色，但要从“原则上足够”走到“现实中可构造”，会遇到下列困难：

1. 知识获取瓶颈：专家的大量知识是经验性、隐含性和情境化的，很难穷尽地写成 `IF-THEN` 规则。即使规则可写，采集、校验和维护的成本也会随领域规模迅速增长。
2. 常识问题：人类默认掌握大量背景知识，而符号系统只知道被明确编码的内容。开放世界中的对象、关系、例外和语境几乎不可能预先列完。
3. 框架问题：一次行动后，系统不仅要描述改变了什么，还要高效确定什么没有改变。若为每个动作枚举所有不变量，表示和推理的成本会非常高。
4. 脆弱性与覆盖盲区：输入只要偏离预设形式，规则就可能无法触发或触发错误；规则在封闭“积木世界”中成立，并不保证能迁移到噪声多、例外多的现实环境。
5. 组合爆炸：状态、规则和可能动作增多后，搜索空间往往呈指数增长。理论上存在解，并不等于在有限时间与算力内能找到解。
6. 感知与符号接地问题：真实世界首先提供像素、声音、触觉等连续信号。如何把它们可靠地映射成有意义的离散符号，本身就是困难问题。

因此，这些问题并没有严格地在逻辑上“证伪”充分性论断，却削弱了它作为工程路线的可操作性：一个体系即使理论上足够，也可能无法被人类以可承受的成本构造出来。

1.3 LLM 驱动的智能体是否符合 PSSH

较合理的结论是：**它部分符合，但不是经典符号主义的直接延续；现代 LLM 智能体更适合被称为神经—符号混合系统。**

- 从实现层看，计算机处理离散 token、程序指令、JSON 参数和工具返回值，因此整个系统当然包含物理符号操作。
- 从核心知识表示层看，LLM 的知识主要分布在连续的神经网络权重和激活中，不是人类可直接读取的规则库；其推断主要是数值计算，而非经典专家系统式的显式逻辑演绎。
- 从智能体工作层看，LLM 又会生成和操作自然语言、代码、计划、API 参数等显式符号，并能调用搜索器、计算器、数据库和规则引擎。因此，智能体外围表现出很强的符号处理特征。

所以，若对“符号系统”采用宽泛的计算主义定义，LLM 智能体可以被纳入 PSSH；若坚持经典定义——知识应以可解释的显式符号和规则存储——则纯 LLM 并不符合。LLM 的成功至少说明：显式手工规则不是实现智能的唯一有效工程路径，也使 PSSH 的“必要性”继续面临争论。


 第 2 题：MYCIN 与高风险领域的专家系统

2.1 除知识获取瓶颈和脆弱性外的阻碍因素

技术与临床因素

外部有效性不足：在一个医院、一个人群或一种数据条件下有效，不代表换医院、设备、检验标准或疾病谱后仍然有效。
输入数据质量：病历缺失、检验误差、术语不统一和录入延迟都会传播到诊断结果中。
不确定性校准不足：置信因子可以表达不确定性，但不等同于经过大样本验证、具有可靠校准度的临床概率。
动态更新困难：指南、药物、耐药谱和疾病流行情况持续变化，静态知识库容易过时。
系统集成困难：若不能与电子病历、检验、处方和医院流程顺畅集成，医生就要重复录入数据，实际使用成本过高。
缺少持续监测：上线后的性能漂移、异常病例与群体差异若无法被及时发现，风险会累积。

伦理、法律与社会因素

责任边界模糊：误诊造成伤害时，应由医生、医院、知识工程师还是软件厂商承担责任并不容易界定。
偏差与公平性：规则来源和验证样本若不能覆盖不同年龄、性别、族群和基础疾病人群，就可能造成系统性差异。
知情同意与患者自主：患者需要知道系统参与了决策，并有权要求人工解释、复核或申诉。
自动化偏误：医生可能因系统看似权威而过度依赖建议，也可能因不信任系统而完全忽略正确提醒。
可解释不等于可信：系统能打印出一条推理链，只能说明“按哪些规则得出结果”，不能自动证明规则正确、完整或适用于当前患者。
监管和临床证据门槛：高风险诊断软件需要明确适用范围、严格验证、变更管理和上市后监督。FDA 对临床决策支持尤其强调，医务人员应能独立审查建议依据，而不是主要依赖软件作出诊疗决策[^2]。

2.2 现代医疗诊断智能体的设计方案

1. 数据接入与质量控制层
   - 通过标准接口读取病史、检验、影像报告和用药记录；
   - 做单位统一、缺失值检测、异常值提示和数据来源追踪；
   - 不确定或缺失的关键数据应主动询问，不能自行补造。

2. 混合知识与推理层
   - 用规则引擎执行绝对禁忌证、药物相互作用、剂量上限等确定性约束；
   - 用经过临床验证的统计或机器学习模型估计风险；
   - 用检索增强生成（RAG）从最新指南、药品说明书和院内规范中检索证据；
   - LLM 负责整合信息、生成鉴别诊断和解释，但不得把自身参数中的“记忆”当作唯一证据。

3. 安全校验层
   - 对输出进行规则复核、冲突检测、剂量计算复算和证据一致性检查；
   - 展示数据缺口、模型适用范围、置信度以及“为什么不能确定”；
   - 对危急值、罕见病、孕产妇和儿童等高风险情形自动升级给专科医生。

4. 人机协作层
   - 输出候选诊断、支持证据、反对证据和建议的下一步检查，而不是只给单一结论；
   - 医生保留最终决策权；高风险操作必须人工确认；
   - 允许医生纠正结果，并记录纠正理由，用于后续审计和改进。

5. 验证与治理层
   - 在部署前进行回顾性验证、前瞻性临床验证、亚组公平性测试和安全压力测试；
   - 上线后监测误报、漏报、校准、漂移和真实临床结局；
   - 建立版本控制、完整审计日志、隐私保护、网络安全、事故上报和可回滚机制。

2.3 规则系统今天仍占优势的垂直领域

当问题同时具有“规则明确、变化可跟踪、错误代价高、需要逐条审计、训练数据不足”这些特征时，规则系统往往优于纯深度学习。例如：

安全联锁与工业控制：温度、压力或阀门达到阈值时必须执行确定动作，系统需要可验证的确定性，而不是概率猜测。
访问控制和合规策略：基于角色的权限、数据保留期、交易限额和审批条件通常是明确规范，规则输出可审计、可复现。
编译器、协议与格式校验：语法、类型、通信协议和报文格式具有正式定义，解析器和规则检查器比神经模型更可靠。
金融交易的硬约束：如额度、禁止名单、会计恒等式和部分监管报送规则。深度模型可负责风险排序，但硬约束仍适合规则执行。
医疗中的确定性安全检查：例如已知严重过敏、绝对禁忌证、明确剂量上限。规则可作为底线防护，但不能据此推导“整个诊断系统都应只用规则”。

最佳实践通常不是二选一，而是**规则系统负责不可违反的边界，学习系统负责模式识别和风险排序，人类负责高风险价值判断**。


第 4 题：“心智社会”与现代多智能体系统

4.1 `GRASP` 失效后的系统表现，以及去中心化的利弊

在教材的积木塔链路中，`GET-BLOCK` 依赖 `SEE-SHAPE → REACH → GRASP`。如果 `GRASP` 失效：

1. 视觉模块仍可能找到积木，机械臂也可能伸向目标；
2. 由于无法完成抓握，积木不能被搬运；
3. `ADD-BLOCK` 无法完成，`BUILDER` 可能反复重试、超时、报告失败，甚至陷入循环；
4. 整个搭塔目标最终失败。

这说明去中心化本身不等于容错。若只有一个 `GRASP` 且它是必经节点，它仍是功能上的单点故障。只有增加备用抓握模块、替代动作（推、吸附）、失败检测和重新规划，系统才真正具有韧性。

去中心化架构的优势：

- 模块专业化，容易局部开发、测试、替换和扩展；
- 多个模块可以并行工作，减少中央控制器的瓶颈；
- 加入冗余和动态重分配后，可隔离局部故障；
- 局部规则的组合可能产生设计者未显式编写的有效行为，即“涌现”。

去中心化架构的劣势：

- 局部正确不保证全局正确，可能产生冲突、死锁、循环和资源竞争；
- 系统级行为难以预测、解释和形式化验证；
- 通信、同步和一致性会产生额外开销；
- 错误可能跨模块传播，定位根因比单体系统更困难；
- 若缺少共同目标、协议和仲裁机制，各模块可能各自优化却损害整体结果。

4.2 与 CAMEL-Workforce、MetaGPT、CrewAI 的关联和差异|

共同点在于：都反对把所有能力塞进单一、不可分割的“全能核心”，强调角色分工、消息交互和整体能力由协作产生。现代框架确实继承了“社会化智能”的思想。

不同点在于：现代框架中的每个 agent 往往都由强大的 LLM 驱动，已经拥有语言理解、推理和工具调用能力；并且实际工程系统常使用中央协调器、管理者或固定工作流，并非明斯基意义上的完全去中心化。CAMEL 官方文档明确描述了任务分解、协调器分配、执行和故障恢复的生命周期[^5]；MetaGPT 用 `Agents + Environment + SOP + Communication + Economy` 概括多智能体系统[^6]；CrewAI 则把 agents、tasks 与顺序/层级 process 组合成 crew[^7]。

 4.3 LLM 时代是否使“心智社会”过时

没有过时，但应从“弱个体组成强整体”扩展为“能力较强的个体通过结构化协作形成更可靠的整体”。

理由如下：

- 系统中的检索器、解析器、权限检查器、测试器和监控器仍然可以是简单的“无心”过程；不是每个组件都需要 LLM。
- 单个 LLM 即使能力强，也仍受上下文窗口、工具权限、专业知识和可靠性限制，角色分工可以降低任务复杂度。
- 多个智能体可以进行交叉审查、提出反例和独立验证，从组织层面补偿单模型弱点。
- 现代 agent 内部本身也可被理解为许多子过程的组合：感知、记忆、检索、规划、执行和反思共同构成整体行为。

不过，不能简单地认为“智能体越多越聪明”。多智能体会增加成本、延迟、错误传播和共识幻觉。如果任务可以由一个模型加确定性工具稳定完成，增加多个角色未必有收益。“心智社会”今天更有价值的是其**模块化、协作和涌现的设计视角**，而不是要求每个系统都必须采用完全去中心化的大量 agent。


第 5 题：强化学习与监督学习

5.1 AlphaGo 的“试错学习”机制


训练过程可概括为：

1. 当前策略与自身或其他版本对弈；
2. 在每个局面选择动作并得到新的棋盘状态；
3. 一局结束后，根据胜负得到正或负的反馈；
4. 将最终结果沿对局轨迹回传，更新策略网络和价值估计，使导致胜利的行动序列更可能被选择；
5. 新策略继续生成更高质量的对局，再次训练，形成“自我对弈—评估—更新”的循环；
6. 实战时再把神经网络与蒙特卡洛树搜索结合，以评估和搜索候选落子。

需要作一个历史上的精确区分：原始 AlphaGo 先从专家棋谱做监督学习，再通过自我对弈强化学习提高；AlphaGo Zero 才从随机下法开始，只依赖规则、搜索和自我对弈学习。Google DeepMind 对这两条路线有明确说明。

5.2 强化学习为何适合序贯决策，与监督学习的数据差异

强化学习特别适合序贯决策，原因是当前动作会改变后续状态和可选动作，动作的好坏常常要到很久以后才能判断。其目标是最大化折扣累计回报：

因此它能处理三个核心问题：

延迟奖励与信用分配：最终成功由前面哪些动作贡献；
探索—利用权衡：是选择已知较好的动作，还是尝试可能更好的新动作；
状态分布随策略改变：智能体的行为会改变它未来看到的数据。


5.3 超级马里奥：两种方法分别需要什么数据

监督学习方案（行为克隆）需要大量人类或强智能体的游戏记录，每个样本至少包含：

- 当前画面或游戏状态；
- 此刻玩家采取的按键动作；
- 可选的关卡、剩余生命、分数等上下文。

模型学习“看到这个状态时模仿专家按什么键”。优点是起步快、训练稳定；缺点是标签成本高，模型只会模仿数据覆盖到的行为。一旦自身小失误使它进入训练数据从未出现的状态，误差可能连续累积。

强化学习方案需要可反复交互的游戏模拟器，以及状态、合法动作、终止条件和奖励函数。例如，向右推进、通过检查点和通关获得正奖励，死亡、超时或后退受到惩罚。智能体通过大量尝试自行采集轨迹。

对这个任务，强化学习更适合作为主体方法，因为游戏是典型的长时序控制问题，最终目标是通关而不是逐帧模仿。如果人类演示充足，最佳工程方案通常是先用监督学习或离线强化学习获得初始策略，再用在线强化学习自我改进；这样兼顾启动速度和超越演示者的可能性。

5.4 强化学习在 LLM 训练中的关键作用

预训练的下一个 token 预测目标教会模型“什么文本看起来可能出现”，却不直接等价于“什么回答最有帮助、最安全、最符合人的意图”。强化学习主要在后训练和对齐阶段发挥作用：

1. 人类编写高质量示范，先进行监督微调；
2. 人类对多个候选回答排序，用偏好数据训练奖励模型；
3. 把 LLM 视为策略，把生成的回答视为动作序列；
4. 用策略优化提高奖励，同时限制模型不要偏离基础模型过远；
5. 最终改善指令遵循、有用性、安全性和对话风格。

InstructGPT 是经典案例：它先收集示范，再收集回答比较来训练奖励模型，最后用 PPO 优化策略。强化学习的关键价值不是向模型灌输全部事实知识，而是把难以写成精确公式的人类偏好转化为可优化的反馈信号。

同时应注意：奖励模型可能继承标注者偏差，模型也可能“钻奖励的空子”。而且现代偏好优化不一定都采用严格意义上的在线强化学习，一些方法直接用偏好对做优化。因此，更准确的说法是：基于反馈的对齐是现代 LLM 后训练的关键组成，RLHF 是其中一条重要路线，而不是唯一方案。


第 6 题：预训练—微调范式

6.1 预训练如何缓解知识获取瓶颈

符号主义需要知识工程师逐条访谈专家，把知识写成事实、关系和规则。其瓶颈不只在于录入慢，还在于许多语言常识、模糊概念和经验规律很难显式表达。

预训练改变了知识获取的方式：模型从海量文本、图像或其他数据中，通过自监督目标自动发现统计规律，不再要求人为给每条知识打标签或编写规则。一份语料可以共同服务许多下游任务，微调只需较少的领域样本。因此，知识采集从“逐条人工编码”转为“规模化数据学习”。

两种知识表示的差别如下：

| 方面 | 符号主义 | 预训练模型 |
|---|---|---|
| 表示形式 | 显式符号、事实、逻辑关系、规则 | 分布在大量参数和向量激活中的隐式表示 |
| 获取方式 | 专家与工程师人工编码 | 从海量数据中自监督学习 |
| 可解释性 | 单条规则易检查和追踪 | 单个参数通常没有独立、稳定语义 |
| 扩展方式 | 增加和维护规则库 | 扩大和改善数据、模型与训练目标 |
| 对例外的处理 | 需显式补充规则 | 可通过统计相似性泛化，但可能产生幻觉 |
| 一致性 | 可施加强逻辑约束 | 知识可能矛盾、模糊或过时 |

“解决”在这里应理解为大幅缓解工程瓶颈，而不是彻底解决知识问题。预训练把人工编码成本转化成了数据治理、算力、评测、更新和可验证性问题。

6.2 互联网数据带来的问题与缓解方法

| 风险 | 可能后果 | 缓解措施 |
|---|---|---|
| 错误、谣言和低质量内容 | 模型复述错误事实或生成虚假依据 | 权威源加权、质量过滤、事实性评测、检索增强、要求引用与允许拒答 |
| 社会偏见和仇恨内容 | 对群体产生歧视或不公平表现 | 数据平衡与过滤、分群评测、红队测试、偏好对齐和人工监督 |
| 隐私与敏感信息 | 记忆或泄露个人数据 | 合法采集、PII 检测与删除、去重、差分隐私、安全审计和输出防护 |
| 著作权和许可不清 | 侵权争议、内容归属不明 | 记录数据来源与许可、尊重退出机制、使用授权数据、输出相似性检测 |
| 数据陈旧 | 回答滞后于现实 | 带版本的知识库、RAG、联网检索、持续更新，并给出知识截止时间 |
| 语言和地域不均衡 | 低资源语言与地区效果差 | 定向补充代表性数据、与当地专家共建评测、公开亚组性能 |
| 数据污染与重复 | 基准泄漏、过拟合、错误放大 | 近重复检测、训练/测试隔离、数据谱系管理和独立留出集 |
| 恶意内容与投毒 | 后门、错误行为或安全绕过 | 数据供应链审计、异常检测、对抗测试、最小权限和运行时监控 |
| 能源与资源消耗 | 高成本和环境负担 | 高效模型、稀疏化、蒸馏、复用基础模型及披露能耗 |

互联网规模带来的能力和风险是同一枚硬币的两面。NIST 的生成式 AI 风险框架把虚构、数据隐私、有害偏差、信息完整性和知识产权等列为需要贯穿生命周期治理的问题[^4]。有效治理不能只靠训练前清洗，还要覆盖训练、评测、部署、监测和退出的全过程。

6.3 该范式会不会被取代

我的判断是：**“一次大规模学习通用表示，再低成本适配任务”这一思想会长期存在，但今天的单次离线预训练加单次微调，会演化为更连续、更模块化的体系。**

可能的演进方向包括：

检索增强：把时效性事实放在外部知识库，参数负责语言与推理，减少频繁重训；
多模态和具身预训练：同时学习文本、图像、音频、视频和行动轨迹，形成更接近环境动力学的世界模型；
合成数据与自我改进：由模型生成练习、验证器筛选结果，再用高质量样本迭代训练；
神经—符号融合：神经网络处理模糊感知和自然语言，符号模块承担精确计算、约束和证明；
参数高效适配与模块路由：通过适配器、专家混合、提示和工具组合，避免为每项任务完整微调；
交互式智能体学习：模型不仅从静态语料学习，还从环境行动、工具结果和人类反馈中学习。

这些方向更像是扩展而非完全推翻预训练。只要获取通用能力仍需利用大规模共享数据，而下游任务又各不相同，“基础学习 + 任务适配”的两阶段抽象就仍有生命力；改变的会是数据模态、适配手段、更新频率和外部知识所占比例。

第 7 题：三个时代的智能代码审查助手

7.1 1980 年代：符号主义方案

可实现的系统更像“可配置的静态检查专家系统”：

1. 用词法分析器、语法分析器把源代码转换为抽象语法树；
2. 建立符号表、类型信息、控制流图和数据流图；
3. 把专家经验写成规则，例如未初始化变量、不可达代码、空指针风险、资源未释放、圈复杂度过高和命名规范违反；
4. 用推理机匹配规则，并输出规则编号、触发位置和修改建议；
5. 对 PR 的概括主要依赖文件类型、函数名、调用关系和提交模板，很难生成流畅、准确的自然语言总结。

主要困难：

- 不同语言、框架和项目惯例需要不同规则库，维护成本极高；
- 很多缺陷依赖业务语义、跨文件上下文和运行时行为，难以写成局部规则；
- 对别名、并发、动态绑定等问题进行精确静态分析成本很高，容易在漏报和误报之间权衡；
- 规则无法自然概括“这次改动为什么这样做”，也很难提出具有上下文的设计建议；
- 新型错误必须先由人发现、总结，再人工编码，系统不能从历史审查中自动学习。

因此它能承担 lint 和部分静态分析，却难以成为题目所描述的综合审查助手。

7.2 2015 年左右：无 LLM 的深度学习方案

系统可以采用“静态分析 + 多个专用学习模型”的组合：

- 用 CNN、RNN/LSTM 或早期代码表示学习模型编码 token 序列；
- 用 AST、控制流图和调用图提取结构特征；
- 用监督学习预测某次改动是否容易产生缺陷、是否应重点审查、应由谁审查；
- 用分类器识别代码异味和风险类型；
- 用序列到序列模型尝试生成提交摘要或简短评论；
- 继续让编译器、单元测试、lint 和静态分析器提供确定性证据。

所需训练数据包括历史 commit/PR diff、审查评论、缺陷标签、合并结果、测试结果和漏洞记录。相比 1980 年代，它能从大量案例中学习模式，减少手写规则并提升排序能力。

但它仍有明显局限：每个子任务通常要单独收集标签和训练模型；跨仓库泛化差；长代码和跨文件依赖难以建模；生成摘要容易空泛；模型很难进行多步推理，也不能主动调用工具验证自己的怀疑。因此系统仍以“风险打分和辅助分类”为主。

你会如何设计这个智能体的架构？它应该包含哪些模块
可按“感知—思考—行动—观察”闭环设计：

1. 感知与上下文构建

- 从代码托管平台读取 PR 描述、diff、提交历史、讨论和 CI 状态；
- 解析仓库结构、语言、依赖、AST、调用图和受影响文件；
- 从代码库检索相关定义、测试、设计文档、编码规范和历史相似 PR；
- 对大仓库进行分层摘要，确保关键上下文进入模型而不是简单截断。

2. 规划与任务分解

规划器先判断改动类型和风险，再拆成可验证的子任务，例如：

- 概括实现逻辑和影响范围；
- 检查正确性、边界条件、并发、安全和性能；
- 检查 API 兼容性、数据库迁移和依赖变化；
- 判断测试覆盖是否足够，并制定验证计划。

复杂 PR 可以由不同专长的审查角色并行分析，但应由一个汇总器去重、解决冲突并控制噪声。

3. 模型、记忆与知识

- LLM 负责语言理解、跨文件推理、解释和建议生成；
- 短期记忆保存当前 PR 的证据和待验证假设；
- 长期记忆保存项目规范、架构决策与被开发者接受或拒绝的历史建议；
- RAG 只检索与当前改动相关的代码和文档，并保留来源锚点。

4. 工具执行

在隔离沙箱中按最小权限运行：

- 编译器、类型检查、lint、静态分析和安全扫描；
- 现有测试、受影响测试选择、覆盖率分析和模糊测试；
- 必要时生成临时测试或最小复现，并实际执行；
- `git diff`、代码搜索、依赖漏洞库和性能基准。

工具结果返回模型后，智能体应修正原判断；没有工具或代码证据支持的问题，应降低置信度或不发布。

5. 输出、护栏和人机协作

- 输出分为 PR 摘要、影响范围、阻断问题、非阻断建议和测试缺口；
- 每条问题绑定准确的文件与行号，包含“证据—影响—修复建议—置信度”；
- 区分确定性工具发现与模型推测，避免把风格偏好说成 bug；
- 自动发布前设置严重度和置信度阈值，低置信度内容只作内部候选；
- 禁止智能体未经批准合并代码、访问生产密钥或执行不可信脚本；
- 由开发者作最终判断，接受/拒绝反馈进入评测数据，但不能未经审查就在线改写核心策略。

6. 评测与监控

- 离线指标：真实缺陷召回率、误报率、行号准确率、建议可执行性和摘要忠实度；
- 在线指标：开发者采纳率、被标记为无用的比例、审查时延和逃逸缺陷率；
- 对不同语言、仓库规模和安全级别分别评测，监控模型或代码分布变化。

7.4 三个时代的总体对比

| 时代 | 知识来源 | 上下文能力 | 主要产出 | 核心瓶颈 |
|---|---|---|---|---|
| 1980 年代符号主义 | 人工规则和程序分析理论 | 适合明确、局部、形式化关系 | lint、静态告警、模板化解释 | 规则获取与组合爆炸，缺乏业务语义 |
| 2015 年深度学习 | 带标签的历史代码与审查数据 | 能学统计模式，但长程和跨项目能力有限 | 风险预测、分类、专用摘要 | 标签昂贵、任务碎片化、泛化与解释弱 |
| 当前 LLM 智能体 | 预训练知识 + 仓库检索 + 工具证据 + 项目记忆 | 能理解自然语言要求，跨文件推理并迭代验证 | 综合摘要、缺陷假设、证据化建议和测试计划 | 幻觉、成本、安全、上下文选择和治理 |

任务从“几乎不可能”变为“可行”，并不是因为 LLM 单独替代了过去的技术，而是因为三类能力被组合起来：

1. 预训练提供通用语言、代码和世界知识，减少为每个仓库从零建模的成本；
2. LLM 提供自然语言理解、跨信息整合、任务分解和解释能力；
3. 工具调用让系统用编译、测试和静态分析验证推理，而不只靠生成；
4. 检索和记忆把通用模型适配到具体仓库；
5. 人类监督、权限边界和评测机制把概率模型控制在可接受的工程风险内。


习题2代码
import re
import random
import json
from pathlib import Path

MEMORY_FILE = Path(__file__).with_name("memory.json")

context={"age":None,
         "name":None,
         "gender":None,
}
def load_memory():
    """从 JSON 文件加载用户的结构化记忆。"""
    if not MEMORY_FILE.exists():
        return context.copy()

    try:
        with MEMORY_FILE.open("r", encoding="utf-8") as file:
            saved_context = json.load(file)

        # 只加载程序认可的字段
        return {
            key: saved_context.get(key)
            for key in context
        }
    except (json.JSONDecodeError, OSError) as error:
        print(f"Therapist: I could not load my memory: {error}")
        return context.copy()
    
def save_memory(context):
    """将结构化记忆保存到 JSON 文件。"""
    try:
        with MEMORY_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                context,
                file,
                ensure_ascii=False,
                indent=4
            )
    except OSError as error:
        print(f"Therapist: I could not save my memory: {error}")

load_context = load_memory()


rules = {
    r'I need (.*)': [
        "Why do you need {0}?",
        "Would it really help you to get {0}?",
        "Are you sure you need {0}?"
    ],
    r'Why don\'t you (.*)\?': [
        "Do you really think I don't {0}?",
        "Perhaps eventually I will {0}.",
        "Do you really want me to {0}?"
    ],
    r'Why can\'t I (.*)\?': [
        "Do you think you should be able to {0}?",
        "If you could {0}, what would you do?",
        "I don't know -- why can't you {0}?"
    ],
    r'I am (.*)': [
        "Did you come to me because you are {0}?",
        "How long have you been {0}?",
        "How do you feel about being {0}?"
    ],
    r'.* mother .*': [
        "Tell me more about your mother.",
        "What was your relationship with your mother like?",
        "How do you feel about your mother?"
    ],
    r'.* father .*': [
        "Tell me more about your father.",
        "How did your father make you feel?",
        "What has your father taught you?"
    ],
    r'I love (.*)': [
        "Why do you love {0}?",
        "What is it about {0} that you like?",
        "How long have you loved {0}?"
    ],
    r'I hate (.*)': [
        "Why do you hate {0}?",
        "What is it about {0} that you dislike?",
        "How long have you hated {0}?"
    ],
    r'I feel (.*)': [
        "Do you often feel {0}?",
        "When do you usually feel {0}?",
        "What other feelings do you have?"
    ],
    r'.*': [
        "Please tell me more.",
        "Let's change focus a bit... Tell me about your family.",
        "Can you elaborate on that?"
    ],
    
}


pronoun_swap = {
    "i": "you", "you": "i", "me": "you", "my": "your",
    "am": "are", "are": "am", "was": "were", "i'd": "you would",
    "i've": "you have", "i'll": "you will", "yours": "mine",
    "mine": "yours"
}
    
def swap_pronouns(phrase):
    """
    对输入短语中的代词进行第一/第二人称转换
    """
    words = phrase.lower().split()
    swapped_words = [pronoun_swap.get(word, word) for word in words]
    return " ".join(swapped_words)

def update_memory(user_input):
    """
    从用户输入中提取姓名、年龄和职业。

    返回：
        (字段名, 字段值)，如果没有提取到信息则返回 None。
    """

    # 识别姓名，例如：
    # My name is Alice.
    # You can call me Alice.
    name_patterns = [
        r"\bmy name is ([a-zA-Z][a-zA-Z '-]*)[.!?]?$",
        r"\byou can call me ([a-zA-Z][a-zA-Z '-]*)[.!?]?$",
    ]

    for pattern in name_patterns:
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            context["name"] = name
            save_memory(context)
            return "name", name

    # 识别年龄，例如：
    # I am 22 years old.
    # My age is 22.
    age_patterns = [
        r"\bI am (\d{1,3}) years old\b",
        r"\bmy age is (\d{1,3})\b",
    ]

    for pattern in age_patterns:
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            age = match.group(1)
            context["age"] = age
            save_memory(context)
            return "age", age

    # 识别职业，例如：
    # I am a teacher.
    # I work as an engineer.
    # My occupation is doctor.
    occupation_patterns = [
        r"\bI work as (?:a|an) ([a-zA-Z][a-zA-Z -]*)[.!?]?$",
        r"\bI am (?:a|an) ([a-zA-Z][a-zA-Z -]*)[.!?]?$",
        r"\bmy (?:job|occupation|profession) is "
        r"(?:a|an)?\s*([a-zA-Z][a-zA-Z -]*)[.!?]?$",
    ]

    for pattern in occupation_patterns:
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            occupation = match.group(1).strip()
            context["occupation"] = occupation
            save_memory(context)
            return "occupation", occupation

    return None


def recall_memory(user_input):
    """
    判断用户是否正在询问以前提到的信息。

    如果用户正在询问记忆内容，返回对应回答；
    否则返回 None。
    """

    # 询问姓名
    name_questions = [
        r"\bwhat is my name\b",
        r"\bwhat's my name\b",
        r"\bdo you remember my name\b",
        r"\bwho am I\b",
    ]

    if any(
        re.search(pattern, user_input, re.IGNORECASE)
        for pattern in name_questions
    ):
        if context["name"]:
            return (
                f"You told me that your name is "
                f"{context['name']}."
            )
        return "You haven't told me your name yet."

    # 询问年龄
    age_questions = [
        r"\bhow old am I\b",
        r"\bwhat is my age\b",
        r"\bwhat's my age\b",
        r"\bdo you remember my age\b",
    ]

    if any(
        re.search(pattern, user_input, re.IGNORECASE)
        for pattern in age_questions
    ):
        if context["age"]:
            return (
                f"You told me that you are "
                f"{context['age']} years old."
            )
        return "You haven't told me your age yet."

    # 询问职业
    occupation_questions = [
        r"\bwhat do I do\b",
        r"\bwhat is my job\b",
        r"\bwhat's my job\b",
        r"\bwhat is my occupation\b",
        r"\bwhat is my profession\b",
        r"\bdo you remember my job\b",
    ]

    if any(
        re.search(pattern, user_input, re.IGNORECASE)
        for pattern in occupation_questions
    ):
        if context["occupation"]:
            return (
                f"You told me that you work as "
                f"a {context['occupation']}."
            )
        return "You haven't told me your occupation yet."

    # 询问系统记住了什么
    memory_questions = [
        r"\bwhat do you remember about me\b",
        r"\bwhat do you know about me\b",
        r"\bshow my information\b",
    ]

    if any(
        re.search(pattern, user_input, re.IGNORECASE)
        for pattern in memory_questions
    ):
        known_information = []

        if context["name"]:
            known_information.append(
                f"your name is {context['name']}"
            )

        if context["age"]:
            known_information.append(
                f"you are {context['age']} years old"
            )

        if context["occupation"]:
            known_information.append(
                f"you work as a {context['occupation']}"
            )

        if not known_information:
            return "I don't know much about you yet."

        return "I remember that " + ", and ".join(known_information) + "."

    return None
def respond(user_input):
    """根据记忆和规则库生成回答。"""

    # 清除记忆命令
    if re.fullmatch(
        r"(forget everything|clear memory|forget me)[.!?]?",
        user_input.strip(),
        re.IGNORECASE
    ):
        return "I have forgotten the information I stored about you."

    # 优先判断用户是否在询问过去的信息
    recalled_response = recall_memory(user_input)
    if recalled_response:
        return recalled_response

    # 提取本轮对话中的新信息
    remembered_information = update_memory(user_input)

    if remembered_information:
        field, value = remembered_information

        if field == "name":
            return (
                f"Nice to meet you, {value}. "
                "I will remember your name."
            )

        if field == "age":
            return (
                f"I see. You are {value} years old. "
                "I will remember that."
            )

        if field == "occupation":
            return (
                f"I see. You work as a {value}. "
                "How do you feel about your work?"
            )

    # 使用 ELIZA 规则库生成普通回答
    for pattern, responses in rules.items():
        match = re.search(pattern, user_input, re.IGNORECASE)

        if match:
            captured_group = (
                match.group(1).strip()
                if match.groups()
                else ""
            )

            swapped_group = swap_pronouns(captured_group)
            response_template = random.choice(responses)

            return response_template.format(swapped_group)

    # 理论上不会运行到这里，因为规则库包含 r".*"
    return "Please tell me more."


def main():
    print("Therapist: Hello! How can I help you today?")
    print(
        "Therapist: You can type 'clear memory' "
        "if you want me to forget your information."
    )

    if context["name"]:
        print(f"Therapist: Welcome back, {context['name']}.")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nTherapist: Goodbye. It was nice talking to you.")
            break

        if not user_input:
            print("Therapist: Please say something.")
            continue

        if user_input.lower() in {"quit", "exit", "bye"}:
            print("Therapist: Goodbye. It was nice talking to you.")
            break

        response = respond(user_input)
        print(f"Therapist: {response}")


if __name__ == "__main__":
    main()
