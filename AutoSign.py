'''每小时判断一次，判断是否为上午09点'''
# !python3
# coding=UTF-8
import sys  # 系统调用
import os   # 用于获取脚本的绝对路径
# 从单一文件ConnectToUSTC.py中引入依赖的方式：其中ConnectToUSTC.py用到的依赖不需要再次引入
from ConnectToUSTC import getYmlConfig, conn_USTC  # 连接USTC统一身份认证
from Sign import USTC_dailysign # 进行一次每日上报
import time  # 系统时间


'''自动打卡的执行程序'''
def AutoSign():
    abs_file = os.path.abspath(sys.argv[0])
    abs_dir = abs_file[:abs_file.rfind("/")]    # 父文件夹绝对路径
    config = getYmlConfig(abs_dir + '/config.yml')
    users = config['users']
    for user in users:
        session = conn_USTC(user)
        USTC_dailysign(session, user)

if __name__ == "__main__":
    while 1:
        time_now = time.strftime("%H", time.localtime())
        if (time_now == "09"):
            print('Auto Sign Start:')
            AutoSign()
            print('Auto Sign succeeded at {0}!'.format(time.strftime("%Y-%M-%D %H:%M:%S", time.localtime())))
            print('\n')
            time.sleep(3600)
            # 待测试是否成功
            # 考虑整一个QQ机器人，每次成功打卡就给我发消息
        else:
            # 睡眠1h=3600s
            time.sleep(3600)