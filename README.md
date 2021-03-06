# CQU-Grade-Monitor
# 重庆大学成绩监控
## :gem: 目前实现的功能

- [x] 成绩实时监控
- [x] 服务器&PC运行皆可
- [x] 邮件通知
- [x] 微信推送
- [x] 手机推送(iOS)
- [x] 程序运行错误报警推送 *[邮件+微信+手机]*

> ### 欢迎有想法的朋友和我邮件交流, 包括但不限于功能扩展、设计优化等

## :alien: 待实现

- [ ] 代码重构
- [ ] 对非程序员更友好, 如设计GUI
- [ ] 支持`pip install`, 开箱即用
- [ ] ~~小程序~~
- [ ] 设计为1对多模式, 服务器跑主程序, 用户在web页面提交`username`, `password`等参数即可开始监控 
   
## :blue_heart: 运行配置说明

0. **需要进行配置的地方为 33-48 行, 其余部分不需要更改**

1. 可以跑在服务器上, 注意使用`nuhup`和`输出重定向`来实现后台持久化运行, 提供参考命令如下:

   **`nohup python3 -u cqu_grade_monitor.py > grade.log 2>&1 &`**

   - 如果想看实时监控进展, 可以通过`tail -f grade.log`查看; 

   - 如果想看错误日志, 可以通过`cat error.log`查看; 

   - 如果想看邮件发送日志, 可以通过`cat mail.log`查看;

2. 也可以跑在自己的电脑上, `cmd`窗口实时显示, 也可以后台运行, 自行研究一下

3. 需要使用到的库已经放在requirements.txt，分别是`requests`和`bs4`, 使用pip安装的可以使用指令
   
   `pip install -r requirements.txt`

4. 运行出错警报采用**指数退避方式**推送, 第一个目的是能实现持久警报, 防止看漏消息, 没注意到警报; 第二个目的是避免人在外面, 无法解决问题, 但是一直警报的烦恼;

5. **脚本稳定性有待提升[学校服务器不稳定], 后续会逐渐完善, 请谅解!**

6. **有问题欢迎提`issue`或者联系`vayneduan@foxmail.com`**

## :warning: 特别声明
   - 本仓库发布的项目中涉及的任何脚本，仅用于测试和学习研究，禁止用于商业用途及各种引流或者任何非法目的
   - 本脚本不存储、不上传用户的账号、密码, 不会导致密码泄露等问题. `VayneDuan`对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害
   - 间接使用脚本的任何用户，包括但不限于建立VPS或在某些行为违反国家/地区法律或相关法规的情况下进行传播, `VayneDuan`对于由此引起的任何隐私泄漏或其他后果概不负责
   - 如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我将在收到认证文件后删除相关脚本
   - 以任何方式查看此项目的人, 以及直接或间接使用本项目的任何脚本的人都应仔细阅读此声明, `VayneDuan`保留随时更改或补充此声明的权利。一旦使用并复制了任何相关脚本或者本项目，则视为您已接受此特别声明
   - 本项目遵循`GPL-2.0 License`协议，如果本特别声明与`GPL-2.0 License`协议有冲突之处，以本特别声明为准

