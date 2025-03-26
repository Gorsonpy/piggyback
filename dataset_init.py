import os
import shutil
from tqdm import tqdm

# 设置路径
cub_root = '/root/gorsonpy/TransferGenie/dataset/CUB_200_2011'  # 修改为您的CUB数据集根目录
target_root = '/root/gorsonpy/dataset/CUB-200-2011-ImageFolder'  # 修改为目标目录
train_dir = os.path.join(target_root, 'train')
test_dir = os.path.join(target_root, 'test')

# 创建目标目录
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

print("读取数据集信息...")

# 读取类别信息
classes = {}
with open(os.path.join(cub_root, 'classes.txt'), 'r') as f:
    for line in f:
        class_id, class_name = line.strip().split()
        # 将类名中的空格替换为下划线，避免路径问题
        classes[class_id] = class_name.replace(' ', '_')

    # 读取图像路径
image_paths = {}
with open(os.path.join(cub_root, 'images.txt'), 'r') as f:
    for line in f:
        image_id, image_path = line.strip().split()
        image_paths[image_id] = image_path

# 读取图像标签
image_labels = {}
with open(os.path.join(cub_root, 'image_class_labels.txt'), 'r') as f:
    for line in f:
        image_id, class_id = line.strip().split()
        image_labels[image_id] = class_id

# 读取训练/测试分割
train_test = {}
with open(os.path.join(cub_root, 'train_test_split.txt'), 'r') as f:
    for line in f:
        image_id, is_train = line.strip().split()
        train_test[image_id] = is_train

# 创建每个类别的目录
print("创建类别目录...")
for class_name in classes.values():
    os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
    os.makedirs(os.path.join(test_dir, class_name), exist_ok=True)

# 复制图像到目标目录
print("开始复制图像...")
for image_id, image_path in tqdm(image_paths.items()):
    class_id = image_labels[image_id]
    class_name = classes[class_id]
    is_train = train_test[image_id] == '1'

    src_path = os.path.join(cub_root, 'images', image_path)

    if is_train:
        dst_path = os.path.join(train_dir, class_name, os.path.basename(image_path))
    else:
        dst_path = os.path.join(test_dir, class_name, os.path.basename(image_path))

    # 复制图像
    shutil.copy(src_path, dst_path)

print("处理完成！")

# 统计信息
train_class_counts = {cls: 0 for cls in classes.values()}
test_class_counts = {cls: 0 for cls in classes.values()}

for image_id in image_paths:
    class_id = image_labels[image_id]
    class_name = classes[class_id]
    is_train = train_test[image_id] == '1'

    if is_train:
        train_class_counts[class_name] += 1
    else:
        test_class_counts[class_name] += 1

total_train = sum(train_class_counts.values())
total_test = sum(test_class_counts.values())

print(f"训练集图像总数: {total_train}")
print(f"测试集图像总数: {total_test}")
print(f"总类别数: {len(classes)}")