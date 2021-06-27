#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-06-27
@file: test.py
@Desc
"""
import os
os.system(
    r"sqlacodegen --noviews --noconstraints --noindexes --outfile ./auto_file/models.py mysql://root:root@127.0.0.1:3306/test"
)

if __name__ == '__main__':
    pass
