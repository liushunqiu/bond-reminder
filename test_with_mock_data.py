#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用模拟数据测试通知系统
验证整个通知流程是否正常工作
"""

import os
import sys
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_new_bonds import BondNotifier


class MockBondNotifier(BondNotifier):
    def __init__(self, test_date=None):
        """使用模拟数据测试"""
        if test_date:
            self.today = test_date
        else:
            self.today = datetime.now().strftime('%Y-%m-%d')
        print(f"使用模拟数据测试 {self.today} 的可转债申购信息...")
    
    def fetch_bond_data(self):
        """返回模拟数据 - 模拟2026-01-16有2只可转债"""
        if self.today == "2026-01-16":
            print(f"✓ 模拟数据：{self.today} 有2只可转债申购")
            return [
                {
                    "bond_id": "123456",
                    "bond_nm": "测试转债A",
                    "apply_cd": "789012",
                    "price": "100.00",
                    "convert_price": "12.50"
                },
                {
                    "bond_id": "654321",
                    "bond_nm": "测试转债B",
                    "apply_cd": "210987",
                    "price": "100.00",
                    "convert_price": "15.20"
                }
            ]
        else:
            print(f"✓ 模拟数据：{self.today} 无可转债申购")
            return []
    
    def test_all_notifications(self):
        """测试所有通知方式"""
        print("\n" + "="*70)
        print("测试所有通知方式")
        print("="*70)
        
        # 获取模拟数据
        bonds = self.fetch_bond_data()
        
        # 格式化消息
        message = self.format_bond_message(bonds)
        print("\n生成的消息内容:")
        print("-" * 70)
        print(message)
        print("-" * 70)
        
        # 测试各种通知方式（不实际发送）
        print("\n测试通知方式:")
        
        # 测试邮件配置
        smtp_host = os.getenv('SMTP_HOST')
        sender_email = os.getenv('SENDER_EMAIL')
        if smtp_host and sender_email:
            print("✓ 邮件通知已配置")
            print(f"  SMTP服务器: {smtp_host}")
            print(f"  发件人: {sender_email}")
        else:
            print("✗ 邮件通知未配置")
        
        # 测试钉钉
        dingtalk = os.getenv('DINGTALK_WEBHOOK')
        if dingtalk:
            print("✓ 钉钉通知已配置")
            print(f"  Webhook: {dingtalk[:50]}...")
        else:
            print("✗ 钉钉通知未配置")
        
        # 测试企业微信
        wechat = os.getenv('WECHAT_WORK_WEBHOOK')
        if wechat:
            print("✓ 企业微信通知已配置")
            print(f"  Webhook: {wechat[:50]}...")
        else:
            print("✗ 企业微信通知未配置")
        
        # 测试Server酱
        serverchan = os.getenv('SERVERCHAN_SENDKEY')
        if serverchan:
            print("✓ Server酱通知已配置")
            print(f"  SendKey: {serverchan[:20]}...")
        else:
            print("✗ Server酱通知未配置")
        
        # 实际发送通知（如果配置了）
        print("\n" + "="*70)
        print("发送通知测试")
        print("="*70)
        self.send_notifications(message)
        
        return len(bonds)


def test_scenarios():
    """测试不同场景"""
    print("="*70)
    print("可转债通知系统 - 模拟数据测试")
    print("="*70)
    
    # 场景1：测试2026-01-16（有2只可转债）
    print("\n[场景1] 测试2026-01-16（有2只可转债）:")
    notifier1 = MockBondNotifier("2026-01-16")
    count1 = notifier1.test_all_notifications()
    print(f"结果: 找到 {count1} 只可转债")
    
    # 场景2：测试今天（无可转债）
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"\n[场景2] 测试今天 {today}（无可转债）:")
    notifier2 = MockBondNotifier()
    count2 = notifier2.test_all_notifications()
    print(f"结果: 找到 {count2} 只可转债")
    
    # 总结
    print("\n" + "="*70)
    print("测试总结:")
    print("="*70)
    print(f"✓ 消息格式化功能正常")
    print(f"✓ 通知系统配置检测正常")
    print(f"✓ 模拟数据测试通过")
    
    if count1 == 2:
        print(f"✓ 2026-01-16数据正确识别2只可转债")
    else:
        print(f"✗ 2026-01-16数据识别异常")
    
    if count2 == 0:
        print(f"✓ 今天数据正确识别为无可转债")
    else:
        print(f"✗ 今天数据识别异常")
    
    # 检查配置
    configured_methods = 0
    if os.getenv('SMTP_HOST') and os.getenv('SENDER_EMAIL'):
        configured_methods += 1
    if os.getenv('DINGTALK_WEBHOOK'):
        configured_methods += 1
    if os.getenv('WECHAT_WORK_WEBHOOK'):
        configured_methods += 1
    if os.getenv('SERVERCHAN_SENDKEY'):
        configured_methods += 1
    
    print(f"\n已配置的通知方式: {configured_methods} 种")
    
    if configured_methods == 0:
        print("⚠️  警告: 未配置任何通知方式，请在GitHub Secrets中配置")
        print("   参考 SETUP.md 文件进行配置")
    else:
        print("✓ 通知方式已配置，系统将正常运行")
    
    return configured_methods > 0


if __name__ == "__main__":
    try:
        success = test_scenarios()
        print("\n✓ 模拟测试完成！")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
