#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def f(x):
	return "0x%x" %x

def printhex(l):
	var=""
	for x in l:
		var+=f(x)+' '
	print(var)

fo = open('foo.bin','rb+')
print ("文件名: ", fo.name)
print ("是否已关闭 : ", fo.closed)
print ("访问模式 : ", fo.mode)

a=fo.read()
print(a)
b=list(a)
printhex(b)
b.append(0x03)
c=bytes(b'hhhh')
fo.write(c)