#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Server酱通知
"""

import os
import sys
from datetime import datetime

# 加载.env文件
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_new_bonds import BondNotifier


def test_serverchan():
    """测试Server酱通知"""
    print("=" * 80)
    print("测试Server酱通知")
    print("=" * 80)
    
    # 检查配置
    send_key = os.getenv('SERVERCHAN_SENDKEY')
    print(f"\nServer酱SendKey: {send_key[:20]}...{send_key[-10:] if send_key else 'None'}")
    
    if not send_key:
        print("✗ 未配置SERVERCHAN_SENDKEY")
        return False
    
    # 创建通知器
    notifier = BondNotifier("2026-01-16")
    
    # 获取数据
    bonds = notifier.fetch_bond_data()
    
    # 格式化消息
    message = notifier.format_bond_message(bonds)
    
    print(f"\n找到 {len(bonds)} 只可转债")
    print(f"\n消息内容:")
    print("-" * 80)
    print(message)
    print("-" * 80)
    
    # 发送通知
    print("\n发送Server酱通知...")
    success = notifier.send_server_chan(message)
    
    if success:
        print("\n✓ Server酱通知发送成功！")
        print("请检查你的手机是否收到通知")
    else:
        print("\n✗ Server酱通知发送失败")
    
    return success


if __name__ == "__main__":
    try:
        # 检查是否安装了python-dotenv
        try:
            from dotenv import load_dotenv
        except ImportError:
            print("未安装python-dotenv，正在安装...")
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", "python-dotenv"])
            from dotenv import load_dotenv
        
        success = test_serverchan()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)