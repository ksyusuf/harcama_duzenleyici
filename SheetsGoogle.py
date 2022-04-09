import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
import datetime

DOCUMENT_ID = '1n6jwfnnHECDa-e1nJS4sYARojYkAA0rpZTDoi8jT_qw'
JSON = 'kontrolcu-key.json'
# bu key sheets için de docs için de kullanılıyor.

class GoogleSheets:
    def __init__(self):
        self.scope = ["https://www.googleapis.com/auth/spreadsheets"]

        self.sheet_id = DOCUMENT_ID
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(JSON, self.scope)
        self.credss = ServiceAccountCredentials.from_json_keyfile_name(JSON, self.scope)
        self.service = discovery.build('sheets', 'v4', credentials=self.creds)
        self.client = gspread.authorize(self.credss)
        self.sheet = self.client.open("Gider Düzenleyici").sheet1
        # TODO: TEK TEK SATIR EKLEME İŞLEMİNİ YAPAMALIYIM. HOCAYA SUNUMDA HAVALI OLACAK

    def veri_ekleme(self, return_edilmis_veri):
        # data = self.sheet.get_all_records()  # Get a list of all records
        # row = self.sheet.row_values(3)  # Get a specific row
        # col = self.sheet.col_values(3)  # Get a specific column
        # cell = self.sheet.cell(1,1).value  # Get the value of a specific cell
        self.sheet.add_rows(8)  # istenen adette satır ekliyor
        # sheet.update_cell(2,2, "CHANGED")  # Update one cell
        # self.sheet.append_row(insertRow, table_range="A7")
        # numRows = sheet.row_count  # Get the number of rows in the sheet
        # sheet.append_row(insertRow, table_range="G2:G3")

        # FORMATIMIZ ŞÖYLEYDİ [[ TARİH TUTAR FİRMA TÜR MALZEME AÇIKLAMA ]]
        # self.sheet.insert_row(insertRow ,8) # belirlenen satırı aşağı kaydırıp veriyi ekliyor. bizim işimize yarayan bu

        # tarih formatı şöyle olacak
        # dd.mmmm.yyyy

        # print(return_edilmis_veri)

        print("Yükleniyor...")
        yazma_siniri_sayaci = 0
        yazdirilacak_veri = []

        #creds = None
        #creds = ServiceAccountCredentials.from_service_account_file(
        #    kimlik_bilgileri.JSON, scopes=self.hedef)
        # service = build('sheets', 'v4', credentials=self.creds)

        for harcama in return_edilmis_veri:
            # datetime modulünde 1. değer 01/01/0001 tarihine karşılık geliyor.
            # excelde 1. değer 31/12/1899 tarihine karşılık geliyor.
            # python ve excel tarih değer farkı = 693.594 693594
            # gelen tarih değerinin üzerinde işlem yapabilmek için
            # onu matematiksel ifadeye dönüştürdüm.
            tarih = harcama["tarih"] # buradan datetime formatında veri gelecek
            gelen_gun_degeri = datetime.date(year=tarih.year, month=tarih.month, day=tarih.day).toordinal()
            # print("gelen gun değeri", gelen_gun_degeri)
            gelen_gun_degeri = gelen_gun_degeri - 693594
            # eklenecek_sharcama = ["",
            #                       "",
            #                       "",
            #                       gelen_gun_degeri,
            #                       float(harcama["tutar"]),
            #                       harcama["firma"],
            #                       harcama["tür"],
            #                       harcama["malzeme"],
            #                       harcama["açıklama"]]

            # bu metotla her seferinde istek gönderiyo sheets'e. kotayı kötü etkileyen yöntem
            # yeni yöntemde verileri sözlük gibi bir yapıda tutup topluca yazdıracğız
            # bu şekilde yazma sınırı olayını da kaldırabileceğiz.
            # self.sheet.insert_row(eklenecek_sharcama, 4)

            # yazma_siniri_sayaci = yazma_siniri_sayaci + 1
            # print("Tamamlanan kayıt no.: ", yazma_siniri_sayaci)
            #
            # # yazdırma sırasında bir hata olmasın diye azcık bekletiyoruz
            # if yazma_siniri_sayaci % 30 == 0:
            #     print("Yazma sınırı! (130 sn bekliyor...)")
            #     time.sleep(130)

            yazdirilacak_veri.append(
                        [
                           gelen_gun_degeri,
                           float(harcama['tutar']),
                           harcama['firma'],
                           harcama['tür'],
                           harcama['malzeme'],
                           harcama['açıklama']
                        ])

        range_ = 'D3:I3'

        value_range_body = {
            "values": yazdirilacak_veri
        }


        request = self.service.spreadsheets().values()\
            .append(spreadsheetId=self.sheet_id,
                    range=range_,
                    valueInputOption='USER_ENTERED',
                    insertDataOption='INSERT_ROWS',
                    body=value_range_body)

        response = request.execute()

if __name__ == '__main__':
    print("sheets içeriden çalıştırıldı")
    sheets = GoogleSheets()

    # datetime modulünde 1. değer 01/01/0001 tarihine karşılık geliyor.
    # excelde 1. değer 31/12/1899 tarihine karşılık geliyor.
    # python ve excel tarih değer farkı = 693.594 693594
    # gelen tarih değerinin üzerinde işlem yapabilmek için
    # onu matematiksel ifadeye dönüştürdüm.

    gelen_gun_degeri = datetime.date(year=2021, month=11, day=13).toordinal()
    gelen_gun_tarihi = datetime.date(year=2021, month=11, day=5)
    # içeriden çalıştırırken gelen gün değerinin tarihi yok ki.
    # tarih farklı yapıda olduğundan, içeriden çalıştıramazsın şimdilik.
    # print(gelen_gun_tarihi)
    # print(datetime.date.fromordinal(gelen_gun_degeri))
    yuklenen_veri = [{'tarih': gelen_gun_tarihi,
                      'tutar': 55,
                      'firma': 'Albatros',
                      'tür': 'Kişisel',
                      'malzeme': 'Nargile',
                      'açıklama': 'Sheetsi içeriden çalıştırdım'}]
    sheets.veri_ekleme(yuklenen_veri)
