# 1本章介绍了三种经典的智能体范式:ReAct、Plan-and-Solve 和 Reflection。请分析:
# 1.1这三种范式在"思考"与"行动"的组织方式上有什么本质区别？
ReAct：思考一步、行动一步、观察结果，再继续思考，边做边规划
Plan_and_solve：先形成完整计划，再按照计划依次执行，先规划再行动
Reflection：先执行，再评价执行结果，根据反馈重新改进 尝试到反思再根据反思结果重新行动
# 1.2如果要设计一个"智能家居控制助手"（需要控制灯光、空调、窗帘等多个设备，并根据用户习惯自动调节），你会选择哪种范式作为基础架构？为什么？
选择ReAct，因为家具控制助手需要控制多个设备，通过react先进行思考，做出行动之后，观察用户行为，如果用户对该动作并未再次调整说明用户满意，无需再调整，此外需要根据每天的时间，房间的温度湿度，光线的强度选择是否调节，或者怎么调节具体的哪些家具
# 1.3是否可以将这三种范式进行组合使用？若可以，请尝试设计一个混合范式的智能体架构，并说明其适用场景。
# 混合起来本质是多智能体框架
Plan-and-Solve 决定整体应该怎么做 ReAct 决定当前一步接下来怎么做 Reflection 判断已经做得是否足够好 
使用场景：
深度研究与信息检索
例如行业研究、文献综述和竞品分析。任务需要先规划研究方向，再动态搜索资料，最后检查证据是否充分。
复杂代码开发
计划器负责拆分需求，ReAct负责读取代码、运行测试和修改程序，Reflection负责代码审查、错误检查与性能优化。
数据分析
智能体需要先规划分析流程，再调用数据库、Python或可视化工具，最后检查计算结果和结论是否一致。
长文写作
Plan-and-Solve负责设计文章结构，ReAct负责查找材料和撰写章节，Reflection负责检查论证、事实、重复内容和语言质量。
决策支持
例如医疗辅助、金融分析和商业决策。这些任务步骤复杂且对准确性要求较高，需要多轮验证。不过在高风险场景中，反思不能替代专业人员审查。

# 2. ToolExecutor 扩展实践

## 2.1 计算器工具

原来的 `ToolExecutor` 只保存工具名称、描述和函数，已经足够支持简单工具，但还缺少参数校验、异常隔离和调用结果的统一格式。下面的实现使用 Python 的 `ast` 解析表达式，只允许数字和四则运算，避免直接使用 `eval` 带来的代码执行风险。

```python
import ast
import operator as op
from typing import Any, Callable


class Calculator:
    _operators = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.USub: op.neg,
        ast.UAdd: op.pos,
    }

    @classmethod
    def _evaluate(cls, node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return cls._evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.UnaryOp) and type(node.op) in (ast.USub, ast.UAdd):
            return cls._operators[type(node.op)](cls._evaluate(node.operand))
        if isinstance(node, ast.BinOp) and type(node.op) in cls._operators:
            left = cls._evaluate(node.left)
            right = cls._evaluate(node.right)
            if isinstance(node.op, ast.Div) and right == 0:
                raise ValueError("除数不能为 0")
            return cls._operators[type(node.op)](left, right)
        raise ValueError("表达式包含不支持的语法")

    @classmethod
    def calculate(cls, expression: str) -> str:
        expression = expression.replace("×", "*").replace("÷", "/").strip()
        if len(expression) > 200:
            raise ValueError("表达式过长")
        tree = ast.parse(expression, mode="eval")
        result = cls._evaluate(tree)
        return f"{result:g}"


executor = ToolExecutor()
executor.registerTool(
    "calculator",
    "计算安全的四则运算和幂运算。输入为 expression，例如 (123 + 456) * 789 / 12",
    Calculator.calculate,
)
```

对于题目中的表达式，调用 `calculator[(123 + 456) × 789 / 12]`，结果为 `38038.5`。提示词中应明确工具输入格式，例如：

```text
calculator[{"expression": "(123 + 456) * 789 / 12"}]
```

更推荐让模型输出 JSON 参数，而不是依赖位置参数，这样可以扩展单位、精度等字段。

## 2.2 工具选择失败和参数错误处理

不能在工具不存在或参数错误时直接终止，也不能把异常堆栈暴露给用户。执行器应返回结构化结果，并把可恢复的错误反馈给模型，让模型在有限次数内纠正。

```python
from dataclasses import dataclass
import json


@dataclass
class ToolResult:
    ok: bool
    message: str
    retryable: bool = False


class SafeToolExecutor(ToolExecutor):
    def execute(self, name: str, raw_input: str) -> ToolResult:
        tool = self.tools.get(name)
        if tool is None:
            names = ", ".join(self.tools)
            return ToolResult(False, f"工具不存在。可用工具：{names}", True)

        try:
            value = json.loads(raw_input)
            if not isinstance(value, dict):
                raise ValueError("工具参数必须是 JSON 对象")
            return ToolResult(True, str(tool["func"](**value)))
        except (json.JSONDecodeError, TypeError, ValueError, ZeroDivisionError) as exc:
            return ToolResult(False, f"参数错误：{exc}。请根据工具 schema 修正后重试。", True)
        except Exception:
            # 记录完整日志，但只向模型返回稳定、无敏感信息的错误。
            return ToolResult(False, "工具执行失败，请换一种参数或稍后重试。", False)
```

ReAct 循环可以维护每个工具的失败次数：

1. 第一次失败：返回工具 schema、错误原因和一个正确示例。
2. 第二次失败：要求模型重新检查工具名称、必填字段和字段类型，并禁止重复原请求。
3. 第三次失败：停止自动调用，改用候选工具或向用户询问缺失信息。
4. 对不可恢复错误（权限不足、服务不可用）不重试，转人工或返回明确的降级结果。

因此，失败反馈应该进入 `Observation`，而不是 Python 异常直接打断循环；同时要设置最大步数、单工具最大重试次数和总耗时上限，避免死循环。

## 2.3 工具数量达到 50—100 个时的工程优化

把全部工具描述塞进每一次提示词会造成上下文变长、费用升高、模型混淆和工具误选。可采用以下机制：

- 工具按领域、权限和风险分组，例如订单、支付、物流、搜索、计算；
- 先用轻量意图分类器或向量检索召回 Top-K 工具，再把详细 schema 注入主模型；
- 使用统一的 JSON Schema 描述参数，并在调用前做本地校验；
- 为工具增加 `tags`、前置条件、成本、延迟、权限和风险等级；
- 对高风险工具使用显式确认和人工审批；
- 记录工具调用成功率、参数错误率和平均延迟，按指标淘汰或改写描述；
- 对相似工具提供路由器或聚合 API，例如用一个“物流查询”工具隐藏多个供应商实现；
- 缓存稳定查询结果，并为工具目录建立版本号。

推荐的两阶段流程是“工具检索/路由 → 主模型生成结构化调用”，而不是让主模型直接在 100 个工具中盲选。

# 3. Plan-and-Solve 的动态与分层规划

## 3.1 动态重规划

静态计划适合步骤稳定、依赖明确的任务，但真实环境中可能出现库存不足、接口失败、结果不满足约束等情况。动态版本应把计划表示成带状态的任务图，而不是不可变字符串列表：

```python
from dataclasses import dataclass, field
from typing import Literal


@dataclass
class Step:
    id: str
    description: str
    status: Literal["pending", "running", "done", "failed"] = "pending"
    result: str = ""
    attempts: int = 0
    dependencies: list[str] = field(default_factory=list)


def should_replan(step: Step, result: str) -> bool:
    return step.status == "failed" or "不符合约束" in result or "不可用" in result
```

执行器每完成一步都进行验证：结果是否满足验收条件、是否影响后续步骤、是否仍符合用户目标。若失败，先按策略重试或替代工具；仍失败则把当前状态、失败原因和剩余目标交给规划器，要求规划器只修改受影响的子图，保留已经验证成功的步骤。重规划还应设置次数、成本和时间预算，连续失败时暂停并向用户解释，而不是无限自我修正。

## 3.2 预订北京到上海商务旅行的范式选择

单独使用 Plan-and-Solve 不够稳健，因为航班、酒店和租车库存及价格会实时变化；单独使用 ReAct 又可能缺少跨服务的全局约束，例如时间衔接、预算和公司差旅政策。更合适的是组合：

1. Plan-and-Solve 生成整体目标、预算、时间和依赖关系；
2. ReAct 分别查询航班、酒店、租车并根据实时观察调整；
3. Reflection 在提交订单前检查日期、乘客信息、价格、取消政策和行程冲突；
4. 最终支付或下单前必须获得用户确认。

## 3.3 分层规划

第一层只生成抽象目标，例如“确认出行约束 → 生成交通方案 → 预订住宿 → 预订租车 → 汇总并确认”。第二层在执行某个高层步骤时，才生成详细子计划，例如把“生成交通方案”拆成查询航班、筛选直飞、检查行李政策、比较价格和锁定候选。

分层规划的优势是减少一次性规划的上下文压力，允许每个子领域使用专门工具和约束，也便于局部重规划、权限隔离、并行执行和人工介入。代价是需要维护父子任务状态，并处理高层目标与子计划之间的一致性。

# 4. Reflection 的模型、终止条件与论文助手

## 4.1 执行模型和反思模型分离

用更快、更便宜的模型执行，用更强的模型反思，通常可以降低总体成本并提高缺陷发现率。强模型可以承担复杂的代码审查、事实核验和安全检查；快模型负责格式化、改写和常规执行。代价是两个模型的能力边界、上下文窗口和输出格式可能不一致，反思模型还可能提出执行模型无法实现的建议。因此应使用统一的结构化反馈 schema，记录模型版本，并对关键结论加入测试或工具证据，不能只相信反思文本。

## 4.2 更智能的终止条件

“包含无需改进”过于脆弱，可能因措辞不同提前停止；固定最大次数又可能浪费预算。可综合以下条件：

- 通过自动测试、类型检查、事实核验和格式校验；
- 本轮评分超过阈值，且连续两轮提升小于 `epsilon`；
- 反思问题的严重性均低于阈值；
- 发现反馈与上一轮重复，或连续两轮没有有效修改；
- 达到 token、时间、费用和最大迭代预算；
- 触发高风险项时转人工，而不是继续循环。

## 4.3 学术论文助手的多维 Reflection

初稿生成后，为每一轮建立独立的反馈维度：

| 维度 | 检查内容 | 可验证信号 |
|---|---|---|
| 段落逻辑 | 主题句、论据、过渡和结论是否连贯 | 段落论证图、缺失前提 |
| 方法创新性 | 与已有工作差异是否清楚，是否夸大 | 文献检索和 claim-evidence 表 |
| 科学严谨性 | 结论是否超出实验支持，统计方法是否合理 | 统计检查、反例检查 |
| 语言表达 | 清晰、准确、术语一致，避免空泛表达 | 术语表、可读性指标 |
| 引用规范 | 每个外部事实有可追溯来源，引用格式一致 | DOI/标题核验、引用覆盖率 |

每个评审器只输出 `issue、severity、evidence、suggestion`，编辑器按严重性排序后修改，并重新运行检查。高风险事实、数据和引用必须要求作者确认；最终停止条件应同时满足逻辑、证据、语言和引用四类阈值。

# 5. 提示词工程实践

## 5.1 ReAct 与 Plan-and-Solve 提示词的结构差异

ReAct 提示词强调 `Thought → Action → Observation` 的循环，工具描述、调用语法和历史记录是核心，因为模型每次只决定下一步。Plan-and-Solve 提示词则要求一次性输出有序计划，再把当前步骤、已完成结果和剩余任务交给执行器，核心是全局顺序和步骤边界。前者擅长环境不确定、需要根据观察调整的任务；后者擅长依赖稳定、可以提前拆解的任务。

## 5.2 角色设定的影响

“极其严格的代码评审专家”会更关注算法复杂度、边界条件和缺陷，可能给出较多批评；“注重代码可读性的开源项目维护者”会更关注命名、模块边界、文档、测试和社区协作，反馈通常更温和、更偏向可维护性。角色设定会改变评价维度、语气和修改优先级，但不能替代明确的检查清单、输入输出格式和客观验收标准。

## 5.3 Few-shot 示例

可在 ReAct 提示词中加入一个完整、无歧义的示例，并明确示例仅用于学习格式：

```text
示例问题：计算 12 * 8
示例输出：
Thought: 这是一个数学计算问题，应使用 calculator。
Action: calculator[{"expression": "12 * 8"}]

观察结果：96
示例输出：
Thought: 已获得计算结果。
Action: Finish[96]
```

与只给抽象规则相比，few-shot 能显著提高 `Action` 的格式遵循率，尤其能减少工具名拼写错误和参数字段遗漏。缺点是占用上下文，示例过多可能限制模型处理真实问题；示例还必须覆盖错误和 Finish 情况，并定期验证不会诱导模型照抄示例内容。

# 6. 电商客服智能体方案

## 6.1 核心架构

我会选择“Plan-and-Solve + ReAct + Reflection”的组合，并将业务规则和权限控制放在模型之外：

1. Plan-and-Solve 根据退款理由、订单和政策生成处理计划；
2. ReAct 调用订单、物流和政策工具，处理实时信息和缺失字段；
3. Reflection 对退款资格、证据完整性、政策例外、语气和置信度进行复核；
4. 规则引擎决定自动批准、拒绝、补充材料或转人工，模型只负责理解、解释和生成草稿；
5. 发送邮件、退款和修改订单等副作用操作必须经过权限校验，必要时要求人工或用户确认。

## 6.2 工具设计

至少需要以下工具：

- `get_order(order_id, user_id)`：查询订单商品、金额、下单时间、支付状态和收货信息，并校验用户权限；
- `get_logistics(order_id)`：查询物流节点、签收状态、预计送达时间和异常记录；
- `get_refund_policy(category, reason, order_status)`：返回适用政策条款、时间窗口、例外条件和所需证据；
- `calculate_refund(order_id, policy_result)`：按规则计算可退金额、运费和优惠券处理方式；
- `send_email(to, subject, body, idempotency_key)`：发送最终确认邮件，支持幂等和审计；
- `create_human_review_case(order_id, reason, evidence)`：争议或低置信度时创建人工工单。

工具返回统一的结构化结果，并包含来源、时间戳、权限状态和错误类型；发送邮件和退款工具不能仅凭自然语言直接调用。

## 6.3 提示词与决策约束

系统提示词应明确：优先遵守公司政策和用户权限；不得编造订单、物流或政策信息；证据不足时必须询问或转人工；不能为了“取悦用户”突破退款规则；回复应解释结论、金额、下一步和申诉渠道。可以要求模型输出：

```json
{
  "decision": "approve|reject|need_more_info|human_review",
  "confidence": 0.0,
  "policy_evidence": [],
  "missing_information": [],
  "customer_reply": ""
}
```

置信度低于阈值，或涉及高金额、欺诈嫌疑、政策例外和用户投诉时，强制执行 Reflection，并优先输出 `human_review`。客服语言应承认用户诉求、清楚说明依据、避免指责，并提供可操作的后续步骤。

## 6.4 上线风险与技术措施

- **错误批准或拒绝**：使用规则引擎、政策版本管理、离线回放评测和人工抽检；
- **隐私泄露**：最小权限、字段脱敏、租户隔离、加密、审计日志和数据保留期限；
- **提示词注入**：订单和政策数据与用户文本分离，工具白名单、参数 schema 校验和输出过滤；
- **重复退款或重复发信**：幂等键、事务状态机、金额上限和人工审批；
- **幻觉和过度承诺**：只允许基于工具证据生成事实，回复前进行事实一致性检查；
- **服务不可用或超时**：重试退避、熔断、缓存只读查询和人工兜底；
- **政策变化导致过期决策**：政策知识库版本化，生效日期校验，规则变更后自动回归测试；
- **偏见和体验下降**：按用户群体监测批准率、转人工率、投诉率和等待时间，定期进行公平性与对抗性评测。

上线后应保留完整的决策证据链：原始请求、使用的政策版本、工具响应、模型版本、最终决策和人工修改记录。这样既便于申诉和审计，也便于定位模型、工具或政策配置的问题。