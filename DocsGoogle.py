from __future__ import print_function
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

DOCUMENT_ID = '1wOXdJ8ZbG3BQc205kVQIfoO8WOCi2oHwmOx7lx69kBc'
# google docs'taki dokümanın link kısmındaki id'si

JSON = 'kontrolcu-key.json'
# json'u google dos api'sinden credentials kısmından mail oluşturarak
# daha sonra oluşturulan mailin KEYS kısmından keyi json olarak indirdim
# daha sonra oluşturulan maili google dokümanına paylaşılan kişilere ekledim.
# bu şekilde bu mail aracılığı ile dokümana erişim sağlayabildik.


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
        self.icerik = doc_content
        self.dokuman_uzunlugu = len(self.icerik)

        # print("doküman uzunluğu: ", self.dokuman_uzunlugu, "karakter")
        # print(self.icerik)

        # title = "başlık_!"
        # Make a request body
        # requests = {'title': title}
        # böyle bir istek oluşturduk ama bunu execute etmediğimiz sürece gitmez.

        # Create the document
        # doc = service.documents().create(body=requests).execute()
        # print(doc) # belgenin mevcut tüm özelliklerini yazdırıyor
        print(self.icerik)


if __name__ == '__main__':
    print("Docs içeriden çalıştırıldı.")
    docs = GoogleDocs()
    docs.IcerigiCek()