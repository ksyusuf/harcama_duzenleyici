import SheetsGoogle, DocsGoogle
import datetime

class Kaydedici:
    def __init__(self):
        """
        yapıcı fonksiyonumuz
        """
        self.dokumanim = DocsGoogle.GoogleDocs()
        self.excelim = SheetsGoogle.GoogleSheets()

    def kayit(self):
        """
        Kayıt işlemini gerçekleştirir.
        """
        self.dokumanim.IcerigiCek() # dokümanın boş olduğunu kontrol etmeden önce içeriği çekmelisin
        if self.dokumanim.dokumanBosMu() != True:
            self.dokumanim.verileriDuzenle()
            self.excelim.veri_ekleme(self.dokumanim.veriKayitYazdir())
            # veriKayıtYazdır'ı çalıştırmadan önce veriyi çekmiş olmaslısın [ IcerigiCeK() ]
            return "Kayıt işlemi tamamlandı."
        else:
            return "Doküman Boş!"

    def docsTemizleme(self):
        self.dokumanim.tumunuSil()


    def Goruntule(self):
        """
        verileri okunabilir şekilde görüntüler.
        :return: str
        """
        self.dokumanim.IcerigiCek()
        if self.dokumanim.dokumanBosMu() == True:
            return "Doküman boş."
        else:
            self.dokumanim.verileriDuzenle()
            return self.dokumanim.WebeGonder()

    def PeriyodikIsleme(self):
        print("Kayıt emri verildi.")
        print("Çalışmaya başladı ", datetime.datetime.strftime(datetime.datetime.now(), '%A - %X - %d.%m.%Y'))
        sonuc = self.kayit()
        print(f"{sonuc} {datetime.datetime.strftime(datetime.datetime.now(), '%A - %X - %d.%m.%Y')}")
        self.docsTemizleme()
        return sonuc

if __name__ == '__main__':
    print("mail, içeriden çağırıldı...")
    dokumanim = Kaydedici().dokumanim
    excelim = Kaydedici().excelim
    dokumanim.IcerigiCek()
    dokumanim.verileriDuzenle()
    dokumanim.WebeGonder()
    #excelim.veri_ekleme(dokumanim.veriKayitYazdir())
    #dokumanim.tumunuSil()
else:
    print("main, dışarıdan çağırıldı...")
    Kaydedici()


# kaydedici sınıfını oluşturdum. çağırılma durumunda o sınıf harekete geçecek.