import re
import requests
import hashlib
import time
from consts import *
from time import strftime, localtime
from bs4 import BeautifulSoup
#* 邮件发送 *#
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from time import strftime, localtime
import datetime

words = ['秋', '春']
mailPush = False
appPush = False
wechatPush = True
pushTest = False

sleepTime = 300  # ! 两次查询之间的间隔时间, 不建议修改
api = "https://sc.ftqq.com/"+ftKey+".send"  # ! 方糖请求url, 不要修改
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #

mailSERVER = {
    'host': "smtp.qq.com",
    'port': 465
}

mailUSER = {
    "email": mailAccount,  # 邮箱登录账号
    "password": mailKey  # 发送人邮箱的授权码
}


class PersonMail(object):
  def __init__(self, receivers, sender=mailUSER["email"]):
    self.From = sender
    self.To = receivers
    self.msg = ''

  def write_msg(self, subject, content):
    self.msg = MIMEText(content, 'plain', 'utf-8')
    self.msg['From'] = Header(self.From)
    self.msg['To'] = Header(str(";".join(self.To)))
    self.msg['Subject'] = Header(subject)

  def send_email(self):
    try:
      smtp_client = smtplib.SMTP_SSL(mailSERVER["host"], mailSERVER["port"])
      smtp_client.login(mailUSER["email"], mailUSER["password"])
      smtp_client.sendmail(self.From, self.To, self.msg.as_string())
      smtp_client.quit()
      code = 1
      success_info = "[INFO]\t" + \
          strftime("%Y-%m-%d %H:%M:%S \t", localtime()) + \
          f"发送到 {self.To[0]}"+" 成功!"
      return code, success_info
    except smtplib.SMTPException as e:
      code = 0
      error_info = "[ERROR]\t"+strftime("%Y-%m-%d %H:%M:%S \t", localtime())+e
      return code, error_info


def send_to_somebody(mailAddress, course, grade):
  receivers = [mailAddress]
  mail = PersonMail(receivers)
  mail.write_msg(f"{course}出成绩啦!", f"您的成绩是: {grade}分, 详情请登录 202.202.1.41 查看")
  code, result = mail.send_email()
  return code, result


def testPush():
  if(mailPush):
    mailCode, mailInfo = send_to_somebody(mailAccount, '启动成功====', '邮件功能正常')
    print('邮件正常')
  if(wechatPush):
    title = "启动成功了"
    content = "微信推送功能正常"
    data = {
        "text": title,
        "desp": content
    }
    req = requests.post(api, data=data)
    print('微信推送正常')
  if(appPush):
    requests.get(
        f"https://api.day.app/{barkKey}/启动成功/手机推送功能测试正常?isArchive=1&sound=bell")
    print('手机推送正常')


def gradePush(new_course, new_score):
  #! [成绩推送] 邮件
  if(mailPush):
    mailCode, mailInfo = send_to_somebody(mailAccount, new_course, new_score)
    if(mailCode):
      with open('./mail.log', 'a', encoding='UTF-8') as f:
        f.write(mailInfo)
    else:
      with open('./error.log', 'a', encoding='UTF-8') as f:
        f.write(mailInfo)

  #! [成绩推送] 微信
  if(wechatPush):
    title = f"{new_course}出成绩了"
    content = f"你的分数是{new_score}分"
    data = {
        "text": title,
        "desp": content
    }
    req = requests.post(api, data=data)

  #! [成绩推送] APP
  if(appPush):
    requests.get(
        f"https://api.day.app/{barkKey}/{new_course} 出成绩了/你的分数是{new_score}?isArchive=1&sound=bell")


def errorPush():
  #! [错误报警] APP
  if(appPush):
    requests.get(
        f"https://api.day.app/{barkKey}/错误报警/程序运行出错了, 快去看看吧?isArchive=1&sound=bell")
  #! [错误报警] 微信
  if(wechatPush):
    title = f"运行出错了"
    content = f"快去检查一下吧!"
    data = {
        "text": title,
        "desp": content
    }
    req = requests.post(api, data=data)
  #! [错误报警] 邮件
  if(mailPush):
    mailCode, mailInfo = send_to_somebody(
        mailAccount, '程序出错了=====', '程序出错了=====')
    if(mailCode):
      with open('./mail.log', 'a', encoding='UTF-8') as f:
        f.write(mailInfo)
    else:
      with open('./error.log', 'a', encoding='UTF-8') as f:
        f.write(mailInfo)
