import json
import random
import os
import argparse
from pathlib import Path

def split_dataset(input_json, output_dir, train_ratio=0.7, val_ratio=0.15):
    """
    划分数据集为train/val/test
    
    参数:
        input_json: 输入的JSON文件路径
        output_dir: 输出目录
        train_ratio: 训练集比例
        val_ratio: 验证集比例
    """
    # 确保比例总和 <= 1
    test_ratio = 1.0 - train_ratio - val_ratio
    assert test_ratio >= 0, "训练集和验证集比例总和不能超过1"
    
    # 加载原始JSON文件
    with open(input_json, 'r') as f:
        data = json.load(f)
    
    # 检查是否有必要的字段
    if "frames" not in data:
        raise ValueError("JSON文件中缺少必需的'frames'字段")
    
    # 提取所有帧并打乱顺序
    all_frames = data["frames"]
    random.shuffle(all_frames)
    
    # 计算划分点
    n_total = len(all_frames)
    n_train = int(n_total * train_ratio)
    n_val = int(n_total * val_ratio)
    n_test = n_total - n_train - n_val

    # 划分数据集
    train_frames = all_frames[:n_train]
    val_frames = all_frames[n_train:n_train+n_val]
    test_frames = all_frames[n_train+n_val:]

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 保存划分后的JSON文件
    def save_subset(subset_name, frames):
        # 复制原始数据（排除frames）
        subset_data = {k: v for k, v in data.items() if k != "frames"}
        # 添加划分后的帧
        subset_data["frames"] = frames
        
        output_path = os.path.join(output_dir, f"transforms_{subset_name}.json")
        with open(output_path, 'w') as f:
            json.dump(subset_data, f, indent=4)
        return output_path

    train_path = save_subset("train", train_frames)
    val_path = save_subset("val", val_frames)
    test_path = save_subset("test", test_frames)

    # 生成划分统计信息
    split_stats = {
        "total_frames": n_total,
        "train_frames": n_train,
        "val_frames": n_val,
        "test_frames": n_test,
        "train_ratio": train_ratio,
        "val_ratio": val_ratio,
        "test_ratio": test_ratio,
        "output_paths": {
            "train": os.path.abspath(train_path),
            "val": os.path.abspath(val_path),
            "test": os.path.abspath(test_path)
        }
    }
    
    stats_path = os.path.join(output_dir, "split_summary.json")
    with open(stats_path, 'w') as f:
        json.dump(split_stats, f, indent=4)
    
    print(f"数据集划分成功！")
    print(f"总帧数: {n_total}")
    print(f"训练集: {n_train} 帧 ({n_train/n_total:.1%})")
    print(f"验证集: {n_val} 帧 ({n_val/n_total:.1%})")
    print(f"测试集: {n_test} 帧 ({n_test/n_total:.1%})")
    print(f"划分摘要已保存至: {stats_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="划分JSON数据集为train/val/test")
    parser.add_argument("--input_json", type=str, required=True, 
                        help="输入的JSON文件路径")
    parser.add_argument("--output_dir", type=str, required=True,
                        help="输出目录，划分后的文件将保存在此")
    parser.add_argument("--train_ratio", type=float, default=0.7,
                        help="训练集比例（0-1之间）")
    parser.add_argument("--val_ratio", type=float, default=0.15,
                        help="验证集比例（0-1之间）")
    
    args = parser.parse_args()
    
    # 验证比例
    if not (0 <= args.train_ratio <= 1 and 0 <= args.val_ratio <= 1):
        raise ValueError("比例必须在0和1之间")
    
    # 确保输入文件存在
    if not os.path.exists(args.input_json):
        raise FileNotFoundError(f"输入文件不存在: {args.input_json}")
    
    # 确保路径格式正确
    input_json = os.path.abspath(args.input_json)
    output_dir = os.path.abspath(args.output_dir)
    
    split_dataset(input_json, output_dir, args.train_ratio, args.val_ratio)