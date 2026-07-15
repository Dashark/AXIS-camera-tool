# -*- coding:utf-8 -*-

import re
import subprocess
import requests
from base_info import *
from logconfig import logger
from requests.auth import HTTPDigestAuth

class MyHttp:
    def __init__(self, ip):
        self.addr = "http://"+ip
        self.ip=ip
        self.net_is_ok=False
        self.auth = HTTPDigestAuth(username, password)
        self.schedule_is_ok=False
        self.Recipient_is_ok = False

    def check_net(self):
        result = subprocess.run(['ping', '-n', '4', self.ip],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            self.net_is_ok=True
            logger.info(f"{self.ip}网络正常")
        else:
            self.net_is_ok=False
            logger.warning(f"{self.ip}网络不通")


    def AddScheduledEvent(self,path="/vapix/services"):
        """
        设置日程表
        """
        start_time_format="19700101T"+start_time.replace(":","")
        end_time_format = "19700101T"+end_time.replace(":", "")
        xml_data=f'''<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope
      xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope"
    >
      <SOAP-ENV:Header/>
      <SOAP-ENV:Body xmlns:aev="http://www.axis.com/vapix/ws/event1">

    <aev:AddScheduledEvent>
        <aev:NewScheduledEvent>
          <aev:Name>daily</aev:Name>
          <aev:EventID>com.axis.schedules.after_hours</aev:EventID>
          <aev:Schedule>
              <aev:ICalendar Dialect="http://www.axis.com/vapix/ws/ical1">DTSTART:{start_time_format}
DTEND:{end_time_format}
RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU</aev:ICalendar>
          </aev:Schedule>
        </aev:NewScheduledEvent>
    </aev:AddScheduledEvent>
      </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

        url = self.addr + path
        if self.net_is_ok:
            # req = requests.post(url, auth=self.auth,data=xml_data,headers=header)
            while True:
                req = requests.post(url, auth=self.auth, data=xml_data)
                if req.status_code==200:
                    logger.info("日程表设置成功")
                    self.schedule_is_ok=True
                    break
                elif "already exists" in req.text:
                    self.RemoveSchedule()
                else:
                    logger.error("日程表设置失败")
                    break

    def AddRecipient(self, path="/vapix/services"):
        """
        设置日收件人
        """
        xml_data = f'''<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope
      xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope"
    >
      <SOAP-ENV:Header/>
      <SOAP-ENV:Body xmlns:act="http://www.axis.com/vapix/ws/action1">
        
      <act:AddRecipientConfiguration>
         <act:NewRecipientConfiguration>
            <act:Name>reboot</act:Name>
            <act:TemplateToken>com.axis.recipient.http</act:TemplateToken>
            <act:Parameters>               <act:Parameter Name="upload_url" Value="http://{self.ip}/axis-cgi/restart.cgi"/>
               <act:Parameter Name="login" Value="{username}"/>
               <act:Parameter Name="password" Value="{password}"/>
               <act:Parameter Name="qos" Value="0"/>
               <act:Parameter Name="proxy_host" Value=""/>
               <act:Parameter Name="proxy_port" Value=""/>
               <act:Parameter Name="proxy_login" Value=""/>
               <act:Parameter Name="proxy_password" Value=""/>
</act:Parameters>
         </act:NewRecipientConfiguration>
      </act:AddRecipientConfiguration>
      </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

        url = self.addr + path
        if self.net_is_ok:
            # req = requests.post(url, auth=self.auth,data=xml_data,headers=header)
            req = requests.post(url, auth=self.auth, data=xml_data)
            if req.status_code == 200:
                logger.info("收件人设置成功")
                self.Recipient_is_ok=True
            else:
                logger.error("收件人设置失败")

    def AddActionRule(self,path="/vapix/services"):
        """
        设置规则
        """
        config_xml_data = f'''<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope
      xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope"
    >
      <SOAP-ENV:Header/>
      <SOAP-ENV:Body xmlns:act="http://www.axis.com/vapix/ws/action1" xmlns:aev="http://www.axis.com/vapix/ws/event1" xmlns:wsnt="http://docs.oasis-open.org/wsn/b-2" xmlns:tns1="http://www.onvif.org/ver10/topics" xmlns:tnsaxis="http://www.axis.com/2009/event/topics">
        <act:AddActionConfiguration>
      <act:NewActionConfiguration>
        <act:Name>通过 HTTP 发送通知</act:Name>
        <act:TemplateToken>com.axis.action.fixed.notification.http</act:TemplateToken>
        <act:Parameters>
<act:Parameter Name="parameters" Value=""/>
<act:Parameter Name="message" Value=""/>
<act:Parameter Name="upload_url" Value="http://192.168.0.90/axis-cgi/restart.cgi"/>
<act:Parameter Name="qos" Value="0"/>
<act:Parameter Name="login" Value="root"/>
<act:Parameter Name="password" Value="pass"/>
<act:Parameter Name="proxy_host" Value=""/>
<act:Parameter Name="proxy_port" Value=""/>
<act:Parameter Name="proxy_login" Value=""/>
<act:Parameter Name="proxy_password" Value=""/>
</act:Parameters>
      </act:NewActionConfiguration>
     </act:AddActionConfiguration>
      </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

        url = self.addr + path
        if self.net_is_ok and self.schedule_is_ok and self.Recipient_is_ok:
            # req = requests.post(url, auth=self.auth,data=xml_data,headers=header)
            config_req = requests.post(url, auth=self.auth, data=config_xml_data)
            pattern = r'<aa:ConfigurationID>(\d+)</aa:ConfigurationID>'
            # 使用 re.search 查找匹配的内容
            match = re.search(pattern, config_req.text)
            # 检查是否找到匹配
            if match:
                # 提取第一个捕获组的内容，即配置 ID
                Action_id = match.group(1)

                rule_xml_data = f'''<?xml version="1.0" encoding="UTF-8"?>
                    <SOAP-ENV:Envelope
                      xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope"
                    >
                      <SOAP-ENV:Header/>
                      <SOAP-ENV:Body xmlns:act="http://www.axis.com/vapix/ws/action1" xmlns:aev="http://www.axis.com/vapix/ws/event1" xmlns:wsnt="http://docs.oasis-open.org/wsn/b-2" xmlns:tns1="http://www.onvif.org/ver10/topics" xmlns:tnsaxis="http://www.axis.com/2009/event/topics">

                    <act:AddActionRule>
                      <act:NewActionRule>
                        <act:Name>reboot</act:Name>
                        <act:Enabled>true</act:Enabled>
                        <act:StartEvent><wsnt:TopicExpression Dialect="http://docs.oasis-open.org/wsn/t-1/TopicExpression/Concrete">tns1:UserAlarm/tnsaxis:Recurring/Interval</wsnt:TopicExpression><wsnt:MessageContent Dialect="http://www.onvif.org/ver10/tev/messageContentFilter/ItemFilter">boolean(//SimpleItem[@Name="id" and @Value="com.axis.schedules.after_hours"]) and boolean(//SimpleItem[@Name="active" and @Value="1"])</wsnt:MessageContent></act:StartEvent>


                        <act:PrimaryAction>{Action_id}</act:PrimaryAction>
                      </act:NewActionRule>
                    </act:AddActionRule>

                      </SOAP-ENV:Body>
                    </SOAP-ENV:Envelope>'''

                rule_req=requests.post(url, auth=self.auth, data=rule_xml_data)
                if (config_req.status_code+rule_req.status_code) == 400:
                    logger.info("规则设置成功")

                else:
                    logger.error("规则设置失败")
            else:
                logger.error("规则设置失败")



    def RemoveActionRule(self,Action_id, path="/vapix/services"):
        """
        删除规则
        """
        xml_data = f'''<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope
      xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope"
    >
      <SOAP-ENV:Header/>
      <SOAP-ENV:Body xmlns:act="http://www.axis.com/vapix/ws/action1" xmlns:aev="http://www.axis.com/vapix/ws/event1" xmlns:wsnt="http://docs.oasis-open.org/wsn/b-2" xmlns:tns1="http://www.onvif.org/ver10/topics" xmlns:tnsaxis="http://www.axis.com/2009/event/topics">
        
    <act:RemoveActionConfiguration>
      <act:ConfigurationID>{Action_id}</act:ConfigurationID>
    </act:RemoveActionConfiguration>
  
      </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

        url = self.addr + path
        if self.net_is_ok:
            # req = requests.post(url, auth=self.auth,data=xml_data,headers=header)
            req = requests.post(url, auth=self.auth, data=xml_data)
            if req.status_code == 200:
                logger.info("删除规则成功")
            else:
                logger.error("删除规则失败")

    def RemoveSchedule(self, type="after_hours", path="/vapix/services"):
        """
        删除删除日程表
        """
        xml_data = f'''<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope
      xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope"
    >
      <SOAP-ENV:Header/>
      <SOAP-ENV:Body xmlns:aev="http://www.axis.com/vapix/ws/event1">
        
      <aev:RemoveScheduledEvent>
          <aev:EventID>com.axis.schedules.{type}</aev:EventID>
      </aev:RemoveScheduledEvent>
      </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>'''

        url = self.addr + path
        if self.net_is_ok:
            # req = requests.post(url, auth=self.auth,data=xml_data,headers=header)
            req = requests.post(url, auth=self.auth, data=xml_data)
            if req.status_code == 200:
                logger.info("删除日程表成功")
            else:
                logger.error("删除日程表失败")

    def app_action(self,package,action="remove"):
        """操作应用，action：remove、start、stop、restart"""
        action_lit=["remove","start","stop","restart"]
        url=self.addr + "/axis-cgi/applications/control.cgi"
        if action not in action_lit:
            logger.error(f"action参数必须在{action_lit}之中")
        else:
            post_data={"action":action,"package":package}
            req = requests.get(url, auth=self.auth, params=post_data)
            if req.status_code == 200:
                logger.info(f"{action}--{package}成功")
            else:
                logger.error(f"{action}--{package}失败")

if __name__ == "__main__":
    for ip in app_ip_list:
        logger.info(f"======开始设定{ip}相机应用======")
        app_http = MyHttp(ip=ip)
        app_http.check_net()
        if app_http.net_is_ok:
            try:
                app_http.app_action(package=app_name,action=action)
            except Exception as e:
                logger.error(f"设定{ip}相机应用时出现异常：{e}")
    else:
        logger.info("相机应用配置完成")

    for ip in reboot_ip_list:
        logger.info(f"======开始设定{ip}相机重启======")
        test_http=MyHttp(ip=ip)
        test_http.check_net()
        if test_http.net_is_ok:
            try:
                test_http.AddScheduledEvent()
                test_http.AddRecipient()
                test_http.AddActionRule()
            except Exception as e:
                logger.error(f"设定{ip}相机重启时出现异常：{e}")
    else:
        logger.info("相机重启配置完成")

    input("执行完成，按任意键退出")




