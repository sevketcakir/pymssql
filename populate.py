#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import pypyodbc as pyodbc  # you could alias it to existing pyodbc code (not every code is compatible)

from datetime import timedelta, datetime


# Fonksiyon tanımlamaları
def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())))


db_host = 'PAUPC\SQLEXPRESS'
db_name = 'TicaretSitesi'

connection_string = 'Driver={SQL Server};Server=' + db_host + ';Database=' + db_name + ';Trusted_Connection=yes;'
db = pyodbc.connect(connection_string)
cursor = db.cursor()

sql = 'SELECT * FROM urun;'
cursor.execute(sql)
urunlerDic = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
sql = 'SELECT * FROM musteri'
cursor.execute(sql)
musteriDic = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
# musteri_id=list()
# for res in query_results:
#     musteri_id.append(res["id"])
# print(musteri_id)
# for i in range(1,100):
#     sql='INSERT INTO DENEME VALUES({0});'.format(random.randint(1,99999))
#     cursor.execute(sql)
# db.commit()

# Tanımları yükle
with open('input/adres.txt') as f:
    adresler = f.readlines()
with open('input/adres_tanim.txt') as f:
    adres_tanim = f.readlines()

# Tablolardan verileri sil
cursor.execute('DELETE FROM fatura_detay')
cursor.execute('DELETE FROM fatura')
cursor.execute('DELETE FROM musteri_adres;')

# Müşteri adreslerini yükle
for i in range(0, len(musteriDic)):
    cursor.execute('INSERT INTO musteri_adres (adres_tanim,adres,musteri_id) VALUES(?,?,?)',
                   (random.choice(adres_tanim), random.choice(adresler), musteriDic[i]["id"]))
for i in range(0, len(musteriDic)):
    cursor.execute('INSERT INTO musteri_adres (adres_tanim,adres,musteri_id) VALUES(?,?,?)',
                   (random.choice(adres_tanim), random.choice(adresler), random.choice(musteriDic)["id"]))
db.commit()
# Siparişleri oluştur
for sp in range(1,3000):
    bas_tar = datetime.strptime("01.01.2000", "%d.%m.%Y")
    bit_tar = datetime.strptime("05.05.2016", "%d.%m.%Y")
    durum = ['satildi', 'satildi', 'beklemede', 'iptal']  # satildi ağırlığı daha fazla
    # print(random_date(bas_tar, bit_tar))

    m_id = random.choice(musteriDic)["id"]
    cursor.execute("SELECT id FROM musteri_adres WHERE musteri_id=?;", (m_id,))
    mAdDict = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    #print(m_id)
    cursor.execute("INSERT INTO fatura (tarih,durumu,musteri_id,adres_id) VALUES(?,?,?,?)",
                   (random_date(bas_tar, bit_tar), random.choice(durum), m_id,random.choice(mAdDict)["id"]))
    cursor.execute("SELECT @@IDENTITY as snum") # Eklenen satırın id'sini al
    snum = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()][0]["snum"]# Bunun çok daha basiti vardır ama python bilmeyince kulağı böyle gösteriyor insan
    dsay = random.randint(1,6)
    toplam=0.0
    for i in range(1,dsay+1):
        urun=random.choice(urunlerDic)
        miktar=random.randint(1,5)
        cursor.execute("INSERT INTO fatura_detay (urun_id,tutar,satir_no,miktar,fatura_id) VALUES(?,?,?,?,?)",
                       (urun["id"],urun["fiyat"],i,miktar,snum))
    cursor.execute("UPDATE fatura SET toplam_tutar=(SELECT SUM(tutar*miktar) FROM fatura_detay WHERE fatura_id=?) WHERE id=?",
                   (snum,snum))
# Değişiklikleri kaydet ve bağlantıyı kapat
db.commit()
cursor.close()
db.close()
