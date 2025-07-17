import heapq
import time
import copy

# 八数码问题求解类
class EightPuzzle:
    # 初始化方法
    def __init__(self, initial_status, target_status):
        self.initial_status = initial_status  # 初始状态
        self.target_status = target_status    # 目标状态
        self.size = 3                         # 棋盘大小(3x3)
        self.solution_path = []               # 存储解决方案路径及评估值
        self.step_count = 0                   # 步数计数器
        self.nodes_expanded = 0               # 扩展节点数
        self.max_open_size = 0                # open集最大大小
        self.search_log = []                  # 搜索过程日志

        # 验证输入合法性
        if not self.is_valid(initial_status) or not self.is_valid(target_status):
            raise ValueError("输入不合法！请输入0-8的且不重复的数字！")

    # 判断输入合法性方法：必须包含0-8的数字且不重复
    def is_valid(self, status):
        if len(status) != 3 or any(len(row) != 3 for row in status):
            return False

        numbers = []
        for row in status:
            numbers.extend(row)

        return sorted(numbers) == list(range(9))

    # 找到空白格 0 的位置
    def find_zero(self, status):
        for i in range(self.size):
            for j in range(self.size):
                if status[i][j] == 0:
                    return (i, j)
        return None

    # 生成所有可能的移动状态
    def get_possible_moves(self, status):
        blank_row, blank_col = self.find_zero(status)
        possible_moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_row, new_col = blank_row + dr, blank_col + dc
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                new_status = copy.deepcopy(status)
                new_status[blank_row][blank_col], new_status[new_row][new_col] = new_status[new_row][new_col], new_status[blank_row][blank_col]
                possible_moves.append(new_status)

        return possible_moves

    # 启发式函数 - 计算错位数 w(n)
    def heuristic(self, status):
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if status[i][j] != 0 and status[i][j] != self.target_status[i][j]:
                    count += 1
        return count

    # A*算法 - 求解八数码问题
    def a_star(self):
        open_set = []        # 优先队列(open集)
        closed_set = set()   # 已访问状态集(closed集)

        h = self.heuristic(self.initial_status)
        initial_f = 0 + h

        # 存储元组: (f(n), step_count, status, path, g(n), h(n), parent_status)
        heapq.heappush(open_set, (initial_f, self.step_count, self.initial_status, [], 0, h, None))

        while open_set:
            self.max_open_size = max(self.max_open_size, len(open_set))
            current_f, _, current_status, path, g, h, parent_status = heapq.heappop(open_set)
            self.nodes_expanded += 1
            status_tuple = tuple(tuple(row) for row in current_status)
            if status_tuple in closed_set:
                continue
            closed_set.add(status_tuple)
            if current_status == self.target_status:
                self.reconstruct(current_status, path, g, h, parent_status)
                return True

            # 生成所有可能的移动
            for move in self.get_possible_moves(current_status):
                move_tuple = tuple(tuple(row) for row in move)
                if move_tuple not in closed_set:
                    new_g = g + 1
                    new_h = self.heuristic(move)
                    new_f = new_g + new_h
                    self.step_count += 1
                    heapq.heappush(open_set, (new_f, self.step_count, move, path + [current_status], new_g, new_h, current_status))

        return False

    # 重构解决方案路径，确保评估值正确
    def reconstruct(self, final_status, path, final_g, final_h, parent_status):
        self.solution_path = []

        self.solution_path.append((final_status, final_g, final_h, final_g + final_h))

        current_status = parent_status
        remaining_path = path.copy()

        while current_status is not None and remaining_path:
            status = remaining_path.pop()
            g = final_g - len(self.solution_path)
            h = self.heuristic(status)
            f = g + h
            self.solution_path.insert(0, (status, g, h, f))
            current_status = self.find_parent_status(current_status, remaining_path)

        initial_h = self.heuristic(self.initial_status)
        self.solution_path.insert(0, (self.initial_status, 0, initial_h, initial_h))

    # 帮助找到父状态
    def find_parent_status(self, current_status, path):
        if not path:
            return None
        return path[-1] if path else None

    # 显示当前状态
    def display(self, status):
        for row in status:
            print(" ".join(str(num) if num != 0 else " " for num in row))

    # 逐步演示解决方案(需按Enter键继续)
    def display_stepwise(self):
        print("\n初始状态:")
        self.display(self.initial_status)
        h = self.heuristic(self.initial_status)
        print(f"d(n)=0, w(n)={h}, f(n)={h}")
        print("------------------------------------------")
        input("按Enter键继续...")

        for i, (status, g, h, f) in enumerate(self.solution_path[1:], 1):
            print(f"\n第 {i} 步:")
            self.display(status)
            print(f"d(n)={g}, w(n)={h}, f(n)={f}")
            print("------------------------------------------")
            input("按Enter键继续...")

        print("\n已到达目标状态!")

    # 自动连续播放解决方案
    def display_animate(self):
        print("\n初始状态:")
        self.display(self.initial_status)
        h = self.heuristic(self.initial_status)
        print(f"d(n)=0, w(n)={h}, f(n)={h}")
        print("------------------------------------------")
        time.sleep(1)

        for i, (status, g, h, f) in enumerate(self.solution_path[1:], 1):
            print(f"\n第 {i} 步:")
            self.display(status)
            print(f"d(n)={g}, w(n)={h}, f(n)={f}")
            print("-------------------------------------------------------")
            time.sleep(1)

        print("\n已到达目标状态!")