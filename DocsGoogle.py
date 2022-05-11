from __future__ import print_function
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import re
import datetime

DOCUMENT_ID = '1wOXdJ8ZbG3BQc205kVQIfoO8WOCi2oHwmOx7lx69kBc'
# google docs'taki dokümanın link kısmındaki id'si
# nku hesabı ile entegreliyiz.

JSON = 'kontrolcu-key.json'


# json'u google dos api'sinden credentials kısmından mail oluşturarak
# daha sonra oluşturulan mailin KEYS kısmından keyi json olarak indirdim
# daha sonra oluşturulan maili google dokümanına paylaşılan kişilere ekledim.
# bu şekilde bu mail aracılığı ile dokümana erişim sağlayabildik.


# BU FONKSİYONLAR DÜZENLİ ÇIKTI ALABİLMEMİ SAĞLIYOR
# ilki belgedeki elementlerle ilgili kontrol sağlıyor. ikinci işi bitiriyor.
def read_paragraph_element(element):
    """Dokümandaki elementlere göre ayıklama yapıyor
        Args:
            element: GoogleDocs'taki içeriğin content kısmını alır.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')
def read_strucutural_elements(elements):
    """Metnin tüm elementlerini inceler aradan içeriği temize çeker.
        Args:
            elements: Elementlerin listesini alır.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_strucutural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            # The text in the TOC is also in a Structural Element.
            toc = value.get('tableOfContents')
            text += read_strucutural_elements(toc.get('content'))
    return text

ay_sirasi = {
    "ocak": 1,
    "şubat": 2,
    "mart": 3,
    "nisan": 4,
    "mayıs": 5,
    "haziran": 6,
    "temmuz": 7,
    "ağustos": 8,
    "eylül": 9,
    "ekim": 10,
    "kasım": 11,
    "aralık": 12
}

class GoogleDocs:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/documents']
        self.DOCUMENT_ID = DOCUMENT_ID
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(JSON, self.SCOPES)
        self.service = build('docs', 'v1', credentials=self.creds)

    def IcerigiCek(self):
        # Retrieve the documents contents from the Docs service.
        self.document = self.service.documents().get(documentId=self.DOCUMENT_ID).execute()

        print('\n---------------------------------------\n'
              'Dokümanınızın başlığı: {}\n'.format(self.document.get('title')))

        doc_content = self.document.get('body').get('content')
        self.icerik = read_strucutural_elements(doc_content)
        self.dokuman_uzunlugu = len(self.icerik)

        # print(self.document)
        # print("- - - - - - - - - - - - - - - -")
        # print(self.icerik)

    def tumunuSil(self):
        """Dokümanı temizler."""
        if (self.dokuman_uzunlugu > 1):
            requests = [
                {
                    'deleteContentRange': {
                        'range': {
                            'startIndex': 1,
                            'endIndex': self.dokuman_uzunlugu,
                        }

                    }

                },
            ]
            result = self.service.documents().batchUpdate(
                documentId=self.DOCUMENT_ID, body={'requests': requests}).execute()
            print("Tüm içerik silindi.")
        else:
            print("Silme işlemi başarısız.\nDoküman zaten boş.")

    def durumSifirlayici(self):
        self.turMu = False
        self.aciklamaMi = False

    def dokumanBosMu(self):
        if self.dokuman_uzunlugu <= 1:
            # print("Doküman boş")
            return True

    def verileriDuzenle(self):
        while True: # düzenlenecek veriyi fazla satırlardan arındırır.
            if "\n\n" not in self.icerik:
                break
            else:
                self.icerik = self.icerik.replace("\n\n", "\n")


        while True: # düzenlenecek veriyi fazla boşluk karakterlerinden arındırır.
            if "  " not in self.icerik:
                break
            else:
                self.icerik = self.icerik.replace("  ", " ")


        gunler = self.icerik.splitlines()
        # tüm veriyi \n karakterinden, yani satırbaşlarından ayırdım.
        # çünkü her yeni tarihi satırabaşı ile ifade ediyorum.

        self.return_edilecek_harcamalar = []  # bunun içine google sheet'e göndereceğimiz veriler ekleniyor.

        bir_adet_harcama = {}

        tur = []
        aciklama = []
        karaktersiz = []

        def BirAdetYazdirma():
            bir_adet_harcama["tarih"] = duzenli_tarih

            bir_adet_harcama["harcama"] = " ".join(tur)
            tur.clear()

            bir_adet_harcama["tutar"] = str(harcama)  # tutarı şimdilik string olarak kaydediyorum.
            # duruma göre ondalık sayı olarak kaydederim.

            bir_adet_harcama["açıklama"] = " ".join(aciklama)
            aciklama.clear()

            karaktersiz_aciklama = " ".join(karaktersiz)
            if not karaktersiz:  # karaktersizler listesi boş ise pas geçsin yoksa yazdırsın.
                pass
            else:
                bir_adet_harcama["açıklama"] = "@ " + karaktersiz_aciklama
                karaktersiz.clear()

            self.return_edilecek_harcamalar.append(bir_adet_harcama.copy())
            bir_adet_harcama.clear()

        self.durumSifirlayici()  # bu fonksiyonla durumları çağırdım döngüye.

        for BirGun in gunler:

            tarih = BirGun.split(" ", 2)[:2]
            # ikinci boşluk tarihten sonrasını ifade ediyor. örneğin
            # 29 şubat bla bla bla (harcama kısmı)
            # ikinci boşluktan bölüp soldaki parçayı alınca tarihi almış oluyoruz.

            harcama_kismi = BirGun.split(" ", 2)[2:][0].replace(",", ".")
            # ikinci boşluktan bölüp sağdaki parçayı alınca HARCAMA kısmını almış oluyoruz.
            # ayrıca ondalık ayıracı olarak . kullanıldığından, ondalık değerlerin düzeltilmesi için
            # virgülleri nokta ile değiştriyoruz.
            # bunun sebebi harcama içinde ondalıklı işlem var ise eval fonksiyonu hata vermemesidir.
            # ancak tüm içerikteki virgülleri etkiliyor bu. yani açıklama kısmına vigüllü bir şey yazarsan
            # bu nokta olur.
            # print(harcama_kismi)

            tarih_gun = tarih[0].zfill(2)
            # tarihin gün kısmını veriyo başında sıfır olarak iki haneli şekilde ( 2 kasım => 02 kasım )
            tarih_ay = tarih[1]  # tarihin ay kısmını alıyor.
            # tarihe ek olarak yılı da eklemem gerekebilir. excelin formatına göre.
            # şimdilik programı çalıştırdığımız tarihin yılı ile kayıt gerçekleştiriliyor.
            tarih_yil = str(datetime.datetime.now().year)
            duzenli_tarih = datetime.date(year=int(tarih_yil), month=int(ay_sirasi[tarih_ay.lower()]),
                                          day=int(tarih_gun))
            # girilmiş tarihi datetime modülü ile okunabilir hale getiriyoruz. excele işlemede işimize yaryacak.
            # print("harcama kısmı string: " + harcama_kismi)
            anahtar = "#"

            for harcama in harcama_kismi.split(" "):
                # harcama kısmını kelime kelime ele alıyoruz.
                # işlem yapılabilir sayı görene kadar kelimeleri ilgili hücrelere kaydediyor.
                # örneğin ulaşım kategorisindeki harcamayı görünce ulaşım değeri olduğunu kaydediyor.
                # sistem biraz tersten işliyor. ilk başta sayı değeri olup olmadığını kontrol ediyor
                # eğer sayı değilse (tutar) içerik bilgisidir deyip ilgili yerlere işleme yapıyoruz.
                if harcama.isdigit():
                    # içinde SADECE sayı değeri var.
                    BirAdetYazdirma()
                    self.durumSifirlayici()
                    continue
                elif (("." in harcama) or ("+" in harcama) or ("-" in harcama) or ("*" in harcama) or ("/" in harcama)) \
                        and ((re.search("[0-9]\.[0-9]", harcama)) or re.search("[0-9]\+[0-9]", harcama) or re.search(
                    "[0-9]-[0-9]", harcama)
                             or re.search("[0-9]\*[0-9]", harcama) or re.search("[0-9]/[0-9]", harcama)):
                    # içinde [ . + - * / ] var ve bunlar sayılar arasında.
                    harcama = eval(harcama)  # güvenlik açığı !!!
                    BirAdetYazdirma()
                    self.durumSifirlayici()
                    continue
                elif (("+" in harcama) or ("-" in harcama) or ("*" in harcama) or ("/" in harcama)) and not (
                re.search("[A-Za-z]-[A-Za-z]", harcama)):
                    # içinde [ . + - * / ] var, öncesinde ve sonrasında herhangi bir harf YOK.
                    harcama = eval(harcama)  # güvenlik açığı !!!
                    BirAdetYazdirma()
                    self.durumSifirlayici()
                    continue
                else:
                    # buraya geldiyse demek ki bu bir karakter dizisi, işlenecek.
                    if harcama[0] == anahtar:
                        # harcama denilen şey belirteç ise ilk karakteri '#'dir. bunun kontrolünü sağlıyoruz.
                        # eğer belirteçe denk geldiyse ikinci karakterine göre yerleşim yapıyoruz.
                        # örneğin #t ulaşım --- bu; harcamanın türünün ulaşım olduğunu ifade ediyor.
                        # ben şimdi özel karakterler ayarlayabilecek şekilde modifikasyon sağlayacağım.
                        #     self.KategoriKontrol(harcama[1])
                        if harcama[1] == "h":
                            self.turMu = True
                            self.aciklamaMi = False
                            continue
                        elif harcama[1] == "a":
                            self.turMu = False
                            self.aciklamaMi = True
                            continue
                        else:
                            print("Yanlış etiket !!!")

                    if self.turMu == True:
                        tur.append(harcama.capitalize())
                        continue
                    elif self.aciklamaMi == True:
                        aciklama.append(harcama.capitalize())
                        continue
                    else:
                        # print("karaktersizler var!!")
                        karaktersiz.append(harcama)

        # print(self.return_edilecek_harcamalar)
        # print("Harcama sayısı: ", len(self.return_edilecek_harcamalar))

    def KategoriKontrol(self, belirtec):
        """
        Belirteçlere göre durumların değerlerini günceller.
        ilgili duruma True, diğerlerine False değerini atar.
            :param belirtec: tek karakterli string dizisi alır.
        """
        # TODO: fonksiyon henüz açıklamadaki işlevini yerine getiremiyor.
        SorguListesi = [self.turMu, self.aciklamaMi]
        belirtec_listesi = {
            self.turMu: "t",
            self.aciklamaMi: "a",
        }

        for kontrol_belirteci, sorgu in belirtec_listesi, SorguListesi:
            self.durumSifirlayici()
            if kontrol_belirteci == sorgu:
                self.turMu = False
                self.aciklamaMi = False

    def WebeGonder(self):
        """
        Webde görüntüleme fonksiyonu
        normalde burada [ tuple, tuple, ... ] şeklinde göndermeliydim ama yapamadım.
        okunan veri string yapılıp gönderildikten sonra html tarafında json yapılarak
        düzenli gösterim sağlanmaktadır.
        fonksiyonun çıktısı: {"tutar": "20.5", "tarih": "d ... bu bir stringtir.
        """

        json_olarak_liste = []

        # print(str(self.return_edilecek_harcamalar))
        string_json = str(self.return_edilecek_harcamalar).replace("'", '"').replace(' d', ' "d').replace('),', ')",').replace("[", "").replace("]", "").replace("},", "},,,")
        """
        string_json: {"tutar": "20.5", "tarih": "d ... şeklinde bir yapıdadır.
        # bu yapıyı burada json yapamadım ben de string olarak yollayıp html tarafında json haline getirip
        # görsellik sundum.
        # print(string_json)
        """
        return string_json

    def veriKayitYazdir(self):
        return self.return_edilecek_harcamalar


if __name__ == '__main__':
    docs = GoogleDocs()
    docs.IcerigiCek()
