#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-06-27
@file: sql_config.py.py
@Desc
"""
import json

from tool.CONTANT import SQL_PATH

with open(SQL_PATH, 'r', encoding="utf-8") as f:
    sql_json = json.loads(f.read())

APP_SQL_CONFIG = f"mysql+pymysql://{sql_json.get('user')}:{sql_json.get('password')}@" \
    f"{sql_json.get('host')}:{sql_json.get('port')}/{sql_json.get('database')}"

if __name__ == '__main__':
    pass
