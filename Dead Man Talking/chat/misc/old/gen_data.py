import re
import json

def parse_time_format(time_str):
    """
    將時間格式 00:01:49,480 轉換為秒數。
    """
    hours, minutes, seconds = map(float, time_str.replace(',', '.').split(':'))
    return hours * 3600 + minutes * 60 + seconds

def read_and_filter_by_time(file_path, start_time, end_time):
    """
    讀取檔案並篩選出在時間區間內的字幕。
    """
    filtered_data = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i in range(len(lines)):
        # 檢查是否為時間範圍行
        if re.match(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", lines[i]):
            time_range = lines[i].strip()
            start, end = time_range.split(' --> ')
            start_sec = parse_time_format(start)
            end_sec = parse_time_format(end)

            # 如果字幕在指定的時間區間內
            if start_sec >= start_time and end_sec <= end_time:
                # 合併該段字幕的所有文字
                content = []
                j = i + 1
                while j < len(lines) and lines[j].strip() and not re.match(r"^\d+$", lines[j]):
                    content.append(lines[j].strip())
                    j += 1

                # 加入過濾後的結果
                if content:
                    filtered_data.append({
                        "role": "assistant",
                        "content": " ".join(content)
                    })

    return filtered_data

# 主程式
if __name__ == "__main__":
    # 輸入檔案路徑
    input_file = "text.srt"

    # 指定時間範圍（以秒為單位）
    start_time = 8*60+4  
    end_time = 10*60+45

    # 讀取並過濾資料
    result = read_and_filter_by_time(input_file, start_time, end_time)
    # 調整格式為嵌套的 messages 結構
    result = [{"messages": result}]
    # 儲存為 JSON
    output_file = "filtered_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"資料已成功過濾並儲存為 {output_file}")
