#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查所有字段，看看是否有其他日期信息
"""

import requests
import json

def check_all_fields():
    """检查所有字段，看看是否有其他日期信息"""
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_BOND_CB_LIST",
        "columns": "ALL",
        "pageSize": 50,  # 先查50条看看
        "pageNumber": 1,
        "source": "WEB",
        "client": "WEB"
    }
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    bonds = data.get('result', {}).get('data', [])
    
    if bonds:
        print("所有字段列表:")
        print("=" * 80)
        for i, field in enumerate(sorted(bonds[0].keys()), 1):
            print(f"{i:3d}. {field}")
        
        print("\n" + "=" * 80)
        print("\n包含日期的字段:")
        print("=" * 80)
        
        date_fields = []
        for field in bonds[0].keys():
            if 'DATE' in field.upper():
                date_fields.append(field)
        
        for i, field in enumerate(sorted(date_fields), 1):
            print(f"{i:3d}. {field}")
        
        print("\n" + "=" * 80)
        print("\n查看几个债券的所有日期字段:")
        print("=" * 80)
        
        for i, bond in enumerate(bonds[:3], 1):
            print(f"\n债券 {i}: {bond.get('SECURITY_NAME_ABBR', 'N/A')}")
            for field in sorted(date_fields):
                value = bond.get(field, '')
                if value:
                    print(f"  {field}: {value}")
    
    return bonds

def check_new_bond_api():
    """尝试新股申购的API"""
    print("\n" + "=" * 80)
    print("尝试新股申购API（可能包含可转债）")
    print("=" * 80)
    
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_NETHIS_BOND",
        "columns": "ALL",
        "pageSize": 50,
        "pageNumber": 1,
        "source": "WEB",
        "client": "WEB"
    }
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"响应状态: {data.get('success', 'N/A')}")
        print(f"消息: {data.get('message', 'N/A')}")
        
        if data.get('result') and data['result'].get('data'):
            bonds = data['result']['data']
            print(f"\n找到 {len(bonds)} 条记录")
            for i, bond in enumerate(bonds[:5], 1):
                print(f"\n{i}. {bond}")
        else:
            print("无数据")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == "__main__":
    try:
        check_all_fields()
        check_new_bond_api()
        print("\n✓ 查询完成")
    except Exception as e:
        print(f"\n✗ 查询失败: {e}")
        import traceback
        traceback.print_exc()