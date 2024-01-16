import os

def combine_logs(output_file):
    current_path = os.getcwd()  # 获取当前工作目录
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(current_path):
            for file in files:
                if file == 'downloads.log':
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read() + '\n')

def create_unique_filename(folder_path, filename):
    name, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename
    while os.path.exists(os.path.join(folder_path, unique_filename)):
        unique_filename = f"{name}_{counter}{ext}"
        counter += 1
    return unique_filename

def organize_files(DownloadsLog_All_txt, downloads_folder):
    current_path = os.getcwd()  # 获取当前脚本执行的目录
    downloads_path = os.path.join(current_path, downloads_folder)

    with open(os.path.join(current_path, DownloadsLog_All_txt), 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) >= 6:
                ip_address = parts[1]  # 提取IP地址
                original_file_name = parts[-3].split('/')[-1]  # 提取原始文件名
                new_file_name = parts[-2]  # 提取新文件名

                ip_folder = os.path.join(downloads_path, ip_address)
                if not os.path.exists(ip_folder):
                    os.makedirs(ip_folder)

                old_path = os.path.join(downloads_path, original_file_name)
                new_file_name = create_unique_filename(ip_folder, new_file_name)
                new_path = os.path.join(ip_folder, new_file_name)

                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                    print(f"Moved '{original_file_name}' to '{new_path}'")
                else:
                    print(f"File '{original_file_name}' not found")

# 第一步：合并downloads.log文件到DownloadsLog_All.txt
combine_logs('DownloadsLog_All.txt')

# 第二步：处理DownloadsLog_All.txt中的数据
downloads_folder = 'downloads'  # downloads文件夹名称
organize_files('DownloadsLog_All.txt', downloads_folder)
