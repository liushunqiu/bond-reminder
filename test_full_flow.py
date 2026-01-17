#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试完整流程 - 使用2026-01-08的实际数据
"""

import os
import sys
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_new_bonds import BondNotifier


class TestFullFlow(BondNotifier):
    def __init__(self, test_date):
        """测试指定日期的完整流程"""
        self.today = test_date
        print(f"="*70)
        print(f"测试完整流程 - {self.today}")
        print(f"="*70)
    
    def test_full_flow(self):
        """测试完整流程"""
        print("\n[1] 获取债券数据...")
        bonds = self.fetch_bond_data()
        print(f"✓ 获取到 {len(bonds)} 只可转债")
        
        print("\n[2] 格式化消息...")
        message = self.format_bond_message(bonds)
        print("生成的消息:")
        print("-" * 70)
        print(message)
        print("-" * 70)
        
        print("\n[3] 保存结果到文件...")
        result = {
            "date": self.today,
            "bonds": bonds,
            "message": message,
            "count": len(bonds)
        }
        
        filename = f'bond_result_{self.today}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"✓ 结果已保存到 {filename}")
        
        print("\n[4] 发送通知（跳过实际发送）...")
        self.send_notifications(message)
        
        print("\n" + "="*70)
        print("✓ 完整流程测试完成")
        print("="*70)
        
        return len(bonds)


if __name__ == "__main__":
    import json
    
    try:
        # 测试2026-01-08（有数据）
        test_date = "2026-01-08"
        notifier = TestFullFlow(test_date)
        count = notifier.test_full_flow()
        
        print(f"\n结果: {test_date} 有 {count} 只可转债申购")
        
        if count > 0:
            print("\n✓ 系统运行正常！可以正确获取并通知可转债申购信息")
        else:
            print("\n⚠️  该日期无可转债申购")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
