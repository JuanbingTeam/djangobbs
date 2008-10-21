#!/usr/bin/env python
#coding=utf-8


import Image, ImageFont
from settings import MEDIA_ROOT
import os.path

VALIDATE_IMAGE_SIZE = (100, 24)
VALIDATE_IMAGE_FORE_GROUND = (255, 255, 255)
VALIDATE_IMAGE_BACK_GROUND = Image.open(os.path.join(MEDIA_ROOT, "accounts/validate-code-backgroud.png"))
#VALIDATE_IMAGE_FONT = ImageFont.truetype("arial.ttf", 18)
VALIDATE_IMAGE_FONT = ImageFont.truetype("fonts/consola.ttf", 18)
