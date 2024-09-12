import json
import time
from datasets import load_dataset

# 加载数据集
ds = load_dataset("AdaptLLM/finance-tasks", "Headline")

qa_pairs = []

# 记录开始时间
start_time = time.time()


for row in ds["test"]:

    input_text = row["input"]

    entries = input_text.split("Headline:")[1:]

    # 处理每一个 headline 的问答对
    for i, entry in enumerate(entries):
        try:
            if "Now answer this question:" in entry:
                headline_part, qa_part = entry.split("Now answer this question:")
            elif "Question:" in entry:
                headline_part, qa_part = entry.split("Question:")
            else:
                continue

            # 提取问题和答案
            qa_pair = qa_part.split()
            question = " ".join(qa_pair[:-1])
            answer = qa_pair[-1]

            # 创建JSON格式的数据
            qa_pairs.append({
                "id": f"{row['id']}_{i}",
                "Question": question.strip(),
                "Answer": answer.strip(),
                "Headline": headline_part.strip()  # 保留了headline以确保信息完整
            })

        except ValueError:
            # 处理分割失败的情况
            print(f"跳过无法解析的条目：{entry}")
            continue

# 保存为JSON文件
output_file = "qa_pairs.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(qa_pairs, f, ensure_ascii=False, indent=4)

# 记录结束时间
end_time = time.time()

# 计算并打印所需时间
elapsed_time = end_time - start_time
print(f"数据集清理和转换完成，共提取了 {len(qa_pairs)} 个问题-答案对。")
print(f"总用时: {elapsed_time:.2f} 秒")

