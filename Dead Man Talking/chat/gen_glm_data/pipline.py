from gen_glm4_format import generate_glm4_format
from conv_jsonl import convert_json_to_jsonl

def main():
    # 設定檔案名稱
    input_srt_file = "input.srt"
    output_json_file = "output.json"
    output_jsonl_file = "output.jsonl"

    print("Step 1: 轉換 SRT -> JSON")
    generate_glm4_format(input_srt_file, output_json_file)

    print("Step 2: 轉換 JSON -> JSONL")
    convert_json_to_jsonl(output_json_file, output_jsonl_file)

    print("Pipeline 完成！請手動執行 split_data.py 來進行資料集切割。")

if __name__ == "__main__":
    main()
