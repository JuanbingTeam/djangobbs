from uploads.models import *
from uploads.config import UPLOAD_FILE_FOLDER
from settings import MEDIA_ROOT
from md5 import md5
from cStringIO import StringIO

import os.path
import time
import PIL

def get_ext_name(fullname):
    """获取文件的扩展名。（不包括.）"""
    i = fullname.find('.')
    result = ""
    if i > -1:
        result = fullname[i+1:]
    if len(result) > 10:
        result = ""
    return result

def getTakeTime(content):
    """获取照片的拍摄时间"""
    file = StringIO(content)
    tag = exif.process_file(file)
    file.close()
    originalTime = str(tag["EXIF DateTimeOriginal"])
    if originalTime == None:
        return None
    else:
        result = "'" + originalTime[0:4] + "/"  + originalTime[5:7] + "/" + originalTime[8:] + "'"
        print result
        result = time.strptime("%Y/%m/%d %H%M%S", result)
        return result

def saveFile(user, i):
    """保存上传文件并返回一个UploadResource记录。修改此函数以修改文件的存储过程"""
    extname = get_ext_name(i.name)
    try:
        e.objects.get(extname__exact=extname)
    except MimeType.DoesNotExist:
        mime = MimeType()
        mime.extname = extname
        mime.minor = extname
        mime.save()

    filename = strftime(UPLOAD_FILE_FOLDER)
    filename = os.path.join(filename, i.name)
    filename = os.path.join(MEDIA_ROOT, folder)
    realname = filename[:]

    count = 0
    while os.path.isdir(realname):
        realname = filename[0:-len(extname)] + str(count) + "." + extname

    content = i.read()
    file = open(filename, "wb")
    file.write(content)
    file.close()

    result = UploadResource()
    result.filename = filename
    result.mime = mime
    result.owner = user
    result.md5code = md5(content).hexdigest()
    
    if mime.major == 'image':
        result.taketime = getTakeTime(content)
    result.save()
    
    return result


def getThumbImage(id, x, y):
    try:
        record = UploadResource.get(id=id)
        record.getFile()
    except UploadResource.DoesNotExist:
        return None

