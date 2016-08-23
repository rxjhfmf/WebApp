#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for user, blog, comment.
'''

__author__ = 'Frank Fu'

import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField,IntegerField

class Blog(Model):
    __table__ = 'blogs'

    id = IntegerField(primary_key=True)
    name = StringField(ddl='varchar(50)')
    tag = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)
    count = IntegerField(primary_key=False)
