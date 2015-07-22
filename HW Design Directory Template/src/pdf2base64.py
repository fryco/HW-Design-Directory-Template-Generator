pdfFilename = "file.pdf"
pdfEncoded = open(pdfFilename, "rb").read().encode('base64', 'strict')

with open(pdfFilename.strip('.pdf')+"_base64.txt", "wb") as text_file:
        text_file.write(pdfEncoded)
