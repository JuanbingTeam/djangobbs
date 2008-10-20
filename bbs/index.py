#!/usr/bin/env python
#coding=utf-8


from django.shortcuts import render_to_response

def index(request):
    data = {'request':request}
    return render_to_response('index.html', data)
