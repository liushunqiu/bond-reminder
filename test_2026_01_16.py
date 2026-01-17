#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
专门测试2026-01-16的数据
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_new_bonds import BondNotifier

def test_2026_01_16():
    """测试2026-01-16"""
    print("=" * 80)
    print("测试 2026-01-16 的可转债数据")
    print("=" * 80)
    
    # 临时修改today
    notifier = BondNotifier()
    notifier.today = "2026-01-16"
    
    print(f"测试日期: {notifier.today}")
    
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
    
    return len(bonds)

if __name__ == "__main__":
    try:
        count = test_2026_01_16()
        print(f"\n✓ 测试完成，找到 {count} 只可转债")
        if count == 2:
            print("✓ 正确！找到了你说的2只可转债！")
        else:
            print(f"⚠️  预期2只，实际找到{count}只")
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()