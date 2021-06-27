#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-06-27
@file: model.py
@Desc
"""
from main.app import db


class U(db.Model, ):
    id = db.Column(db.BIGINT, primary_key=True, default=0)
    score = db.Column(db.INT, default=0)
    da = db.Column(db.VARCHAR(255), default=0)
    UR = db.Column(db.INT, default=0)
    SSR = db.Column(db.INT, default=0)
    SR = db.Column(db.INT, default=0)
    R = db.Column(db.INT, default=0)
    N = db.Column(db.INT, default=0)
    estate = db.Column(db.INT, default=0)
    rent = db.Column(db.INT, default=0)
    rent_time = db.Column(db.DATETIME, default='0000-00-00 00:00:00')
    investment = db.Column(db.INT, default=0)
    money = db.Column(db.INT, default=0)
    achievement = db.Column(db.TEXT)
    permission = db.Column(db.VARCHAR(255), default='user')

    def get(self, *args):
        return tuple(getattr(self, _) for _ in args)


print(all_table)


# db.create_all()

if __name__ == '__main__':
    pass
    # users = U.query.filter_by(id=1327960105)
    users = U.query.all()

    U.query.filter_by(id=1327960105).all()
    # u = U()
    print(users.first())
    # print(type(users[0]))
