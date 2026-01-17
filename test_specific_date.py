#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试特定日期的可转债数据获取
用于验证2026-01-16的数据是否正确
"""

import json
import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from check_new_bonds import BondNotifier


class TestBondNotifier(BondNotifier):
    def __init__(self, test_date: str):
        """重写初始化，使用测试日期"""
        self.today = test_date
        print(f"测试扫描 {self.today} 的可转债申购信息...")
        
    def fetch_bond_data_debug(self) -> List[Dict]:
        """调试版数据获取，显示详细请求信息"""
        try:
            import requests
            
            # 东方财富可转债列表API
            url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
            params = {
                "reportName": "RPT_BOND_CB_LIST",
                "columns": "SECURITY_CODE,SECURITY_NAME_ABBR,PUBLIC_START_DATE,CORRECODE",
                "pageSize": "500",
                "pageNumber": "1",
                "source": "WEB",
                "client": "WEB"
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            print(f"\n请求URL: {url}")
            print(f"请求参数: {json.dumps(params, ensure_ascii=False, indent=2)}")
            
            response = requests.get(url, params=params, headers=headers, timeout=30)
            print(f"响应状态码: {response.status_code}")
            
            response.raise_for_status()
            
            data = response.json()
            print(f"\n响应数据结构:")
            print(json.dumps(data, ensure_ascii=False, indent=2)[:2000] + "...")
            
            if data.get("result") and data["result"].get("data"):
                all_bonds = data["result"]["data"]
                
                # 筛选申购日期为今天的债券
                today_bonds = []
                for bond in all_bonds:
                    public_start_date = bond.get('PUBLIC_START_DATE', '')
                    if public_start_date:
                        apply_date = public_start_date.split(' ')[0]
                        if apply_date == self.today:
                            today_bonds.append(bond)
                
                print(f"\n✓ 成功获取到 {len(today_bonds)} 条数据")
                return today_bonds
            else:
                print(f"\n✗ 未找到数据，响应结构: {list(data.keys())}")
                if "result" in data:
                    print(f"result结构: {list(data['result'].keys()) if data.get('result') else 'None'}")
                return []
                
        except Exception as e:
            print(f"获取数据失败: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def test_data_fetch(self):
        """测试数据获取"""
        print("="*70)
        print(f"测试日期: {self.today}")
        print("="*70)
        
        # 获取数据
        bonds = self.fetch_bond_data_debug()
        
        if not bonds:
            print(f"\n⚠️  {self.today} 没有找到可转债申购数据")
            
            # 尝试获取最近几天的数据作为对比
            print("\n尝试获取最近几天的数据进行对比...")
            for i in range(1, 6):
                check_date = datetime.strptime(self.today, '%Y-%m-%d') - timedelta(days=i)
                check_date_str = check_date.strftime('%Y-%m-%d')
                print(f"  检查 {check_date_str}...")
                
                # 临时修改日期
                original_today = self.today
                self.today = check_date_str
                test_bonds = self.fetch_bond_data_debug()
                self.today = original_today
                
                if test_bonds:
                    print(f"    ✓ 找到 {len(test_bonds)} 只可转债")
                    break
            return []
        
        print(f"\n🎉 找到 {len(bonds)} 只可转债可申购！")
        print("\n详细列表:")
        print("-" * 70)
        
        for i, bond in enumerate(bonds, 1):
            print(f"\n{i}. 债券代码: {bond.get('SECURITY_CODE', 'N/A')}")
            print(f"   债券名称: {bond.get('SECURITY_NAME_ABBR', 'N/A')}")
            print(f"   申购代码: {bond.get('CORRECODE', 'N/A')}")
            print(f"   申购日期: {bond.get('PUBLIC_START_DATE', 'N/A')}")
            print(f"   原始数据: {json.dumps(bond, ensure_ascii=False, indent=2)}")
        
        return bonds


def test_2026_01_16():
    """测试2026年1月8日的数据（数据库中有实际数据）"""
    print("\n" + "="*70)
    print("开始测试 2026-01-08 的可转债数据（数据库中有实际数据）")
    print("="*70)
    
    # 创建测试实例
    test_date = "2026-01-08"
    notifier = TestBondNotifier(test_date)
    
    # 测试数据获取
    bonds = notifier.test_data_fetch()
    
    # 生成消息
    message = notifier.format_bond_message(bonds)
    print("\n" + "="*70)
    print("生成的通知消息:")
    print("="*70)
    print(message)
    
    # 保存测试结果
    result = {
        "test_date": test_date,
        "bonds": bonds,
        "message": message,
        "count": len(bonds),
        "test_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('test_result_2026-01-16.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 测试结果已保存到 test_result_2026-01-16.json")
    
    return len(bonds)


def test_date_range():
    """测试一个日期范围，看看哪些天有新股"""
    print("\n" + "="*70)
    print("测试2026年1月的可转债申购情况")
    print("="*70)
    
    from datetime import datetime, timedelta
    
    # 测试2026年1月1日到1月31日
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 1, 31)
    
    results = []
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        print(f"\n检查 {date_str}...")
        
        notifier = TestBondNotifier(date_str)
        bonds = notifier.fetch_bond_data()
        
        if bonds:
            print(f"  ✓ 找到 {len(bonds)} 只可转债")
            results.append({
                "date": date_str,
                "count": len(bonds),
                "bonds": bonds
            })
        else:
            print(f"  - 无数据")
        
        current_date += timedelta(days=1)
    
    print("\n" + "="*70)
    print("2026年1月可转债申购汇总:")
    print("="*70)
    
    if results:
        for result in results:
            print(f"\n{result['date']}: {result['count']} 只可转债")
            for bond in result['bonds']:
                print(f"  - {bond.get('SECURITY_NAME_ABR', 'N/A')} ({bond.get('SECURITY_CODE', 'N/A')})")
    else:
        print("\n2026年1月没有找到可转债申购数据")
    
    # 保存汇总结果
    with open('january_2026_summary.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return results


if __name__ == "__main__":
    try:
        # 测试指定日期
        count = test_2026_01_16()
        
        # 如果指定日期没有数据，测试整个月
        if count == 0:
            print("\n" + "="*70)
            print("2026-01-16无数据，测试整个1月...")
            print("="*70)
            test_date_range()
        
        print("\n✓ 测试完成！")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
