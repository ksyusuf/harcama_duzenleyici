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

    def veri_ekleme(self, return_edilmis_veri):

        for harcama in return_edilmis_veri:
            tarih = harcama["tarih"]  # buradan datetime formatında veri gelecek
            gelen_gun_degeri = datetime.date(year=tarih.year, month=tarih.month, day=tarih.day).toordinal()
            gelen_gun_degeri = gelen_gun_degeri - 693594

            eklenecek_sharcama = [gelen_gun_degeri,
                                  float(harcama["tutar"]),
                                  harcama["firma"],
                                  harcama["tür"],
                                  harcama["malzeme"],
                                  harcama["açıklama"]]

            self.sheet.insert_row(eklenecek_sharcama, 4)


if __name__ == '__main__':
    print("Çalışıyor...")
    sheets = GoogleSheets()

    gelen_gun_tarihi = datetime.date(year=2021, month=11, day=5)

    yuklenen_veri = [{'tarih': gelen_gun_tarihi,
                      'tutar': 55,
                      'firma': 'Albatros',
                      'tür': 'Kişisel',
                      'malzeme': 'Nargile',
                      'açıklama': 'Sheetsi içeriden çalıştırdım'}]
    sheets.veri_ekleme(yuklenen_veri)
    print("Harcama yüklendi.")
