import PyPDF2


def pdfToText(filePath: str) -> None:
    # using pypdf2 PdfReader to convert pdf to text
    pdfFileObj = open(filePath, 'rb')
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    text = ""
    for i in range(len(pdfReader.pages)):
        text += pdfReader.pages[i].extract_text()
    pdfFileObj.close()

    new_text_file = open("docs/vrc.txt", "w")
    new_text_file.write(text)
    new_text_file.close()
    
