#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 用于验证配置是否正确
"""

import os
import sys
from datetime import datetime, timedelta

def test_environment():
    """测试环境配置"""
    print("=" * 60)
    print("可转债提醒系统 - 配置测试")
    print("=" * 60)
    
    # 测试基本环境
    print("\n[1] Python环境信息:")
    print(f"   Python版本: {sys.version}")
    print(f"   当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 测试环境变量
    print("\n[2] 环境变量配置:")
    
    # 邮件配置
    email_vars = ['SMTP_HOST', 'SMTP_PORT', 'SENDER_EMAIL', 'SENDER_PASSWORD', 'RECEIVER_EMAIL']
    email_configured = sum(1 for var in email_vars if os.getenv(var))
    print(f"   邮件配置: {email_configured}/{len(email_vars)} 项已配置")
    for var in email_vars:
        value = os.getenv(var)
        print(f"     {var}: {'已配置' if value else '未配置'}")
    
    # 其他通知方式
    dingtalk = os.getenv('DINGTALK_WEBHOOK')
    wechat = os.getenv('WECHAT_WORK_WEBHOOK')
    serverchan = os.getenv('SERVERCHAN_SENDKEY')
    
    print(f"   钉钉配置: {'已配置' if dingtalk else '未配置'}")
    print(f"   企业微信: {'已配置' if wechat else '未配置'}")
    print(f"   Server酱: {'已配置' if serverchan else '未配置'}")
    
    # 测试网络连接
    print("\n[3] 网络连接测试:")
    try:
        import requests
        
        # 测试访问东方财富
        print("   测试访问东方财富网...")
        response = requests.get('https://www.eastmoney.com', timeout=10)
        print(f"   东方财富网: {'✓ 可访问' if response.status_code == 200 else '✗ 无法访问'}")
        
        # 测试访问GitHub
        print("   测试访问GitHub...")
        response = requests.get('https://api.github.com', timeout=10)
        print(f"   GitHub API: {'✓ 可访问' if response.status_code == 200 else '✗ 无法访问'}")
        
    except Exception as e:
        print(f"   网络测试失败: {e}")
    
    # 测试导入主脚本
    print("\n[4] 主脚本测试:")
    try:
        # 临时导入主脚本
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # 测试是否能导入
        print("   导入主脚本...")
        from check_new_bonds import BondNotifier
        print("   ✓ 主脚本导入成功")
        
        # 测试实例化
        print("   创建扫描器实例...")
        notifier = BondNotifier()
        print("   ✓ 扫描器创建成功")
        
        # 测试数据获取（不实际发送通知）
        print("   测试数据获取...")
        bonds = notifier.fetch_bond_data()
        print(f"   ✓ 数据获取完成，今日{'有' if bonds else '暂无'}可转债申购")
        
        if bonds:
            print(f"   找到 {len(bonds)} 只可转债:")
            for bond in bonds[:3]:  # 只显示前3个
                name = bond.get('SECURITY_NAME_ABBR', 'N/A')
                code = bond.get('SECURITY_CODE', 'N/A')
                print(f"     - {name} ({code})")
        
    except Exception as e:
        print(f"   ✗ 主脚本测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)
    
    # 总结
    print("\n配置总结:")
    total_methods = sum([
        email_configured == len(email_vars),
        bool(dingtalk),
        bool(wechat),
        bool(serverchan)
    ])
    print(f"已配置的通知方式: {total_methods} 种")
    
    if total_methods == 0:
        print("⚠️ 警告: 未配置任何通知方式，请设置至少一种通知方式！")
    else:
        print("✓ 可以正常接收通知")
    
    return total_methods > 0

if __name__ == "__main__":
    success = test_environment()
    sys.exit(0 if success else 1)
