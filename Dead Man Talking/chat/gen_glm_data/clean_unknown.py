import re

def remove_unknown_speaker(input_srt):
    # 正則表達式匹配 'Speaker Unknown' 區塊
    pattern = re.compile(r'\d+\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\nSpeaker Unknown:.*?(?=\n\d+|\Z)', re.DOTALL)
    
    # 移除匹配到的部分
    cleaned_srt = re.sub(pattern, '', input_srt)
    
    # 移除多餘的空行
    cleaned_srt = re.sub(r'\n{2,}', '\n', cleaned_srt).strip()
    
    return cleaned_srt

# 讀取 SRT 檔案
def process_srt_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cleaned_content = remove_unknown_speaker(content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f'清理後的字幕已儲存至 {output_file}')

# 讀取 text.txt 並處理
input_file = 'output.txt'
output_file = 'output.txt'
process_srt_file(input_file, output_file)