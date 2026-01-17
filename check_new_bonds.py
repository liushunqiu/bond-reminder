#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可转债申购提醒脚本
扫描当天是否有可申购的新债，并通过邮件/钉钉/微信等方式通知
"""

import json
import os
import sys
from datetime import datetime, date
from typing import List, Dict, Optional

import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


def is_weekday(check_date: str = None) -> bool:
    """
    判断是否是工作日（周一到周五）
    
    Args:
        check_date: 要检查的日期字符串（格式：YYYY-MM-DD），如果为None则检查今天
    
    Returns:
        bool: True表示是工作日，False表示是周末
    """
    if check_date:
        check_date_obj = datetime.strptime(check_date, '%Y-%m-%d').date()
    else:
        check_date_obj = date.today()
    
    # 0=周一, 1=周二, 2=周三, 3=周四, 4=周五, 5=周六, 6=周日
    weekday = check_date_obj.weekday()
    return weekday < 5  # 0-4是工作日


class BondNotifier:
    def __init__(self, check_date: str = None):
        """
        初始化债券通知器
        
        Args:
            check_date: 要检查的日期字符串（格式：YYYY-MM-DD），如果为None则使用今天
        """
        if check_date:
            self.today = check_date
        else:
            self.today = datetime.now().strftime('%Y-%m-%d')
        
        # 判断是否是工作日
        self.is_weekday = is_weekday(self.today)
        print(f"开始扫描 {self.today} 的可转债申购信息...")
        print(f"日期类型: {'工作日' if self.is_weekday else '周末'}")
        
    def fetch_bond_data(self) -> List[Dict]:
        """从东方财富网获取可转债申购数据"""
        try:
            # 东方财富可转债列表API
            url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
            params = {
                "reportName": "RPT_BOND_CB_LIST",
                "columns": "SECURITY_CODE,SECURITY_NAME_ABBR,PUBLIC_START_DATE,CORRECODE",
                "pageSize": "500",
                "pageNumber": "1",
                "sortColumns": "PUBLIC_START_DATE,SECURITY_CODE",
                "sortTypes": "-1,-1",
                "source": "WEB",
                "client": "WEB"
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if data.get("result") and data["result"].get("data"):
                all_bonds = data["result"]["data"]
                
                # 筛选申购日期为今天的债券
                today_bonds = []
                for bond in all_bonds:
                    # PUBLIC_START_DATE格式: "2026-01-16 00:00:00"
                    public_start_date = bond.get('PUBLIC_START_DATE', '')
                    if public_start_date:
                        # 提取日期部分
                        apply_date = public_start_date.split(' ')[0]
                        if apply_date == self.today:
                            today_bonds.append(bond)
                
                return today_bonds
            
            return []
            
        except Exception as e:
            print(f"获取数据失败: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def fetch_bond_data_alternative(self) -> List[Dict]:
        """备用数据源：集思录"""
        try:
            url = "https://www.jisilu.cn/data/cbnew/cb_list/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://www.jisilu.cn/"
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # 这里简化处理，实际使用时需要解析HTML或找到API接口
            # 由于集思录可能有反爬机制，建议使用东方财富为主
            return []
            
        except Exception as e:
            print(f"备用数据源获取失败: {e}")
            return []
    
    def format_bond_message(self, bonds: List[Dict]) -> str:
        """格式化债券信息为消息内容"""
        if not bonds:
            return f"📊 {self.today} 今日无可转债申购"
        
        message = f"🎉 {self.today} 今日有 {len(bonds)} 只可转债可申购！\n\n"
        
        for i, bond in enumerate(bonds, 1):
            bond_code = bond.get('SECURITY_CODE', 'N/A')
            bond_name = bond.get('SECURITY_NAME_ABBR', 'N/A')
            apply_code = bond.get('CORRECODE', 'N/A')
            apply_date = bond.get('PUBLIC_START_DATE', 'N/A')
            
            message += f"{i}. {bond_name} ({bond_code})\n"
            if apply_code and apply_code != 'N/A':
                message += f"   申购代码: {apply_code}\n"
            if apply_date and apply_date != 'N/A':
                # 只显示日期部分
                date_only = apply_date.split(' ')[0] if ' ' in apply_date else apply_date
                message += f"   申购日期: {date_only}\n"
        
        message += "\n记得今日申购哦！💰"
        return message
    
    def send_email(self, message: str) -> bool:
        """发送邮件通知"""
        try:
            smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
            smtp_port = int(os.getenv('SMTP_PORT', '587'))
            sender_email = os.getenv('SENDER_EMAIL')
            sender_password = os.getenv('SENDER_PASSWORD')
            receiver_email = os.getenv('RECEIVER_EMAIL')
            
            if not all([sender_email, sender_password, receiver_email]):
                print("邮件配置不完整，跳过邮件发送")
                return False
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = f"可转债申购提醒 - {self.today}"
            
            msg.attach(MIMEText(message, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            
            print("邮件发送成功！")
            return True
            
        except Exception as e:
            print(f"邮件发送失败: {e}")
            return False
    
    def send_dingtalk(self, message: str) -> bool:
        """发送钉钉通知"""
        try:
            webhook_url = os.getenv('DINGTALK_WEBHOOK')
            if not webhook_url:
                print("钉钉配置不完整，跳过钉钉发送")
                return False
            
            data = {
                "msgtype": "text",
                "text": {
                    "content": message
                }
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            response.raise_for_status()
            
            print("钉钉通知发送成功！")
            return True
            
        except Exception as e:
            print(f"钉钉发送失败: {e}")
            return False
    
    def send_wechat_work(self, message: str) -> bool:
        """发送企业微信通知"""
        try:
            webhook_url = os.getenv('WECHAT_WORK_WEBHOOK')
            if not webhook_url:
                print("企业微信配置不完整，跳过企业微信发送")
                return False
            
            data = {
                "msgtype": "text",
                "text": {
                    "content": message
                }
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            response.raise_for_status()
            
            print("企业微信通知发送成功！")
            return True
            
        except Exception as e:
            print(f"企业微信发送失败: {e}")
            return False
    
    def send_server_chan(self, message: str) -> bool:
        """发送Server酱通知"""
        try:
            send_key = os.getenv('SERVERCHAN_SENDKEY')
            if not send_key:
                print("Server酱配置不完整，跳过发送")
                return False
            
            url = f"https://sctapi.ftqq.com/{send_key}.send"
            data = {
                "title": f"可转债申购提醒 - {self.today}",
                "desp": message
            }
            
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            
            print("Server酱通知发送成功！")
            return True
            
        except Exception as e:
            print(f"Server酱发送失败: {e}")
            return False
    
    def send_notifications(self, message: str):
        """发送所有配置的通知"""
        print("\n" + "="*50)
        print("开始发送通知...")
        print("="*50)
        
        # 发送各种通知
        self.send_email(message)
        self.send_dingtalk(message)
        self.send_wechat_work(message)
        self.send_server_chan(message)
        
        print("\n所有通知发送完成！")
    
    def run(self, skip_weekend_notification: bool = True):
        """
        主运行函数
        
        Args:
            skip_weekend_notification: 如果是周末且没有数据，是否跳过通知
        """
        print("="*50)
        print("可转债申购提醒系统")
        print("="*50)
        
        # 如果是周末，可以选择跳过
        if not self.is_weekday:
            print("\n今天是周末，通常不会有新债申购")
            print("继续检查以防万一...")
        
        # 获取债券数据
        bonds = self.fetch_bond_data()
        
        # 格式化消息
        message = self.format_bond_message(bonds)
        print("\n" + message)
        
        # 保存结果到文件
        result = {
            "date": self.today,
            "bonds": bonds,
            "message": message,
            "count": len(bonds),
            "is_weekday": self.is_weekday
        }
        
        with open('bond_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        # 决定是否发送通知
        should_notify = True
        
        # 如果是周末且没有数据，可以选择跳过通知
        if skip_weekend_notification and not self.is_weekday and len(bonds) == 0:
            print("\n今天是周末且无可转债申购，跳过通知")
            should_notify = False
        
        # 如果有数据，总是发送通知
        if len(bonds) > 0:
            should_notify = True
        
        # 发送通知
        if should_notify:
            self.send_notifications(message)
        else:
            print("\n跳过通知发送")
        
        print(f"\n扫描完成！共找到 {len(bonds)} 只可转债")
        return len(bonds)


def main():
    """主函数"""
    try:
        notifier = BondNotifier()
        count = notifier.run()
        sys.exit(0 if count >= 0 else 1)
    except Exception as e:
        print(f"程序运行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
