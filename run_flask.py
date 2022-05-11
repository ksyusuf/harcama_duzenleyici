from flask import Flask, render_template, request
from main import Kaydedici
# otomatik requirements.txt oluşturmak için
# pip3 freeze > requirements.txt

site = Flask(__name__)

@site.route("/") # anasayfa bu route ile oluşuyor sanırım. okey
def anaSayfa():
    return render_template("ana_sayfa.html")

@site.route("/goruntule", methods=['POST', 'GET'])
def goruntuleyici():
    if request.method == 'POST':
        veriler = Kaydedici()
        veriler = veriler.Goruntule()
        if veriler == "Doküman boş.":
            return "Doküman boş."
        else:
            return veriler
    else:
        return "Bu sayfayı görme yetkiniz yok!" # get metodu ile gelirsen bu çalışır

@site.route("/kayit", methods=['POST', 'GET'])
def kaydedici():
    if request.method == 'POST':
        kayitci = Kaydedici()
        return kayitci.PeriyodikIsleme()
    else:
        return "Bu sayfayı görme yetkiniz yok!" # get metodu ile gelirsen bu çalışır


if __name__ == '__main__':
    site.debug = True
    site.run(port="2000")
