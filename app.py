import pymupdf
import ollama
import math
import time
import numpy as np

MODEL = "llama3.2:1b"
EMBED_MODEL = "nomic-embed-text"
BATCH = 32                                          # string chunk to pass for embedding
SHORT_SUMMARY_PROMPT = "Summarise the text in 3 bullet points, each under 15 words."
LONG_SUMMARY_PROMPT = (
    "These are partial summaries of consecutive sections of one document. "
    "Combine them into 6 to 8 bullet points that cover the whole document, "
    "each under 20 words."
)

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

    # list with dicts having text chunk and corresponding page number
    return chunks

# this asks the llm
def ask_llm(prompt):
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content":prompt}]
    )
    return response["message"]["content"]

# make prompt
def make_prompt(text, instruction):
    prompt = f"""{instruction}

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
def summarise_text(text, instruction = SHORT_SUMMARY_PROMPT):
    prompt = make_prompt(text, instruction)
    return ask_llm(prompt)

# summeriser for big texts
def summarise_pdf(chunks, grp_size = 5):
    if not chunks:
        return "No text found in this PDF. It may be a scanned document."

    partial_summary = []
    total_groups = math.ceil(len(chunks) / grp_size)
    
    # group texts form chunks in grp_size, convert them to one string, get their summery and append them to partial summery
    for i in range(0, len(chunks), grp_size):

        print(f"Summarising group {i // grp_size + 1} of {total_groups}...")
        temp_chunk = chunks[i : i+ grp_size]

        temp_text = combine_chunks(temp_chunk)
        summary = summarise_text(temp_text)
        partial_summary.append(summary)
    
    # combine all the partial summary string to one string and pass it to the summeriser
    final_summary = summarise_text("\n\n".join(partial_summary), LONG_SUMMARY_PROMPT)

    # return final summary
    return final_summary

# embed given string list to vectors. each string will get a vector
def embed_text(texts):
    vectors = []

    for i in range(0, len(texts), BATCH):
        to_the_model = texts[i : i + BATCH]
        result = ollama.embed(model=EMBED_MODEL, input=to_the_model)
        partial_vectors = result['embeddings'] # 2d array
        vectors.extend(partial_vectors)
    return vectors

# embed each string in chunks
def embed_chunks(chunks):
    if not chunks:
        return "No text found in this pdf. It may be scanned document."
    to_embed = []

    for chunk in chunks:
        to_embed.append(chunk["text"])
    
    embed_vec = np.array(embed_text(to_embed))
    length = np.linalg.norm(embed_vec, axis = 1, keepdims=True)
    embed_vec_normalised = embed_vec / length

    return embed_vec_normalised

# this makes the later codes execute, when this file run directly and not when it imported
if __name__ == "__main__":
    ans_list = read_pdf("big_report.pdf")
    chunks = make_chunk(ans_list)
    start = time.time()
    vec = embed_chunks(chunks)
    # joined_text = combine_chunks(chunks)
    # print(len(joined_text.split()))
    # print(summarise_pdf(chunks, grp_size = 5))
    print(len(chunks), len(vec), len(vec[0]), vec.shape)
    print(np.linalg.norm(vec[0]))
    print(f"Took {time.time() - start:.1f} seconds")