import pymupdf
import ollama

MODEL = "llama3.2:1b"

# this reads the pdf file
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

# this chunk the text
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

# this asks the llm
def ask_llm(prompt):
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content":prompt}]
    )
    return response["message"]["content"]

# make prompt
def make_prompt(text):
    prompt = f"""Read the text below and write in bullet points with exact 15 words summarising it.

Rules:
- Use only the text below. Do not add outside knowledge.
- Do not write an introduction or a conclusion.

Text:
{text}
"""
    return prompt

# this combines the chunks to a single string with separator
def combine_chunks(chunks):
    joined_chunks = []
    for chunk in chunks:
        joined_chunks.append(chunk['text'])

    # join the text with new line 
    joined_text = "\n\n".join(joined_chunks)

    # this is a big string with all texts
    return joined_text

# summarise text
def summarise_text(text):
    prompt = make_prompt(text)
    return ask_llm(prompt)

# this makes the later codes execute, when this file run directly and not when it imported
if __name__ == "__main__":
    ans_list = read_pdf("testpdf.pdf")
    chunks = make_chunk(ans_list)
    joined_text = combine_chunks(chunks)
    print(len(joined_text.split()))
    print(summarise_text(joined_text))