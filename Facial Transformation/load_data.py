import os

def list_files_in_directory(directory_path):
    try:
        # 使用 os.listdir() 列出資料夾內的所有檔案與目錄
        files = os.listdir(directory_path)
        
        # 過濾出檔案（排除子目錄）
        file_names = [f for f in files if os.path.isfile(os.path.join(directory_path, f))]
        
        # 回傳檔案名稱清單
        return file_names
    
    except FileNotFoundError:
        return "指定的路徑不存在，請檢查路徑是否正確。"
    except Exception as e:
        return f"發生錯誤: {str(e)}"

# 使用範例，這裡使用相對路徑
directory_path = os.path.join(".","dataset", "FFHQ dataset","thumbnails128x128")  # 替換為相對路徑
file_list = list_files_in_directory(directory_path)

if isinstance(file_list, list):
    cnt=0
    print("檔案名稱列表：")
    for file_name in file_list:
        print(file_name)
        cnt+=1
        if cnt==1000:
            break
else:
    print(file_list)  # 錯誤訊息
