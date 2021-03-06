#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Frank Fu'

import time, uuid

from .frame.orm import Model
from .frame.fields import StringField, BooleanField, FloatField, TextField,IntegerField

class Blog(Model):
    __table__ = 'blogs'

    id = IntegerField(primary_key=True)
    name = StringField(ddl='varchar(50)')
    tag = StringField(ddl='varchar(50)')
    summary = StringField(ddl='varchar(200)')
    content = TextField()
    created_at = FloatField(default=time.time)

class Photo(Model):
	__table__='photos'

	id =IntegerField(primary_key=True)
	name = StringField(ddl='varchar(50)')
	alt = StringField(ddl='varchar(50)')
	title = StringField(ddl='varchar(50)')
	src = StringField(ddl='varchar(50)')

class Tag(Model):
	__table__="tags"

	id = IntegerField(primary_key=True)
	name = StringField(ddl='varchar(50)')