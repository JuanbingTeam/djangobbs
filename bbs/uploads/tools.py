#!/usr/bin/env python
#coding=utf-8


from uploads.models import *
from uploads.config import UPLOAD_FILE_FOLDER
from uploads.config import MAX_THUMBNAIL_SIZE

from settings import MEDIA_ROOT
from md5 import md5
from cStringIO import StringIO

import os.path
import time
from datetime import datetime
import PIL
import uploads.exif
import Image, ImageDraw # 需要PIL支持

def get_ext_name(fullname):
    """获取文件的扩展名。（不包括.）"""
    i = fullname.rfind('.')
    result = ""
    if i > -1:
        result = fullname[i+1:]
    if len(result) > 10:
        result = ""
    else:
        result = result.lower()
    return result

def get_take_time(content):
    """获取照片的拍摄时间"""
    file = StringIO(content)
    tag = uploads.exif.process_file(file)
    file.close()
    try:
        originalTime = tag["EXIF DateTimeOriginal"]
        result = time.strptime(originalTime, "%Y:%m:%d %H:%M:%S")
        return datetime(result[0], result[1], result[2], result[3], result[4], result[5])
    except Exception:
        return None
        
def save_uploaded_file(user, i):
    """保存上传文件并返回一个UploadResource记录。修改此函数以修改文件的存储过程"""
    extname = get_ext_name(i.name)
    try:
        mime = MimeType.objects.get(extname__exact=extname)
    except MimeType.DoesNotExist:
        mime = MimeType()
        mime.extname = extname
        mime.minor = extname
        mime.save()

    content = i.read()
    if mime.magic_number != "" and not content.startswith(mime.magic_number):
        raise IllegalFileFormat(i.name, mime)

    filename = time.strftime(UPLOAD_FILE_FOLDER)
    filename = os.path.join(filename, i.name)
    dest = os.path.join(MEDIA_ROOT, filename)
    
    (path, name) = os.path.split(dest)
    if not os.path.isdir(path):
        os.makedirs(path)

    count = 0
    while os.path.isfile(dest):
        count += 1
        dest = os.path.join(MEDIA_ROOT, filename[0:-len(extname)] + str(count) + "." + extname)
        
    if count > 0:
        filename = filename[0:-len(extname)] + str(count) + "." + extname
     
    file = open(dest, "wb")
    file.write(content)
    file.close()
    
    result = UploadResource()
    result.filename = filename
    result.mime = mime
    result.owner = user
    # result.md5code = md5(content).hexdigest() # 暂时不用。
    
    if mime.major == u'image':
        result.taketime = get_take_time(content)

    result.save()
    return result


def get_thumb_image(id, x, y):
    """获取缩略图"""
    x = int(x)
    if x > MAX_THUMBNAIL_SIZE:
        x = MAX_THUMBNAIL_SIZE

    y = int(y)
    if y > MAX_THUMBNAIL_SIZE:
        y = MAX_THUMBNAIL_SIZE

    try:
        record = UploadResource.objects.get(id=id)
        result = Image.open(record.filename.path)
        result.thumbnail((x, y), Image.ANTIALIAS)
        return result
    except Exception, error:
        return None

