#coding:utf-8

import itchat, time
from itchat.content import *


keytime = time.strftime('%Y-%m-%d', time.localtime(time.time()))

@itchat.msg_register([TEXT])
def text_reply(msg):
    print msg
    keywords = []
    keywords.append(u'年')
    keywords.append(u'鸡')
    keywords.append(u'春')
    keywords.append(u'新')
    keywords.append(u'拜')
    keywords.append(u'财')
    print keywords
    for item in keywords:
        print "item is :" + item
        if item in msg['Content']:
            # while True:
            if keytime == '2017-02-01':
                print keytime
                itchat.send((u'恭喜发财'), msg['FromUserName'])
            else:
                print "not " + keytime
                itchat.send((u'鸡年大吉'), msg['FromUserName'])
            break


@itchat.msg_register([PICTURE, RECORDING, VIDEO, SHARING])
def other_reply(msg):
    if keytime == '2017-02-01':
        itchat.send((u'恭喜发财'), msg['FromUserName'])
    else:
        itchat.send((u'鸡年大吉'), msg['FromUserName'])

itchat.auto_login(enableCmdQR=2,hotReload=True)
#
# itchat.run()
itchat.run(debug=True)
