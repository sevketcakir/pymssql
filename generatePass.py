#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import pypyodbc as pyodbc  # you could alias it to existing pyodbc code (not every code is compatible)

from datetime import timedelta, datetime


# Fonksiyon tanımlamaları
def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))
def sifre():
    pchars="qwertyuopasdfghjklizxcvbnm.*-"
    l=random.randint(6,12)
    sifre=''
    for i in range(0,l):
        sifre+=random.choice(pchars)
    return sifre

db_host = 'CAKILENOVO\SQLEXPRESS'
db_name = 'TicaretSitesi'

connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';Trusted_Connection=yes;'
db = pyodbc.connect(connection_string)
cursor = db.cursor()

sql = 'SELECT * FROM musteri'
cursor.execute(sql)
musteriDic = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

for musteri in musteriDic:
    x=sifre()
    #print(x)
    cursor.execute("UPDATE musteri SET sifre=? WHERE id=?",(x, musteri["id"]))

# Değişiklikleri kaydet ve bağlantıyı kapat
db.commit()
cursor.close()
db.close()
