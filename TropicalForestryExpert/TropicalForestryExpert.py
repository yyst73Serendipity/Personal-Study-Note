import sys
from typing import List, Dict, Tuple, Set

class TropicalForestryExpert:
    # 初始化热带林业专家系统
    def __init__(self):
        self.facts: Set[str] = set()     # 使用集合存储已知事实，自动去重
        self.used_rules: Set[int] = set()  # 使用集合存储已使用的规则编号，避免重复应用
        self.knowledge_base = self._init_knowledge_base()  # 初始化知识库
        self.rules = self._init_rules()   # 初始化规则库

    # 知识库初始化：返回分类知识库字典，包含5个类别
    def _init_knowledge_base(self) -> Dict[str, List[str]]:
        return {
            "森林类型": ["热带雨林", "季雨林", "红树林", "热带人工林"],
            "经济树种": ["橡胶树", "油棕", "柚木", "桃花心木", "咖啡树", "可可树"],
            "土壤类型": ["砖红壤", "赤红壤", "火山土", "冲积土", "沙质土"],
            "气候特征": ["高温多雨", "干湿季分明", "常年湿润", "季风气候"],
            "异常症状": [
                "叶片焦枯", "树干流胶", "果实畸形",
                "叶脉黄化", "根系腐烂", "树皮龟裂",
                "落叶异常", "生长停滞", "虫蛀孔洞",
                "真菌斑块", "枝条枯萎"
            ]
        }

    # 规则库初始化：返回规则列表，每个规则包含条件、结果和编号
    def _init_rules(self) -> List[Dict]:
        return [
            # 诊断规则 (1-15)
            {"condition": ["叶片焦枯"], "result": "可能日灼或盐害", "rule_num": 1},
            {"condition": ["树干流胶"], "result": "可能病害或机械损伤", "rule_num": 2},
            {"condition": ["果实畸形"], "result": "可能授粉不良或缺硼", "rule_num": 3},
            {"condition": ["叶脉黄化"], "result": "可能缺镁或病毒病", "rule_num": 4},
            {"condition": ["根系腐烂"], "result": "可能积水或根腐病", "rule_num": 5},
            {"condition": ["树皮龟裂"], "result": "可能干旱或冻害", "rule_num": 6},
            {"condition": ["落叶异常"], "result": "可能病虫害或营养失衡", "rule_num": 7},
            {"condition": ["生长停滞"], "result": "可能土壤板结或缺氮", "rule_num": 8},
            {"condition": ["虫蛀孔洞"], "result": "可能天牛或象甲危害", "rule_num": 9},
            {"condition": ["真菌斑块"], "result": "可能炭疽病或叶斑病", "rule_num": 10},
            {"condition": ["枝条枯萎"], "result": "可能枯萎病或蛀干害虫", "rule_num": 11},
            {"condition": ["橡胶树", "树干流胶"], "result": "可能割胶过度或溃疡病", "rule_num": 12},
            {"condition": ["油棕", "果实畸形"], "result": "可能授粉不足或缺钾", "rule_num": 13},
            {"condition": ["咖啡树", "叶脉黄化"], "result": "可能缺铁或线虫危害", "rule_num": 14},
            {"condition": ["桃花心木", "落叶异常"], "result": "可能叶螨或季节性适应", "rule_num": 15},

            # 种植规则 (16-30)
            {"condition": ["热带雨林"], "result": "适合种植桃花心木", "rule_num": 16},
            {"condition": ["季雨林"], "result": "适合种植柚木", "rule_num": 17},
            {"condition": ["红树林"], "result": "适合种植红树植物", "rule_num": 18},
            {"condition": ["砖红壤"], "result": "适合种植橡胶树", "rule_num": 19},
            {"condition": ["火山土"], "result": "适合种植咖啡树", "rule_num": 20},
            {"condition": ["高温多雨"], "result": "适合种植油棕", "rule_num": 21},
            {"condition": ["干湿季分明"], "result": "适合种植柚木", "rule_num": 22},
            {"condition": ["种植橡胶树"], "result": "需要定期割胶管理", "rule_num": 23},
            {"condition": ["种植油棕"], "result": "需要充足肥料补充", "rule_num": 24},
            {"condition": ["种植咖啡树"], "result": "需要遮荫栽培", "rule_num": 25},
            {"condition": ["桃花心木", "冲积土"], "result": "生长速度最快", "rule_num": 26},
            {"condition": ["柚木", "干湿季分明"], "result": "木材品质最佳", "rule_num": 27},
            {"condition": ["可可树", "常年湿润"], "result": "果实产量最高", "rule_num": 28},
            {"condition": ["热带人工林", "沙质土"], "result": "建议种植椰子", "rule_num": 29},
            {"condition": ["季风气候"], "result": "适合混交林模式", "rule_num": 30}
        ]

    # 欢迎界面：打印系统欢迎信息和功能简介
    def _display_welcome(self):
        print("\n" + "="*50)
        print("热带林业专家系统".center(40))
        print("="*50)
        print("本系统可提供以下帮助：")
        print("- 树木异常诊断  - 种植方案推荐")
        print("- 土壤适配分析  - 气候适应性评估")
        print("="*50)

    # 分类显示知识库：按类别打印知识库内容，方便用户参考
    def _display_knowledge_categories(self):
        print("\n【可输入信息类别】")
        for i, (category, items) in enumerate(self.knowledge_base.items(), 1):
            print(f"{i}. {category}：{' | '.join(items)}")

    # 输入获取方法：处理用户输入流程，包括验证和错误处理
    def get_input(self) -> None:
        self._display_welcome()
        self._display_knowledge_categories()

        while True:
            try:
                user_input = input("\n请输入观察到的现象（多个条件用逗号分隔）:\n> ").strip()
                if not user_input:
                    raise ValueError("输入不能为空")

                # 改进的输入处理
                input_items = [x.strip() for x in user_input.replace("，", ",").split(",")]
                valid_items, invalid_items = self._validate_input(input_items)

                if invalid_items:
                    print(f"\n⚠ 无效输入：{', '.join(invalid_items)}")
                    print("请参考上方有效输入类型")
                    continue

                self.facts = set(valid_items)
                return

            except ValueError as e:
                print(f"\n错误：{str(e)}")
            except Exception as e:
                print(f"\n系统错误：{str(e)}")
                sys.exit(1)

    # 输入有效性验证
    def _validate_input(self, items: List[str]) -> Tuple[List[str], List[str]]:
        valid = []
        invalid = []
        all_items = [
            item for sublist in self.knowledge_base.values()
            for item in sublist
        ]

        for item in items:
            normalized = self._normalize(item)
            match = next(
                (x for x in all_items if self._normalize(x) == normalized),
                None
            )
            (valid if match else invalid).append(match or item)

        return valid, invalid

    # 文本规范化：统一文本格式：去空格、转小写，便于比较
    @staticmethod
    def _normalize(text: str) -> str:
        return text.strip().lower().replace(" ", "")

    # 推理过程显示：基于规则进行正向推理
    def infer(self) -> None:
        print("\n🔍 推理过程：")
        changed = True
        any_rule_applied = False

        while changed:
            changed = False
            for rule in self.rules:
                if rule["rule_num"] in self.used_rules:
                    continue

                if all(cond in self.facts for cond in rule["condition"]):
                    self._apply_rule(rule)
                    changed = True
                    any_rule_applied = True

        if not any_rule_applied:
            print("⚠ 未找到适用规则，请尝试提供更多信息")

    # 应用单条规则并显示推理过程
    def _apply_rule(self, rule: Dict) -> None:
        self.facts.add(rule["result"])
        self.used_rules.add(rule["rule_num"])
        cond_str = " ∧ ".join(rule["condition"])
        print(f"规则{rule['rule_num']}: {cond_str} → {rule['result']}")

    # 分类显示推理结果
    def show_results(self) -> None:
        print("\n" + "=" * 50)
        print("📝 推理结果".center(40))
        print("=" * 50)

        problems = [f for f in self.facts if f.startswith("可能")]
        suggestions = [f for f in self.facts if f.startswith(("适合", "需要", "最适"))]

        if problems:
            print("\n❗ 诊断发现：")
            for p in problems:
                print(f"- {p}")

        if suggestions:
            print("\n🌱 种植建议：")
            for s in suggestions:
                print(f"- {s}")

        if not (problems or suggestions):
            print("\nℹ 当前信息：")
            for fact in self.facts:
                print(f"- {fact}")
            print("\n提示：请提供更多特征以获得更准确的诊断")

    # 主循环
    def run(self) -> None:
        while True:
            try:
                self.facts.clear()
                self.used_rules.clear()

                self.get_input()
                self.infer()
                self.show_results()

                if not self._ask_continue():
                    print("\n感谢使用热带林业专家系统！")
                    break

            except KeyboardInterrupt:
                print("\n\n检测到中断操作，系统将退出...")
                break

    # 询问是否继续咨询
    def _ask_continue(self) -> bool:
        while True:
            choice = input("\n是否继续咨询？(y/n): ").strip().lower()
            if choice in ('y', 'yes'):
                return True
            if choice in ('n', 'no'):
                return False
            print("请输入 y(yes) 或 n(no)")
