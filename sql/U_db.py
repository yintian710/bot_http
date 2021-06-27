#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-06-27
@file: U_db.py
@Desc
"""

from main.app import DBSession
from sql.model import U




if __name__ == '__main__':
    delete_u(11)
    res = select_u(11, 'score', 'id', 'da')
    print(res)
