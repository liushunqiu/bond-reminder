#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用你提供的完整参数测试
"""

import requests
import json

def test_full_params():
    """使用你提供的完整参数测试"""
    print("=" * 80)
    print("使用你提供的完整参数测试")
    print("=" * 80)
    
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    
    # 使用你提供的参数
    params = {
        "reportName": "RPT_BOND_CB_LIST",
        "columns": "ALL",
        "pageSize": 50,
        "pageNumber": 1,
        "sortColumns": "PUBLIC_START_DATE,SECURITY_CODE",
        "sortTypes": "-1,-1",
        "source": "WEB",
        "client": "WEB"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print(f"\n请求URL: {url}")
    print(f"参数: {json.dumps(params, ensure_ascii=False, indent=2)}")
    
    response = requests.get(url, params=params, headers=headers, timeout=30)
    print(f"\n响应状态码: {response.status_code}")
    
    data = response.json()
    bonds = data.get('result', {}).get('data', [])
    
    print(f"\n返回数据条数: {len(bonds)}")
    
    # 查找2026-01-16的数据
    print("\n" + "=" * 80)
    print("2026-01-16 的可转债:")
    print("=" * 80)
    
    target_bonds = []
    for bond in bonds:
        public_date = bond.get('PUBLIC_START_DATE', '')
        if public_date.startswith('2026-01-16'):
            target_bonds.append(bond)
            print(f"\n{bond.get('SECURITY_NAME_ABBR', '')} ({bond.get('SECURITY_CODE', '')})")
            print(f"  申购日期: {public_date}")
            print(f"  申购代码: {bond.get('CORRECODE', '')}")
            print(f"  所有字段: {json.dumps(bond, ensure_ascii=False, indent=4)}")
    
    if not target_bonds:
        print("未找到2026-01-16的记录")
    
    print(f"\n共找到 {len(target_bonds)} 条记录")
    
    # 显示2026年1月所有数据
    print("\n" + "=" * 80)
    print("2026年1月所有可转债:")
    print("=" * 80)
    
    january_bonds = []
    for bond in bonds:
        public_date = bond.get('PUBLIC_START_DATE', '')
        if public_date.startswith('2026-01'):
            january_bonds.append(bond)
            print(f"{public_date} - {bond.get('SECURITY_NAME_ABBR', '')} ({bond.get('SECURITY_CODE', '')})")
    
    print(f"\n共找到 {len(january_bonds)} 条2026年1月的记录")
    
    return target_bonds

if __name__ == "__main__":
    try:
        test_full_params()
        print("\n✓ 测试完成")
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()