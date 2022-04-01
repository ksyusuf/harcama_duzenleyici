from flask import Flask, render_template, request
import DocsGoogle

site = Flask(__name__)

@site.route("/") # anasayfa bu route ile oluşuyor sanırım. okey
def anaSayfa():
    return render_template("ana_sayfa.html")

@site.route("/goruntule", methods=['POST', 'GET'])
def goruntuleyici():
    if request.method == 'POST':
        return DocsGoogle.GoogleDocs()
    else:
        return "Bu sayfayı görmeye yetkiniz yok!" # get metodu ile gelirsen bu çalışır

@site.route("/kayit", methods=['POST', 'GET'])
def kaydedici():
    if request.method == 'POST':
        return "post edildi"
    else:
        return "Bu sayfayı görmeye yetkiniz yok!" # get metodu ile gelirsen bu çalışır

if __name__ == '__main__':
    site.debug = True
    site.run(port="2000")
