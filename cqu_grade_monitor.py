#!/usr/bin/env python3
# coding:UTF-8
# -*- coding: utf-8 -*-
import re, os, json
import requests, random
import hashlib, time
from time import strftime, localtime
import urllib.request
from bs4 import BeautifulSoup

#* 邮件发送 *#
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from time import strftime, localtime

mailKey = 'XXXXXXXXXXXXXXXXXXXXX 填 你 自 己 的 KEY  XXXXXXXXXXXXXXXXXXXXXXXXXXX'
mailAccount = 'XXXXXXXXXXXXXXXXXXXXX 填 你 自 己 的 邮 箱 XXXXXXXXXXXXXXXXXXXXXXXXXXX'
# 设置SMTP服务器以及登录信息
mailSERVER = {
    'host': "smtp.qq.com",
    'port': 465
}

mailUSER = {
    "email":mailAccount,  # 邮箱登录账号
    "password": mailKey  # 发送人邮箱的授权码
}

class PersonMail(object):
    def __init__(self, receivers, sender=mailUSER["email"]):
        self.From = sender
        self.To = receivers
        self.msg = ''

    def write_msg(self, subject, content):
        # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
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
            success_info = "[INFO]\t"+strftime("%Y-%m-%d %H:%M:%S \t", localtime())+f"发送到 {self.To[0]}"+" 成功!"
            return code,success_info
        except smtplib.SMTPException as e:
            code = 0
            error_info = "[ERROR]\t"+strftime("%Y-%m-%d %H:%M:%S \t", localtime())+e
            return code,error_info

def send_to_somebody(mailAddress,course,grade):
        receivers = [mailAddress]
        mail = PersonMail(receivers)
        mail.write_msg(f"{course}出成绩啦!", f"您的成绩是: {grade}分, 详情请登录 202.202.1.41 查看")
        code,result = mail.send_email()
        return code,result
#* 邮件发送 *#

alternative_url_202 = 'http://202.202.1.41/'
alternative_url_jxgl = 'http://jxgl.cqu.edu.cn/'

url = alternative_url_202  #! 如果学校服务器出现问题, 可以替换成: alternative_url_jxgl
homeUrl = url+"home.aspx"
loginUrl = url+"_data/index_login.aspx"
scoreUrl = url+"/XSCJ/Stu_MyScore_print_rpt.aspx?xn=2020&xq=0&rpt=0&rad=2&zfx_flag=0" #xn: 学年, xq: 学期(0:上学期, 1:下学期)
schoolcode = "10611"
url_google = 'http://translate.google.cn'
reg_text = re.compile(r'(?<=TRANSLATED_TEXT=).*?;')
user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 r'Chrome/44.0.2403.157 Safari/537.36'
last_file = ""

def getView():
    view = []
    r = re.compile(
        r'<input type="hidden" name="__VIEWSTATE" value="(.*?)" \/>')
    data = requests.get(loginUrl)
    view = r.findall(data.text)
    r = re.compile(
        r'<input type="hidden" name="__VIEWSTATEGENERATOR" value="(.*?)" \/>')
    data = r.findall(data.text)
    view.append(data[0])
    return view

def checkPwd(self):
    p = hashlib.md5(password.encode()).hexdigest()
    p = hashlib.md5(( username + p[0:30].upper() + schoolcode).encode()).hexdigest()
    return p[0:30].upper()

def login():
    view = getView()
    psw = checkPwd(view)
    datas = {
        '__VIEWSTATE':view[0],
        '__VIEWSTATEGENERATOR': view[1],
        'Sel_Type': ' STU',
        'txt_dsdsdsdjkjkjc': username,
        'txt_dsdfdfgfouyy': password,
        'txt_ysdsdsdskgf': '',
        'pcInfo': '',
        'typeName': '',
        'aerererdsdxcxdfgfg': '',
        'efdfdfuuyyuuckjg': psw
        }
    headers = {
        'Accept':'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3',
        'Connection':'Keep-Alive',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14392'
        }
    html = requests.get(homeUrl, headers = headers)
    cookies = html.cookies
    requests.post(loginUrl, headers = headers, cookies = cookies, data = datas)
    html = requests.get(scoreUrl, headers=headers, cookies=cookies)
    return html

def get(html):
    html.text.encode('utf-8')
    return html.text

def work(result,grade_dic,init,mark_dic,courseNum):
    result = re.sub('<head>.*?</head>', "", result)
    result = re.sub('<input.*?>', "", result)
    result = re.sub('<span.*?</span>', "", result)
    result = re.sub('<table width=.857.*?</table>', "", result)

    coursePos = [10+9*i for i in range(courseNum)]
    gradePos = [x+5 for x in coursePos]

    soup = BeautifulSoup(result, 'html.parser')
    s = soup.findAll('table')
    s = s[3]
    #print(s)

    s1=s.findAll('td')
    for i in range(len(coursePos)):
        name = s1[coursePos[i]].get_text()
        pos = name.index(']')
        name = name[pos+1:]
        grade_dic[name] = s1[gradePos[i]].get_text()
        if(init and s1[gradePos[i]].get_text()!='未录入'):
            mark_dic[name] = 1
    #print(grade_dic)
    return result

def show(final):
    intime = open('result.html', "w")
    intime.write(final)
    os.startfile(r".\result.html")

if __name__ == "__main__":
    def monitor(courseNum):
        global username
        username = 'XXXXXXXXXXXXXXXXXXXXX 填 你 自 己 的 教务网账号 XXXXXXXXXXXXXXXXXXXXXXXXXXX'
        global password
        password = 'XXXXXXXXXXXXXXXXXXXXX 填 你 自 己 的 教务网密码 XXXXXXXXXXXXXXXXXXXXXXXXXXX'

        key = 'XXXXXXXXXXXXXXXXXXXXX 填 你 自 己 的 方糖KEY XXXXXXXXXXXXXXXXXXXXXXXXXXX'
        api = "https://sc.ftqq.com/"+key+".send"

        errorCount = 0
        ssthresh = 1

        grade_dic = {}
        mark_dic = {}
        html   = login()
        result = get(html)
        final  = work(result,grade_dic,True,mark_dic,courseNum)
        print('首次启动:\n',grade_dic)

        '''以下是首次启动时的推送测试, 请自行决定是否开启
        mailCode,mailInfo = send_to_somebody("XXXXXXXXXXXXXXXXXXXXX 填 你 自 己 的 邮箱 XXXXXXXXXXXXXXXXXXXXXXXXXXX",'启动成功====','邮件功能正常')
        print('邮件正常')
        title = "启动成功了"
        content = "微信推送功能正常"
        data = {
        "text":title,
        "desp":content
        }
        req = requests.post(api,data = data)
        print('微信推送正常')
        requests.get(f"https://api.day.app/XXXXXXXXXXXXXXXXXXXXX 填 你 自 己 的 BARK key XXXXXXXXXXXXXXXXXXXXXXXXXXX/启动成功/手机推送功能测试正常?isArchive=1&sound=bell")
        print('手机推送正常')
        '''
        while(1):
            try:
                new_grade_find = False
                time.sleep(60)
                html   = login()
                result = get(html)
                final  = work(result,grade_dic,False,mark_dic,courseNum)

                new_course = 'null'
                new_score = 'null'
                for x in grade_dic.keys():
                    if(grade_dic[x]!='未录入' and x not in mark_dic.keys()):
                        new_course = str(x)
                        new_score = str(grade_dic[x])
                        mark_dic[x] = 1
                        new_grade_find = True
                        print('NEW GRADE FOUND !')

                if(not new_grade_find):
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()),end='\t')
                    print("没有新成绩, 还有 ",str(grade_dic.values()).count('未录入'), " 门没出")
                else:
                    print(strftime("%Y-%m-%d %H:%M:%S", localtime()),end='\t')
                    print(f"有成绩了, {new_course}:{new_score}分")

                    '''[成绩推送] 邮件
                    mailCode,mailInfo = send_to_somebody("XXXXXXXXXXXXXXXXXXXXX 填 你 自 己 的 邮箱 XXXXXXXXXXXXXXXXXXXXXXXXXXX",new_course,new_score)
                    if(mailCode):
                        with open('./mail.log','a',encoding='UTF-8') as f:
                            f.write(mailInfo)
                    else:
                        with open('./error.log','a',encoding='UTF-8') as f:
                            f.write(mailInfo)
                    '''

                    title = f"{new_course} 出成绩了"
                    content = f"你的分数是{new_score}分"

                    data = {
                    "text":title,
                    "desp":content
                    }
                    ''' [成绩推送] 微信
                    req = requests.post(api,data = data)
                    '''
                    ''' [成绩推送] APP
                    requests.get(f"https://api.day.app/XXXXXXXXXXXXXXXXXXXXX 填 你 自 己 的 BARK key XXXXXXXXXXXXXXXXXXXXXXXXXXX/{new_course} 出成绩了/你的分数是{new_score}?isArchive=1&sound=bell")
                    '''
            except Exception as e:

                errorCount+=1

                if(errorCount==ssthresh):
                    ''' [错误报警] APP推送 & 邮件推送
                    requests.get("https://api.day.app/XXXXXXXXXXXXXXXXXXXXX 填 你 自 己 的 BRAK key XXXXXXXXXXXXXXXXXXXXXXXXXXX/错误报警/程序运行出错了, 快去看看吧?isArchive=1&sound=bell")
                    mailCode,mailInfo = send_to_somebody("XXXXXXXXXXXXXXXXXXXXX 填 你 自 己 的 邮箱 XXXXXXXXXXXXXXXXXXXXXXXXXXX",'程序出错了=====','程序出错了=====')
                    if(mailCode):
                        with open('./mail.log','a',encoding='UTF-8') as f:
                            f.write(mailInfo)
                    else:
                        with open('./error.log','a',encoding='UTF-8') as f:
                            f.write(mailInfo)
                    '''
                    ssthresh = 5*ssthresh

                errorTime = strftime("%Y-%m-%d %H:%M:%S \t", localtime())
                errorInfo = '第 '+str(errorCount) + ' 次错误\n\n'
                s = errorTime+errorInfo
                with open('./error.log','a',encoding='UTF-8') as f:
                    f.write(s)
                    f.write(str(e))

    '''
    请将courseNum 换成你自己的课程数量
    '''
    monitor(courseNum = 10) #教务网显示的本学期的课程数量
