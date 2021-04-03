import json
import time
import requests
import re

# 填写Server酱key
SC_KEY = ""
# 填写学号
ID_NUM = ""
# 填写告警余额（低于此值发送信息）
BALANCE = 30


def get_balance(id_num):
    query_url = "https://pay.shu.edu.cn/EPAY/Home/QueryAccount"
    query_data = {'card': id_num}
    html = requests.post(url=query_url, data=query_data).text
    balance = re.search('<input type="text" class="form-control" id="txt_balance" value="(.*?)" readonly>', html)
    return balance.group(1)


def check_balance(id_num, alarm_balance, key):
    balance = get_balance(id_num)
    # print(balance)
    if float(balance) <= alarm_balance:
        return send_notice(id_num, balance, alarm_balance, key)
    return True


def send_notice(id_num, current_balance, alarm_balance, key):
    title = "账户%s余额低于%s元" % (id_num, alarm_balance)
    desp = "您的上海大学一卡通账户%s：\n\n" \
           "当前余额为%s元，低于设定的告警余额%s元，请尽快充值，以免影响使用。\n\n" \
           "上海大学官方充值渠道：\n\n" \
           "[https://pay.shu.edu.cn/epay/home/query](https://pay.shu.edu.cn/epay/home/query) \n\n" \
           "_____________________________________\n\n" \
           "检测时间：%s" \
           % (id_num, current_balance, alarm_balance, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    sc_msg = scSend(title, desp, key)
    # print(sc_msg)
    if sc_msg != False and sc_msg['errmsg'] == 'success':
        return True
    else:
        return False


def scSend(title, desp, key):
    url = "http://sc.ftqq.com/%s.send" % key
    data = {'text': title, 'desp': desp}
    text = ''
    try:
        text = requests.post(url, data=data).text
        result = json.loads(text)
        return result
    except Exception as e:
        print(text)
        print(e)
        return False


if __name__ == '__main__':
    print(check_balance(ID_NUM, BALANCE, SC_KEY))
