import json
import os
import argparse
from pathlib import Path
import glob

def batch_modify_json_files(input_dir, target_string, replacement=""):
    """
    批量修改JSON文件中指定路径前缀
    
    参数:
        input_dir: 包含JSON文件的目录
        target_string: 要从路径中删除的目标前缀字符串
        replacement: 替换内容（默认为空）
    """
    # 查找所有需要修改的JSON文件
    json_files = glob.glob(os.path.join(input_dir, "transforms*.json"))
    
    if not json_files:
        print(f"在目录 {input_dir} 中未找到任何 transforms*.json 文件")
        return
    
    print(f"找到 {len(json_files)} 个JSON文件需要处理")
    
    processed_count = 0
    # 处理每个JSON文件
    for json_path in json_files:
        try:
            # 备份原始文件
            backup_path = os.path.join(os.path.dirname(json_path), f"backup_{os.path.basename(json_path)}")
            if not os.path.exists(backup_path):
                os.rename(json_path, backup_path)
            
            # 读取备份文件
            with open(backup_path, 'r') as f:
                data = json.load(f)
            
            # 检查是否需要修改
            modified = False
            if "frames" in data and isinstance(data["frames"], list):
                for frame in data["frames"]:
                    if "file_path" in frame and target_string in frame["file_path"]:
                        # 删除目标前缀
                        frame["file_path"] = frame["file_path"].replace(target_string, replacement, 1)
                        modified = True
                        print(f"修改路径: {frame['file_path']}")
            
            # 如果修改了内容，保存到新文件
            if modified:
                with open(json_path, 'w') as f:
                    json.dump(data, f, indent=4)
                print(f"成功修改文件: {json_path}")
                processed_count += 1
            else:
                print(f"文件 {json_path} 中没有找到需要修改的路径")
        
        except Exception as e:
            print(f"处理文件 {json_path} 时出错: {str(e)}")
    
    print(f"处理完成！成功修改了 {processed_count} 个JSON文件")
    print(f"原始文件已备份为 backup_transforms*.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量修改JSON文件中的文件路径前缀")
    parser.add_argument("--input_dir", type=str, required=True,
                        help="包含JSON文件的目录路径")
    parser.add_argument("--target_string", type=str, default="./data/my_object/",
                        help="要从路径中删除的目标前缀")
    
    args = parser.parse_args()
    
    # 确保路径格式正确
    input_dir = os.path.abspath(args.input_dir)
    
    # 验证输入目录是否存在
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"目录不存在: {input_dir}")
    
    batch_modify_json_files(input_dir, args.target_string)