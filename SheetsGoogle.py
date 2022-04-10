import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

    def veri_ekleme(self, harcama):
        eklenecek_sharcama = [harcama["tarih"],
                              harcama["harcama"],
                              float(harcama["tutar"]),
                              harcama["açıklama"]]

        self.sheet.insert_row(eklenecek_sharcama, 3)

if __name__ == '__main__':
    print("Çalışıyor...")
    sheets = GoogleSheets()

    yuklenecek_veri = {'tarih': "15.04.2022",
                       'harcama': 'balık ekmek',
                       'tutar': 25,
                       'açıklama': 'yemek'}
    sheets.veri_ekleme(yuklenecek_veri)
    print("Harcama yüklendi.")
