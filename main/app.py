#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author: yintian
@date: 2021-06-27
@file: app.py
@Desc
"""

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sql.sql_config import APP_SQL_CONFIG

app = Flask(__name__)

request = request

app.config['SQLALCHEMY_DATABASE_URI'] = APP_SQL_CONFIG

app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

engine = create_engine(APP_SQL_CONFIG, echo=True)

DBSession = sessionmaker(bind=engine)

db = SQLAlchemy(app)

if __name__ == '__main__':
    pass
