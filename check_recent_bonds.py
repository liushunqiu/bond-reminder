#!/usr/bin/env python3
# -*- coding: utf- -*-
"""
查看数据库中最近的申购记录
"""

import requests
import json
from datetime import datetime

def check_recent_bonds():
    """查看最近的申购记录"""
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_BOND_CB_LIST",
        "columns": "SECURITY_CODE,SECURITY_NAME_ABBR,PUBLIC_START_DATE,CORRECODE",
        "pageSize": 500,
        "pageNumber": 1,
        "source": "WEB",
        "client": "WEB"
    }
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    
    data = response.json()
    bonds = data.get('result', {}).get('data', [])
    
    print(f"总条数: {len(bonds)}")
    
    # 筛选有申购日期的记录
    bonds_with_date = [b for b in bonds if b.get('PUBLIC_START_DATE')]
    
    # 按日期排序（最新的在前）
    sorted_bonds = sorted(
        bonds_with_date, 
        key=lambda x: x.get('PUBLIC_START_DATE', ''), 
        reverse=True
    )
    
    print('\n最近的10条申购记录:')
    print('-' * 70)
    for bond in sorted_bonds[:10]:
        date = bond.get('PUBLIC_START_DATE', '')
        name = bond.get('SECURITY_NAME_ABBR', '')
        code = bond.get('SECURITY_CODE', '')
        apply_code = bond.get('CORRECODE', '')
        print(f"{date} - {name} ({code}) - 申购代码: {apply_code}")
    
    # 检查2026年1月的数据
    print('\n2026年1月的申购记录:')
    print('-' * 70)
    january_bonds = [b for b in sorted_bonds if b.get('PUBLIC_START_DATE', '').startswith('2026-01')]
    if january_bonds:
        for bond in january_bonds:
            date = bond.get('PUBLIC_START_DATE', '')
            name = bond.get('SECURITY_NAME_ABBR', '')
            code = bond.get('SECURITY_CODE', '')
            apply_code = bond.get('CORRECODE', '')
            print(f"{date} - {name} ({code}) - 申购代码: {apply_code}")
    else:
        print("没有找到2026年1月的申购记录")
    
    # 统计各月份数据
    from collections import defaultdict
    month_count = defaultdict(int)
    for bond in sorted_bonds:
        date = bond.get('PUBLIC_START_DATE', '')
        if date and len(date) >= 7:
            month = date[:7]  # 提取年月
            month_count[month] += 1
    
    print('\n各月份申购数量统计:')
    print('-' * 70)
    for month in sorted(month_count.keys(), reverse=True)[:12]:
        print(f"{month}: {month_count[month]} 只")

if __name__ == "__main__":
    try:
        check_recent_bonds()
        print("\n✓ 查询完成")
    except Exception as e:
        print(f"\n✗ 查询失败: {e}")
        import traceback
        traceback.print_exc()