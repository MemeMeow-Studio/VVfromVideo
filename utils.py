import hashlib
import os
import sys
import requests
import pickle
import random
from typing import List, Optional, Union
import numpy as np
import cv2




def get_file_hash(file_path, algorithm='sha256'):
    """
    该函数用于计算文件的哈希值
    :param file_path: 文件的路径
    :param algorithm: 哈希算法，默认为 sha256
    :return: 文件的哈希值
    """
    # 根据指定的算法创建哈希对象
    hash_object = hashlib.new(algorithm)
    try:
        # 以二进制模式打开文件
        with open(file_path, 'rb') as file:
            # 分块读取文件内容，避免大文件占用过多内存
            for chunk in iter(lambda: file.read(4096), b""):
                # 更新哈希对象的内容
                hash_object.update(chunk)
        # 获取最终的哈希值
        return hash_object.hexdigest()
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
        return None

from PIL import Image
import base64
from io import BytesIO
def image_to_base64_jpg(image_path):
    try:
        # 打开图像文件
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            # 创建一个内存缓冲区
            buffer = BytesIO()
            # 将图像保存为JPEG格式到缓冲区
            img.save(buffer, format="JPEG")
            # 获取缓冲区中的二进制数据
            img_bytes = buffer.getvalue()
            # 将二进制数据编码为Base64字符串
            base64_encoded = base64.b64encode(img_bytes).decode('utf-8')
            img.close()
        return base64_encoded
    except Exception as e:
        raise (f"处理图像时出现错误: {e}")

def verify_folder(root):
    if '.' in os.path.basename(root):
        root = os.path.dirname(root)
    if not os.path.exists(root):
        parent = os.path.dirname(root)
        if parent != root:  # 防止在根目录时无限递归
            verify_folder(parent)
        os.makedirs(root, exist_ok=True)
        print(f"dir {root} has been created")





ENDWITH_IMAGE = ['.jpg', '.jpeg', '.png', '.gif']



def get_all_file_paths(folder_path, endwith=None):
    # 用于存储所有文件的绝对路径
    file_paths = []
    # 使用os.walk()遍历文件夹及其子文件夹
    for root, directories, files in os.walk(folder_path):
        for filename in files:
            if endwith:
                if not os.path.splitext(os.path.basename(filename))[1] in endwith:
                    continue
            # 构建文件的绝对路径
            file_path = os.path.join(root, filename)
            # 将绝对路径添加到列表中
            file_paths.append(file_path)
    return file_paths