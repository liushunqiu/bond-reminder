#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增加查询数量，看看是否能获取更多数据
"""

import requests
import json

def check_larger_dataset():
    """查询更多数据"""
    print("=" * 80)
    print("查询1000条数据，查看是否有2026-01-16的记录")
    print("=" * 80)
    
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_BOND_CB_LIST",
        "columns": "SECURITY_CODE,SECURITY_NAME_ABBR,PUBLIC_START_DATE,CORRECODE",
        "pageSize": 1000,
        "pageNumber": 1,
        "source": "WEB",
        "client": "WEB"
    }
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    bonds = data.get('result', {}).get('data', [])
    
    print(f"返回数据条数: {len(bonds)}\n")
    
    # 查找2026-01-16的数据
    target_bonds = []
    for bond in bonds:
        public_date = bond.get('PUBLIC_START_DATE', '')
        if public_date.startswith('2026-01-16'):
            target_bonds.append(bond)
    
    if target_bonds:
        print(f"✓ 找到 {len(target_bonds)} 条2026-01-16的记录:\n")
        for i, bond in enumerate(target_bonds, 1):
            print(f"{i}. {bond['SECURITY_NAME_ABBR']} ({bond['SECURITY_CODE']})")
            print(f"   申购代码: {bond['CORRECODE']}")
            print(f"   申购日期: {bond['PUBLIC_START_DATE']}")
    else:
        print("✗ 未找到2026-01-16的记录\n")
        
        # 显示2026年1月的所有记录
        january_bonds = []
        for bond in bonds:
            public_date = bond.get('PUBLIC_START_DATE', '')
            if public_date.startswith('2026-01'):
                january_bonds.append(bond)
        
        print(f"2026年1月共有 {len(january_bonds)} 只可转债:\n")
        for bond in january_bonds:
            print(f"- {bond['PUBLIC_START_DATE']} - {bond['SECURITY_NAME_ABBR']} ({bond['SECURITY_CODE']})")
    
    return target_bonds

def check_multiple_pages():
    """检查多页数据"""
    print("\n" + "=" * 80)
    print("检查多页数据（查看是否有遗漏）")
    print("=" * 80)
    
    all_january_bonds = []
    
    for page in range(1, 4):  # 检查前3页
        print(f"\n查询第 {page} 页...")
        
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        params = {
            "reportName": "RPT_BOND_CB_LIST",
            "columns": "SECURITY_CODE,SECURITY_NAME_ABBR,PUBLIC_START_DATE,CORRECODE",
            "pageSize": 500,
            "pageNumber": page,
            "source": "WEB",
            "client": "WEB"
        }
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        bonds = data.get('result', {}).get('data', [])
        
        print(f"  返回数据条数: {len(bonds)}")
        
        # 查找2026年1月的数据
        january_bonds = []
        for bond in bonds:
            public_date = bond.get('PUBLIC_START_DATE', '')
            if public_date.startswith('2026-01'):
                january_bonds.append(bond)
        
        print(f"  2026年1月数据: {len(january_bonds)} 条")
        all_january_bonds.extend(january_bonds)
    
    print(f"\n总计找到 {len(all_january_bonds)} 条2026年1月记录")
    
    # 去重
    unique_bonds = {}
    for bond in all_january_bonds:
        code = bond['SECURITY_CODE']
        if code not in unique_bonds:
            unique_bonds[code] = bond
    
    print(f"去重后: {len(unique_bonds)} 条记录")
    
    if len(unique_bonds) > 1:
        print("\n所有2026年1月记录:")
        for bond in unique_bonds.values():
            print(f"- {bond['PUBLIC_START_DATE']} - {bond['SECURITY_NAME_ABBR']} ({bond['SECURITY_CODE']})")
    
    return all_january_bonds

if __name__ == "__main__":
    try:
        check_larger_dataset()
        check_multiple_pages()
        print("\n✓ 查询完成")
    except Exception as e:
        print(f"\n✗ 查询失败: {e}")
        import traceback
        traceback.print_exc()