import pymupdf


def read_pdf(doc_path):
    '''
        This function takes the document as argument. Open it and extract text from each page. Keep the extracted texts in a list called 'text' with index reference to each page numbers. 
    '''

    doc = pymupdf.open(doc_path)
    text = []
    for page in doc:
        text.append(page.get_text())

    # return a list of strs, where each index store text of corresponding page
    return text




ans_list = read_pdf("testpdf.pdf")
for page in ans_list:
    print(len(page.split()))
    print(" ")