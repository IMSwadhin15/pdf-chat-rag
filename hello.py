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

# lines = [
#     {"lineno": "l1", "text": "The library opened in 1962 and has served the community for over six decades."},
#     {"lineno": "l2", "text": "It currently has 24 computers available for public use."},
#     {"lineno": "l3", "text": "A team of 9 dedicated staff members manages the daily operations."},
#     {"lineno": "l4", "text": "The library offers free internet access and a wide collection of books."},
#     {"lineno": "l5", "text": "It also hosts weekly reading events for children and adults."},
# ]

# join_line = []
# for line in lines:
#     join_line.append(line["text"])

# print(join_line)

# new = "\n\n".join(join_line)
# print(type(new))

# import numpy as np

# def cosine(a, b):
#     a, b = np.array(a), np.array(b)
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# print(cosine([1, 0], [1, 0]))
# print(cosine([1, 0], [0, 1]))
# print(cosine([1, 1], [1, 0]))

import ollama
import numpy as np

# texts = ["I love libraries", "Books are great", "The car is red"]
# resp = ollama.embed(model="nomic-embed-text", input=texts)
# vectors = resp["embeddings"]

# print(len(vectors), len(vectors[0]))   # how many vectors, and how long is each


# str = "What is Red"
# resp_str = ollama.embed(model="nomic-embed-text", input=str)
# resp_vec = resp_str["embeddings"]
# print(len(resp_vec[0]))

# def cosine(a, b):
#     a, b = np.array(a), np.array(b)
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# print(cosine(vectors[0], resp_vec[0]))
# print(cosine(vectors[1], resp_vec[0]))
# print(cosine(vectors[2], resp_vec[0]))

texts = [
    "I love libraries",
    "Books are great",
    "The car is red",
    "Reading helps improve vocabulary and focus",
    "Public libraries provide free access to knowledge",
    "She drove her blue sedan down the highway",
    "Electric vehicles are becoming more popular",
    "The chef prepared a delicious pasta dish",
    "Artificial intelligence is transforming technology",
    "The sun rises in the east every morning",
]

batch_size = 2
def embed_text(texts):
    vectors = []

    for i in range(0, len(texts), batch_size):
        to_the_model = texts[i : i + batch_size]
        result = ollama.embed(model="nomic-embed-text", input=to_the_model)
        partial_vectors = result['embeddings'] # 2d array
        vectors.extend(partial_vectors)
    return vectors

vec = embed_text(["hello"]* 70)
print(len(vec))
print(len(vec[0]), len(vec[1]))
# vec2 = embed_text(texts[:3])
# print(len(vec2))

# vec1 = [
#     [1,2,3],
#     [4,5,6],
#     [7,8,9]
# ]
# vec = [[10,11,12],[13,14,15],[16,17,18]]
# vec1.extend(vec)
# print(vec1)
