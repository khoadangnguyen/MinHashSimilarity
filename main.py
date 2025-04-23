import re
import hashlib
import os
import math
import random


def cleanse_text(text):
    removed_punctuation = re.sub(r'[^\w\s]', '', text)
    lower_case = removed_punctuation.lower()
    removed_space = re.sub(r'\s+', '', lower_case)
    return removed_space

def k_shingles_word(text, k):
    return [text[i:i+k] for i in range(len(text) - k + 1)]

def stable_hash(text):
    return int(hashlib.md5(text.encode()).hexdigest(), 16)

def is_prime(x):
    for i in range(3, int(math.sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True

def find_prime(x):
    if x % 2 == 0:
        n = x+1
    else:
        n = x+2
    while not is_prime(n):
        n += 2
    return n

def generate_hash_functions(n, prime_number):
    hash_functions = []
    for i in range(0, n):
        hash_functions.append(
            {'a': random.randrange(1, prime_number),
             'b': random.randrange(0, prime_number)})
    return hash_functions

def apply_minhash(hash_functions, prime_number, kshingles):
    minhash = []
    for i in range(0, len(hash_functions)):
        hashed_kshingles = []
        for kshingle in kshingles:
            hashed_kshingles.append((hash_functions[i]['a']*kshingle + hash_functions[i]['b']) % prime_number)
        minhash.append(min(hashed_kshingles))
    return minhash

data_set_path = 'data/set01'

with open(data_set_path + '/query1.txt', 'r', encoding='utf-8') as file:
    query = file.read()
query = cleanse_text(query)
query_kshingles = k_shingles_word(query, 9)
print(f'number of shingles in the query = {len(query_kshingles)}')
hashed_query_kshingles = [stable_hash(kshingle) for kshingle in query_kshingles]

total_kshingles = len(query_kshingles)
folder_path = data_set_path
docs_kshingles = {}
hashed_docs_kshingles = {}
for filename in os.listdir(folder_path):
    if filename.startswith('doc'):
        full_filename = folder_path + '/' + filename
        with open(full_filename, 'r', encoding='utf-8') as file:
            doc = file.read()
        doc = cleanse_text(doc)
        doc_kshingles = k_shingles_word(doc, 9)
        hashed_doc_kshingles = [stable_hash(kshingle) for kshingle in doc_kshingles]
        docs_kshingles[filename] = doc_kshingles
        hashed_docs_kshingles[filename] = hashed_doc_kshingles
        total_kshingles += len(doc_kshingles)
n = 100
print(f'number of minhash functions: {n}')
prime_number = find_prime(total_kshingles)
hash_functions = generate_hash_functions(n, prime_number)
minhash_query = apply_minhash(hash_functions, prime_number, hashed_query_kshingles)
#print(minhash_query)
minhash_docs = {}
similarities = {}
for key,hashed_doc_kshingles in hashed_docs_kshingles.items():
    minh = apply_minhash(hash_functions, prime_number, hashed_doc_kshingles)
    print(minh)
    print(minhash_query)
    minhash_docs[key] = minh
    intersection = sum(1 for a, b in zip(minhash_query, minh) if a == b)
    print(intersection)
    similarities[key] = intersection/n
print('Jaccard similarities')
print(similarities)

import datasketch as ds
query_mh = ds.MinHash(num_perm=n)
for query_kshingle in query_kshingles:
    query_mh.update(query_kshingle.encode('utf8'))
similarities = {}
for key,doc_kshingles in docs_kshingles.items():
    doc_mh = ds.MinHash(num_perm=n)
    for doc_kshingle in doc_kshingles:
        doc_mh.update(doc_kshingle.encode('utf8'))
    similarities[key] = query_mh.jaccard(doc_mh)
print('datasketch Jaccard similarities')
print(similarities)