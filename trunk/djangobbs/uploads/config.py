#!/usr/bin/env python
#coding=utf-8

"""文件上传的默认配置"""


from djangobbs.install.models import ConfigTree

UPLOAD_FILE_FOLDER = ConfigTree.get_config('djangobbs/uploads/file.folder', r'uploads/%Y/%m/%d') # 用户应该根据自己的实际情况，将此修改为存放上传文件的目录。
MAX_THUMBNAIL_SIZE = ConfigTree.get_config('djangobbs/uploads/max.thumbnail.size', 250) # 用户应该根据自己的实际情况，将此修改为存放上传文件的目录。

def save_config():  
    """Call this function to save the config of this app"""
    ConfigTree.put_config('djangobbs/uploads/file.folder', UPLOAD_FILE_FOLDER)
    ConfigTree.put_config('djangobbs/uploads/max.thumbnail.size', MAX_THUMBNAIL_SIZE)
