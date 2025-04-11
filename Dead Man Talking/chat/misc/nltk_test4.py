from sentence_transformers import SentenceTransformer, util
import requests

# 增加超時時間
requests.adapters.DEFAULT_RETRIES = 5  # 增加重試次數

# 載入模型
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2", cache_folder="./model_cache", trust_remote_code=True)

# 讀取檔案內容
filename = 'jim-7'
input_file = f"{filename}.txt"
output_file = f"{filename}_output.txt"

with open(input_file, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

# 將文本轉換為 dialogue_segments 格式 (假設 alternating user/assistant)
dialogue_segments = []
speaker = "user"

for line in lines:
    dialogue_segments.append((speaker, line))
    speaker = "assistant" if speaker == "user" else "user"

# 測試不同閥值
thresholds = [round(i * 0.1, 1) for i in range(1, 10)]
results = {}

for threshold in thresholds:
    segments = []
    current_segment = []
    current_embedding = None

    for speaker, text in dialogue_segments:
        sentence_embedding = model.encode(text, convert_to_tensor=True)

        if current_embedding is not None:
            similarity = util.pytorch_cos_sim(current_embedding, sentence_embedding).item()
            if similarity < threshold:
                segments.append(current_segment)
                current_segment = []

        current_segment.append((speaker, text))
        current_embedding = sentence_embedding

    if current_segment:
        segments.append(current_segment)

    # **後處理：確保 `user` 不會單獨出現在段落結尾**
    processed_segments = []
    i = 0
    while i < len(segments):
        if len(segments[i]) % 2 == 1 and segments[i][-1][0] == "user":
            if i + 1 < len(segments):
                next_segment = segments[i + 1]
                next_segment.insert(0, segments[i].pop())
                if segments[i]:
                    processed_segments.append(segments[i])
            else:
                processed_segments.append(segments[i])
        else:
            processed_segments.append(segments[i])
        i += 1

    results[threshold] = processed_segments
    print(f'Threshold = {threshold}, segments after post-processing: {len(processed_segments)}')

# 只寫入閥值為 0.3 的結果
final_segments = results[0.3]
with open(output_file, "w", encoding="utf-8") as f:
    for segment in final_segments:
        formatted_segment = "\n".join([
            f"{speaker}: {sentence.replace('user: ', '').replace('assistant: ', '')}"
            for speaker, sentence in segment
        ])
        f.write(formatted_segment + "\n\n")

print(f"結果已寫入 {output_file}")
