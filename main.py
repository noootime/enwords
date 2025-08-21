import os

def import_vocabulary(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            vocabulary = [line.strip() for line in file if line.strip()]

        if not vocabulary:
            print("警告：词库文件为空！")
            return None

        print(f"成功导入 {len(vocabulary)} 个词条。")
        return  vocabulary
    except Exception as e:
        print(f"导入词库时出错: {str(e)}")
        return None

def dictation(vocabulary):
    if not vocabulary:
        print("没有可听写的内容，请先导入有效的词库")
        return

    total = len(vocabulary)
    user_answers = []

    print("\n=========== 开始听写 ===========")
    print(f"总共 {total} 个词条，请开始听写：")
    print("提示：回车提交答案，如果不会，直接回车即可")

    for i in range(total):
        prompt = f"[{i+1}] 请输入："
        user_input = input(prompt).strip()
        user_answers.append(user_input)

    correct = 0
    incorrect = []

    for i in range(total):
        answer = vocabulary[i]
        user_answer = user_answers[i]

        if answer.lower() == user_answer.lower():
            correct += 1
        else:
            incorrect.append((answer, user_answer))

    score = int((correct / total) * 100) if total > 0 else 0

    print("\n=========== 结果 ===========")
    print(f"正确：{correct}")
    print(f"错误：{len(incorrect)}")
    print(f"得分：{score}")

    if incorrect:
        print("\n错误列表：")
        max_answer_len = max(len(item[0]) for item in incorrect)
        max_user_len = max(len(item[1]) for item in incorrect)
        line_length = max_answer_len + max_user_len + 7

        print("-" * line_length)
        print(f"{'答案':<{max_answer_len}} | {'你的答案':<{max_user_len}}")
        print("-" * line_length)

        for answer, user_answer in incorrect:
            display_user = user_answer if user_answer else "（未作答）"
            print(f"{answer:<{max_answer_len}} | {display_user:<{max_user_len}}")

        print("-" * line_length)

def main():
    print("欢迎使用ListenWrite！")

    file_path = input("\n请输入词库文件路径：").strip()

    vocabulary = import_vocabulary(file_path)
    if not vocabulary:
        print("词库导入失败，请检查文件路径是否正确。")
        return

    dictation(vocabulary)

    print("\n程序结束，感谢使用！")

if __name__ == '__main__':
    main()