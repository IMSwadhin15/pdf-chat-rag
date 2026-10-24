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


def make_chunk(pages, chunk_size=150):
    '''
    Splits the extracted text of each page into smaller chunks of words.

    Step-by-step workflow:
    1. Initialize an empty list `chunks` to collect all chunks across the document.
    2. Loop through each page's text using enumerate (starting page numbering at 1).
    3. Split the page text into individual words using `.split()`.
    4. If the page is blank (no words), skip it using `continue`.
    5. Loop through the words in slices of size `chunk_size` (e.g., 0 to 150, 150 to 300...).
    6. For each slice, join the words back into a string and store it as a dictionary 
       with its corresponding `page_no` and `text`.
    7. Return the completed list of all chunk dictionaries.
    '''
    chunks = []
    # loop over all words text list
    for page_no, text in enumerate(pages, start = 1):
        words = text.split()
        # if a page is blank
        if not words:
            continue

        # overlap concept in chunk size
        for i in range (0, len(words), chunk_size):
            chunk = words[i : i+chunk_size]
            chunks.append({
                "page_no" : page_no,
                "text"   : " ".join(chunk)
            })
    return chunks



ans_list = read_pdf("testpdf.pdf")
chunks = make_chunk(ans_list)
print(len(chunks))
# print(chunks)
# print(chunks[0]['page_no'])
# print(chunks[0]['text'])
# print(chunks[4]['page_no'])
# print(chunks[4]['text'])
# print(len(chunks[0]['text'].split()))

# print(ans_list)

# print(type(ans_list[1]))