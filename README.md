# MinHashSimilarity
Detect Plagiarism using MinHashing

In this project, I apply MinHash algorithm to measure word-level (lexical) text similarity between a query text and a
collection of existing documents. The program read the text, the cleanses it, and splits it into k-shingles, where k is 
set to be 9. Based on the number of shingles in each document, the number of MinHash functions is chosen such that it does 
not exceed the numbers of shingles in the query.

The program outputs the estimated Jaccard similarities as a dictionary, where each 
key-value pair represents a document name and its similarity score with query. To validate the implementation, I also use 
datasketch library to compute Jaccard similarities using its MinHash functionality. The program prints these scores  in
the same format for direct comparison with the custom implementation.

Test data is stored in the ./data folder, with each test set containing multiple documents and a corresponding query in 
.txt format. 

For example, in test set 1, there are 3 documents: doc1.txt, doc2.txt, and doc3.txt. The query file 
query1.txt contains text taken from doc1.txt.
The output of the program, shown below, indicates that among the three documents, doc1.txt is the most similar 
to the query. query2.txt and query3.txt are texts copied from doc2.txt and doc3.txt, respectively.
```
Jaccard similarities
{'doc1.txt': 0.26, 'doc3.txt': 0.04, 'doc2.txt': 0.12}
datasketch Jaccard similarities
{'doc1.txt': 0.26, 'doc3.txt': 0.02, 'doc2.txt': 0.02}
```

In test set 2, there is only one document (doc1.txt) and one query (query1.txt), query1.txt contains portion of the texts 
from doc1.txt. The similarity score will increase as query1.txt contains more texts from doc1.txt.
Example output for test set 2.
```
Jaccard similarities
{'doc1.txt': 0.22}
datasketch Jaccard similarities
{'doc1.txt': 0.02}
```