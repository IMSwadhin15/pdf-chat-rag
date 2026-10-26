import pymupdf
import ollama

# MODEL = "llama3.2:1b"

# def read_pdf(doc_path):
#     doc = pymupdf.open(doc_path)
#     text = []
#     for page in doc:
#         text.append(page.get_text())

#     # return a list of strs, where each index store text of corresponding page
#     return text


# def make_chunk(pages, chunk_size=150):

#     chunks = []
#     # loop over all words text list
#     for page_no, text in enumerate(pages, start = 1):
#         words = text.split()
#         # if a page is blank
#         if not words:
#             continue

#         # overlap concept in chunk size
#         for i in range (0, len(words), chunk_size):
#             chunk = words[i : i+chunk_size]
#             chunks.append({
#                 "page_no" : page_no,
#                 "text"   : " ".join(chunk)
#             })
#     return chunks

# def ask_llm(prompt):
#     response = ollama.chat(
#         model=MODEL,
#         messages=[{"role": "user", "content":prompt}]
#     )
#     return response["message"]["content"]

# ans_list = read_pdf("testpdf.pdf")
# chunks = make_chunk(ans_list)
# print(len(chunks))
# print(chunks)
# print(chunks[0]['page_no'])
# print(chunks[0]['text'])
# print(chunks[4]['page_no'])
# print(chunks[4]['text'])
# print(len(chunks[0]['text'].split()))

# print(ans_list)

# print(type(ans_list[1]))
# print(ask_llm("Hello!"))

lines = [
    {"lineno": "l1", "text": "The library opened in 1962 and has served the community for over six decades."},
    {"lineno": "l2", "text": "It currently has 24 computers available for public use."},
    {"lineno": "l3", "text": "A team of 9 dedicated staff members manages the daily operations."},
    {"lineno": "l4", "text": "The library offers free internet access and a wide collection of books."},
    {"lineno": "l5", "text": "It also hosts weekly reading events for children and adults."},
]

join_line = []
for line in lines:
    join_line.append(line["text"])

print(join_line)

new = "\n\n".join(join_line)
print(type(new))