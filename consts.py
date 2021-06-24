import os
import configparser
import hashlib


curpath = os.path.dirname(os.path.realpath(__file__))
cfgpath = os.path.join(curpath, "config.ini")
conf = configparser.ConfigParser()
conf.read(cfgpath, encoding="utf-8")


sections = conf.sections()
acco = conf.items('account')
username = conf.get('account', 'studentId')
password = conf.get('account', 'password')


xn = conf.get('time', 'xuenian')
xq = conf.get('time', 'xueqi')

if xn == '' and xq == '':
  import datetime
  xn = datetime.datetime.now().year
  xq = datetime.datetime.now().month >= 10 and \
        datetime.datetime.now().month <= 5
  # 1 是秋季学期
  # 0 是春季学期
  xq = not xq
  if xq == 1: xn -= 1

mailPush    = conf.get('notify', 'mailPush') == 'True'
mailKey     = conf.get('notify', 'mailKey')
mailAccount = conf.get('notify', 'mailAccount')
appPush     = conf.get('notify', 'appPush') == 'True'
barkKey     = conf.get('notify', 'barkKey')
wechatPush  = conf.get('notify', 'wechatPush') == 'True'
ftKey       = conf.get('notify', 'ftKey')
pushTest    = conf.get('notify', 'pushTest') == 'True'