#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查指定日期范围内的可转债数据
特别关注2026-01-16前后几天的数据
"""

import requests
import json
from datetime import datetime, timedelta

def check_date_range(start_date, end_date):
    """检查指定日期范围内的数据"""
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_BOND_CB_LIST",
        "columns": "SECURITY_CODE,SECURITY_NAME_ABBR,PUBLIC_START_DATE,CORRECODE,SECURITY_START_DATE",
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
    
    print(f"查询日期范围: {start_date} 到 {end_date}")
    print(f"数据库总条数: {len(bonds)}")
    print("=" * 80)
    
    # 筛选指定日期范围内的数据
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    
    found_bonds = []
    for bond in bonds:
        public_date_str = bond.get('PUBLIC_START_DATE', '')
        if public_date_str:
            try:
                public_date = datetime.strptime(public_date_str.split(' ')[0], '%Y-%m-%d')
                if start <= public_date <= end:
                    found_bonds.append({
                        'date': public_date_str,
                        'name': bond.get('SECURITY_NAME_ABBR', ''),
                        'code': bond.get('SECURITY_CODE', ''),
                        'apply_code': bond.get('CORRECODE', ''),
                        'security_start': bond.get('SECURITY_START_DATE', '')
                    })
            except:
                pass
    
    # 按日期排序
    found_bonds.sort(key=lambda x: x['date'])
    
    print(f"找到 {len(found_bonds)} 只可转债:\n")
    for i, bond in enumerate(found_bonds, 1):
        print(f"{i}. {bond['date']} - {bond['name']} ({bond['code']})")
        print(f"   申购代码: {bond['apply_code']}")
        print(f"   股权登记日: {bond['security_start']}")
        print()
    
    return found_bonds

def check_all_january_2026():
    """检查2026年1月所有数据"""
    print("=" * 80)
    print("检查2026年1月所有可转债数据")
    print("=" * 80)
    
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        "reportName": "RPT_BOND_CB_LIST",
        "columns": "SECURITY_CODE,SECURITY_NAME_ABBR,PUBLIC_START_DATE,CORRECODE,SECURITY_START_DATE",
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
    
    # 筛选2026年1月的数据
    january_bonds = []
    for bond in bonds:
        public_date_str = bond.get('PUBLIC_START_DATE', '')
        if public_date_str and public_date_str.startswith('2026-01'):
            january_bonds.append({
                'date': public_date_str,
                'name': bond.get('SECURITY_NAME_ABBR', ''),
                'code': bond.get('SECURITY_CODE', ''),
                'apply_code': bond.get('CORRECODE', ''),
                'security_start': bond.get('SECURITY_START_DATE', '')
            })
    
    print(f"2026年1月共有 {len(january_bonds)} 只可转债:\n")
    for i, bond in enumerate(january_bonds, 1):
        print(f"{i}. {bond['date']} - {bond['name']} ({bond['code']})")
        print(f"   申购代码: {bond['apply_code']}")
        print(f"   股权登记日: {bond['security_start']}")
        print()
    
    return january_bonds

if __name__ == "__main__":
    try:
        # 检查2026-01-16前后5天
        print("检查2026-01-16前后5天的数据:\n")
        check_date_range("2026-01-11", "2026-01-21")
        
        print("\n" + "=" * 80 + "\n")
        
        # 检查整个1月
        check_all_january_2026()
        
        print("\n✓ 查询完成")
    except Exception as e:
        print(f"\n✗ 查询失败: {e}")
        import traceback
        traceback.print_exc()
