from EightPuzzle import EightPuzzle


def input_status(prompt):
    print(prompt)
    status = []
    
    # 循环获取3行输入
    for i in range(3):
        while True:
            row_str = input(f"请输入第 {i + 1} 行(用空格分隔): ")
            try:
                row = list(map(int, row_str.split()))
                if len(row) != 3:
                    print("错误: 每行必须包含3个数字!")
                    continue
                status.append(row)
                break
            except ValueError:
                print("错误: 请输入有效(0-8且不重复)的数字!")
    return status


def main():
    print("八数码问题求解器 - A*算法实现\n")
    print("*****************************************")

    # 获取初始状态
    initial_status = input_status("\n请输入初始状态(0代表空格):")

    # 固定目标状态
    target_status = [
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ]

    try:
        puzzle = EightPuzzle(initial_status, target_status)
        print("\n目标状态:")
        puzzle.display(target_status)

        if initial_status == target_status:
            print("\n当前已是目标状态！")
            print("无需移动。")
            return

        print("\n*****************************************")
        print("\n开始搜索解决方案...")
        solvable = puzzle.a_star()

        if solvable:
            print(f"\n找到解决方案，共需要 {len(puzzle.solution_path) - 1} 步。")
            print(f"扩展节点数: {puzzle.nodes_expanded}")
            print(f"Open集最大大小: {puzzle.max_open_size}")

            while True:
                print("\n请选择演示方式:")
                print("1. 逐步演示解决方案(需按Enter键继续)")
                print("2. 自动连续播放解决方案")
                choice = input("请输入选项(1/2): ")

                print("\n*****************************************")

                if choice == '1':
                    puzzle.display_stepwise()
                    break
                elif choice == '2':
                    puzzle.display_animate()
                    break
                else:
                    print("无效输入，请重新选择。")
        else:
            print("\n无法从初始状态到达目标状态！")

    except ValueError as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()