#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试今天的可转债数据（不固定日期）
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_new_bonds import BondNotifier

def test_today():
    """测试今天的可转债数据"""
    print("=" * 80)
    print("测试今天的可转债数据")
    print("=" * 80)
    
    # 不传入日期参数，自动使用今天
    notifier = BondNotifier()
    
    print(f"\n当前日期: {notifier.today}")
    print(f"是否工作日: {notifier.is_weekday}")
    
    # 获取数据
    bonds = notifier.fetch_bond_data()
    
    print(f"\n找到 {len(bonds)} 只可转债:\n")
    
    for i, bond in enumerate(bonds, 1):
        print(f"{i}. {bond.get('SECURITY_NAME_ABBR', '')} ({bond.get('SECURITY_CODE', '')})")
        print(f"   申购代码: {bond.get('CORRECODE', '')}")
        print(f"   申购日期: {bond.get('PUBLIC_START_DATE', '')}")
        print()
    
    # 生成消息
    message = notifier.format_bond_message(bonds)
    print("\n生成的通知消息:")
    print("-" * 80)
    print(message)
    print("-" * 80)
    
    # 运行完整流程（会自动判断是否发送通知）
    print("\n运行完整流程:")
    count = notifier.run()
    
    return count

if __name__ == "__main__":
    try:
        count = test_today()
        print(f"\n✓ 测试完成，找到 {count} 只可转债")
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()