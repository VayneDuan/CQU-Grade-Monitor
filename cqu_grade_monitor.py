# !/usr/bin/env python3
# coding:UTF-8
# -*- coding: utf-8 -*-
import re
import requests
import hashlib
import time
from consts import *
from time import strftime, localtime
from msgPush import *
from TYRZ.enroll import getScoreJson, getAccessTokenDict
from TYRZ.tyrz import getLoginData
import _thread
if useVpn:
  import socket
  import socks
  socks.set_default_proxy(socks.SOCKS5, vpnUrl, vpnPort)
  socket.socket = socks.socksocket
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #
import pprint   
import os
if not os.path.exists('./logs/error.log'):
  with open('./logs/error.log','w', encoding='UTF-8') as f:
    f.write('init')
    f.write("\n")
if not os.path.exists('./logs/email.log'):
  with open('./logs/email.log','w', encoding='UTF-8') as f:
    f.write('init')
    f.write("\n")
def monitor():
  errorCount = 0
  ssthresh = 1
  grade_dic = {}
  mark_dic = {}

  s = getLoginData(username, password)
  header = getAccessTokenDict(s)
  s.close()
  old_grade = {
      'status': 'success',
      'msg': None,
      'data': {
          '2021春': []
      },
      'code ': None
  }

  # print(old_grade)
  totalSleepTime = 0

  #! 启动时进行推送测试
  if(pushTest):
    testPush()
  while(1):
    try:
      new_grade = getScoreJson(header)
      # print(new_grade)
      new_grade_find = False
      if len(new_grade['data'][f'{xn+xq}{words[xq]}']) != len(old_grade['data'][f'{xn+xq}{words[xq]}']):
        new_grade_find = True

      if totalSleepTime >= 60*60:
        s = getLoginData(username, password)
        s.close()
        header = getAccessTokenDict(s)
        totalSleepTime = 0

      if(not new_grade_find):
        print(strftime("%Y-%m-%d %H:%M:%S", localtime()), end='\t')
        print("没有新成绩")
        #pprint.pprint(new_grade)     
      else:
        grades = new_grade['data'][f'{xn+xq}{words[xq]}']
        grades_old = old_grade['data'][f'{xn+xq}{words[xq]}']
        old_ids = [i['id'] for i in grades_old]
        course_num = len(grades)
        delta_course = len(
            new_grade['data'][f'{xn+xq}{words[xq]}']) - len(old_grade['data'][f'{xn+xq}{words[xq]}'])
        for j in range(course_num):
          gr_obj = grades[j]
          gr_id = gr_obj['id']
          if not gr_id in old_ids:
            new_course = gr_obj['courseName']
            new_score = gr_obj['effectiveScoreShow']
            print(strftime("%Y-%m-%d %H:%M:%S", localtime()), end='\t')
            print(f"有新成绩了, {new_course}:{new_score}")
            _thread.start_new_thread( gradePush,(new_course, new_score))
            # gradePush(new_course, new_score)
      old_grade = new_grade

    except Exception as e:
      errorCount += 1
      if(errorCount == ssthresh):
        errorPush()
        ssthresh = 5*ssthresh
      errorTime = strftime("%Y-%m-%d %H:%M:%S \t", localtime())
      errorInfo = '第 '+str(errorCount) + ' 次错误\n\n'
      s = errorTime+errorInfo
      with open('./logs/error.log', 'a', encoding='UTF-8') as f:
        f.write(s)
        f.write(str(e))
        f.write("\n")
      print(e)

    totalSleepTime += sleepTime
    time.sleep(sleepTime)


if __name__ == "__main__":
  monitor()
