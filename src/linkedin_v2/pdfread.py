import PyPDF2

def main():
    pdfFile="./CV_Brice_FOTZO.pdf"
    
    pdfRead=PyPDF2.PdfFileReader(pdfFile)
    page=pdfRead.getPage(0)
    pageContent=page.extractText()
    print(pageContent)
    
if __name__=="__main__":
    main()