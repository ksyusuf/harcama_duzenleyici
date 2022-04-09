from __future__ import print_function
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import pprint

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

        self.icerik = self.document.get('body').get('content')
        self.dokuman_uzunlugu = len(self.icerik)

        print(self.document)
        print("- - - - - - - - - - - - - - - -")
        print(self.icerik)


if __name__ == '__main__':
    docs = GoogleDocs()
    docs.IcerigiCek()
