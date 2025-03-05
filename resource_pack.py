import os
import json
import shutil
import zipfile
from datetime import datetime
from typing import List, Dict, Optional

from utils import *

class ResourcePackError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        """TODO: 资源包相关错误处理"""
        print(f"ResourcePackError: {self}")
        pass

class ResourcePackService:
    def __init__(self):pass
        
    def create_resource_pack(self, 
                             pack_dir,
                           name: str,
                           version: str,
                           author: str,
                           description: str,
                           image_paths: List[str],
                           cover_image: Optional[str] = None,
                           tags: Optional[List[str]] = None,
                           regex: Optional[Dict] = None,
                             url: str=None) -> str:
        
        if not name or not version or not author:
            raise ResourcePackError("资源包名称、版本号和作者不能为空")
            
        if not image_paths:
            raise ResourcePackError("图片列表不能为空")
            
        valid_images = []
        for img_path in image_paths:
            if not os.path.exists(img_path):
                print(f"文件不存在: {img_path}")
                continue
            if not os.access(img_path, os.R_OK):
                print(f"文件无法访问: {img_path}")
                continue
            valid_images.append(img_path)
            
        if not valid_images:
            raise ResourcePackError("没有有效的图片文件可以打包")
            
        
        # 处理封面图片
        # cover_info = None
        # if cover_image and os.path.exists(cover_image):
        #     try:
        #         cover_name = os.path.basename(cover_image)
        #         name_without_ext, ext = os.path.splitext(cover_name)
        #         ext = ext.lower()
                
        #         file_hash = get_file_hash(cover_image)
        #         if file_hash:
        #             new_cover_name = f"cover{ext}"
        #             new_cover_path = os.path.join(pack_dir, new_cover_name)
        #             shutil.copy2(cover_image, new_cover_path)
        #             print(f"复制封面: {cover_image} -> {new_cover_path}")
        #             cover_info = {
        #                 "filename": new_cover_name,
        #                 "original_name": cover_name,
        #                 "hash": file_hash
        #             }
        #     except Exception as e:
        #         print(str(e))
        
        copied_files = []
        file_mapping = {} 
        for img_path in valid_images:
            img_path: str
            original_name = os.path.basename(img_path)
            name_without_ext, ext = os.path.splitext(original_name)
            ext = ext.lower()
            
            file_hash = get_file_hash(img_path)
            if not file_hash:
                print(f"获取文件hash失败: {img_path}")
                continue
            
            # 处理文件名重复问题
            new_name = original_name

            file_mapping[new_name] = {
                "hash": file_hash,
                "filepath": img_path.split(pack_dir)[-1]
            }


        manifest = {
            "name": name,
            "version": version,
            "author": author,
            "description": description,
            "created_at": datetime.now().strftime("%Y-%m-%d"),
            "tags": tags or [],
            "url": url,
            "update_url": os.path.join(url, pack_dir, "manifest.json").replace('\\', '/')
            # "cover": cover_info,

        }
        if regex:
            manifest['regex']=regex
        manifest['contents'] = {
                "images": {
                    "description": "图像资源目录",
                    "files": file_mapping,

                }
            }
        manifest_path = os.path.join(pack_dir, "manifest.json")
        try:
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=4)
            print(f"Created manifest.json: {manifest_path}")
        except Exception as e:
            raise ResourcePackError(f"创建manifest.json失败: {str(e)}")
            
        return pack_dir
    
       
       
with open(r"D:\ProgramData\vvimages\vvrepo\VVfromVideo\metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)
    metadata: dict
for resource in metadata['resources']:
    img_ps = get_all_file_paths(resource['relative_path'], endwith=ENDWITH_IMAGE)
    resource: dict
    ResourcePackService().create_resource_pack(pack_dir=resource['relative_path'],
                                               name=resource.get('name', metadata.get('name', "none")),
                                               version=metadata['version'],
                                               author=resource.get('author', metadata.get('author', "none")),
                                               description=resource.get("description", "none"),
                                               regex = resource.get("regex", None),
                                               image_paths = img_ps,
                                               url = metadata.get('resource_url'))