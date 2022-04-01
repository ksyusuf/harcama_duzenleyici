from __future__ import print_function
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import re
import datetime


DOCUMENT_ID = '1wOXdJ8ZbG3BQc205kVQIfoO8WOCi2oHwmOx7lx69kBc'
# google docs'taki dokümanın link kısmındaki id'si

JSON = 'kontrolcu-key.json'
# json'u google dos api'sinden credentials kısmından mail oluşturarak
# daha sonra oluşturulan mailin KEYS kısmından keyi json olarak indirdim
# daha sonra oluşturulan maili google dokümanına paylaşılan kişilere ekledim.
# bu şekilde bu mail aracılığı ile dokümana erişim sağlayabildik.



# BU FONKSİYONLAR DÜZENLİ ÇIKTI ALABİLMEMİ SAĞLIYOR
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