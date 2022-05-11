import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

JSON = 'kontrolcu-key.json'
# bu key sheets için de docs için de kullanılıyor.

class GoogleSheets:
    def __init__(self):
        scope = ["https://www.googleapis.com/auth/drive"]

        creds = ServiceAccountCredentials.from_json_keyfile_name(JSON, scope)

        # şu alttaki kısım: gspread kütüphanesi ile çalışıyor.
        # bu kütüphaneyi kullanabilmek için de google drive api aktif edilmeli.
        # ayrıca scope sadece drive erişimi ile çalışabiliyor.
        client = gspread.authorize(creds)
        self.sheet = client.open("Gider Düzenleyici").sheet1  # Open the spreadhseet

    def veri_ekleme(self, harcamalar):
        for harcama in harcamalar:

            tarih = harcama["tarih"]  # buradan datetime formatında veri gelecek
            gelen_gun_degeri = datetime.date(year=tarih.year, month=tarih.month, day=tarih.day).toordinal()
            gelen_gun_degeri = gelen_gun_degeri - 693594
            # google sheetse göre tarih düzeltme değeri bu.

            yazdirilacak_veri = [
                gelen_gun_degeri,
                float(harcama['tutar']),
                harcama['harcama'],
                harcama['açıklama']
                ]
            print(yazdirilacak_veri)

            self.sheet.insert_row(yazdirilacak_veri, 3)

if __name__ == '__main__':
    print("Çalışıyor...")
    sheets = GoogleSheets()

    yuklenecek_veri = {'tarih': "15.04.2022",
                       'harcama': 'balık ekmek',
                       'tutar': 25,
                       'açıklama': 'yemek'}
    sheets.veri_ekleme(yuklenecek_veri)
    print("Harcama yüklendi.")
