import os
import re
import threading
import time
import argparse
from queue import Queue

def search_in_file(file_path, keyword, result_queue, case_sensitive=False):
    """在单个文件中搜索关键词"""
    try:
        encoding = 'utf-8'
        pattern = re.compile(re.escape(keyword), 0 if case_sensitive else re.IGNORECASE)
        matches = []
        
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                if pattern.search(line):
                    matches.append(f"  Line {line_num}: {line.strip()}")
        
        if matches:
            result = f"Found in {file_path}:\n" + "\n".join(matches)
            result_queue.put(result)
    
    except Exception as e:
        result_queue.put(f"Error reading {file_path}: {str(e)}")

def worker(file_queue, keyword, result_queue, case_sensitive):
    """工作线程函数"""
    while not file_queue.empty():
        file_path = file_queue.get()
        search_in_file(file_path, keyword, result_queue, case_sensitive)
        file_queue.task_done()

def main():
    parser = argparse.ArgumentParser(description='文件关键词快速搜索工具')
    parser.add_argument('keyword', type=str, help='要搜索的关键词')
    parser.add_argument('-d', '--directory', default='.', help='搜索目录 (默认: 当前目录)')
    parser.add_argument('-e', '--extensions', nargs='*', default=['txt', 'py', 'java', 'c', 'cpp', 'md', 'html', 'js', 'css'],
                        help='文件扩展名过滤 (默认: txt py java c cpp md html js css)')
    parser.add_argument('-t', '--threads', type=int, default=8, help='线程数 (默认: 8)')
    parser.add_argument('-c', '--case', action='store_true', help='区分大小写')
    args = parser.parse_args()

    start_time = time.time()
    file_queue = Queue()
    result_queue = Queue()

    # 收集匹配的文件
    for root, _, files in os.walk(args.directory):
        for file in files:
            if any(file.endswith(f'.{ext}') for ext in args.extensions):
                file_path = os.path.join(root, file)
                file_queue.put(file_path)

    # 创建工作线程
    threads = []
    for _ in range(min(args.threads, file_queue.qsize())):
        t = threading.Thread(target=worker, args=(file_queue, args.keyword, result_queue, args.case))
        t.start()
        threads.append(t)

    # 等待所有文件处理完成
    file_queue.join()
    
    # 打印结果
    print(f"\n搜索完成! 关键词: '{args.keyword}', 目录: '{args.directory}', 文件类型: {args.extensions}")
    print("=" * 60)
    
    if result_queue.empty():
        print("未找到匹配结果")
    else:
        while not result_queue.empty():
            print(result_queue.get())
            print("-" * 60)
    
    print(f"\n总计扫描文件: {file_queue.qsize()}, 耗时: {time.time() - start_time:.2f}秒")

if __name__ == "__main__":
    main()