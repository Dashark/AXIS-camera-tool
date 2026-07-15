# -*- coding:utf-8 -*-

from config import Config

config = Config()

# 重启配置
start_time=config.get("start_time")
end_time=config.get("end_time")
username=config.get("username")
password=config.get("password")
reboot_ip_list = config.get("reboot_ip_list")


# 操作应用配置
action = config.get("action")
app_name = config.get("app_name")
app_ip_list = config.get("app_ip_list")

