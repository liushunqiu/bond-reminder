#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试工作日判断功能
"""

import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_new_bonds import BondNotifier, is_weekday


def test_weekday_judgment():
    """测试工作日判断功能"""
    print("=" * 80)
    print("测试工作日判断功能")
    print("=" * 80)
    
    # 测试一周的每一天
    today = datetime.now()
    weekday = today.weekday()  # 0=周一, 6=周日
    
    print(f"\n今天是: {today.strftime('%Y-%m-%d')}")
    print(f"今天是: {'工作日' if is_weekday() else '周末'}")
    
    # 测试接下来的7天
    print("\n接下来7天的日期类型:")
    print("-" * 80)
    
    for i in range(7):
        test_date = today + timedelta(days=i)
        date_str = test_date.strftime('%Y-%m-%d')
        is_workday = is_weekday(date_str)
        weekday_name = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][test_date.weekday()]
        status = '✓ 工作日' if is_workday else '✗ 周末'
        
        print(f"{date_str} ({weekday_name}): {status}")


def test_notifier_with_dates():
    """测试不同日期的通知器"""
    print("\n" + "=" * 80)
    print("测试不同日期的通知器")
    print("=" * 80)
    
    # 测试工作日（2026-01-16是周四）
    print("\n[测试1] 工作日 2026-01-16（周四）:")
    notifier1 = BondNotifier("2026-01-16")
    bonds1 = notifier1.fetch_bond_data()
    message1 = notifier1.format_bond_message(bonds1)
    print(f"找到 {len(bonds1)} 只可转债")
    print(f"消息: {message1[:50]}...")
    
    # 测试周末（2026-01-18是周六）
    print("\n[测试2] 周末 2026-01-18（周六）:")
    notifier2 = BondNotifier("2026-01-18")
    bonds2 = notifier2.fetch_bond_data()
    message2 = notifier2.format_bond_message(bonds2)
    print(f"找到 {len(bonds2)} 只可转债")
    print(f"消息: {message2[:50]}...")


def test_skip_weekend_notification():
    """测试周末跳过通知功能"""
    print("\n" + "=" * 80)
    print("测试周末跳过通知功能")
    print("=" * 80)
    
    # 测试周末无数据的情况
    print("\n[测试] 周末 2026-01-18（周六）:")
    notifier = BondNotifier("2026-01-18")
    
    # 获取数据
    bonds = notifier.fetch_bond_data()
    
    print(f"找到 {len(bonds)} 只可转债")
    print(f"是否工作日: {notifier.is_weekday}")
    
    # 测试运行（会自动跳过周末无数据的通知）
    print("\n运行测试（skip_weekend_notification=True）:")
    count = notifier.run(skip_weekend_notification=True)
    
    print(f"\n结果: 找到 {count} 只可转债")
    if not notifier.is_weekday and count == 0:
        print("✓ 周末无数据，正确跳过通知")
    else:
        print("✓ 正常处理")


if __name__ == "__main__":
    try:
        test_weekday_judgment()
        test_notifier_with_dates()
        test_skip_weekend_notification()
        
        print("\n" + "=" * 80)
        print("✓ 所有测试完成")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()