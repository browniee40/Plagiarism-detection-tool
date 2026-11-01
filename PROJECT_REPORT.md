# PROJECT REPORT
## PLAGIARISM DETECTION TOOL USING PYTHON

### 1. Introduction
Plagiarism means presenting another person's words or work as one's own without appropriate acknowledgement. Manually comparing long documents can be difficult. This project develops a basic web-based tool that compares two text documents and identifies matching sequences.

### 2. Problem statement
To design and implement a web application that accepts two text documents, finds matching text segments using hashing and string matching, highlights the common content, and calculates a text similarity percentage.

### 3. Objectives
- Build a simple browser-based document comparison interface.
- Tokenize and normalize input text.
- Apply a rolling hash technique to locate candidate matching sequences.
- Verify hash matches using exact string comparison.
- Highlight matching text and calculate a similarity score.

### 4. Scope
The current version compares two pasted texts or UTF-8 `.txt` files. It works locally and does not query an external plagiarism database. It is intended for educational demonstration of algorithms.

### 5. System requirements
**Hardware:** Computer with a modern web browser and at least 2 GB RAM.

**Software:** Python 3.9+, Flask, pip, and a modern web browser.

### 6. Methodology
The user enters or uploads two documents. The application converts each document into lowercase word tokens. It creates consecutive word windows and calculates a polynomial rolling hash for each window in the first document. Hashes from the second document are checked against this index. Any candidate is verified by comparing the actual words. Matching runs are extended and highlighted. Finally, the application calculates the percentage of matching token positions relative to the larger document.

### 7. Algorithm
1. Read Document A and Document B.
2. Normalize both documents and tokenize them.
3. Choose a window size N.
4. Compute rolling hashes for all N-word windows in A and store their positions.
5. Compute rolling hashes for windows in B.
6. For each hash found in A, compare the actual word windows.
7. Extend verified matches to full matching runs.
8. Mark matched token positions in both documents.
9. Calculate similarity and display the report.

### 8. Similarity formula
Similarity percentage:

`(Number of matching token positions in Document B / Maximum word count of the two documents) × 100`

The formula is a simple project metric, not a universal academic plagiarism score.

### 9. Modules
- **Input module:** Accepts pasted text or `.txt` files.
- **Preprocessing module:** Converts text into normalized tokens.
- **Hashing module:** Calculates rolling hash fingerprints.
- **Matching module:** Verifies candidate windows and extends matching passages.
- **Reporting module:** Displays the score, snippets, counts, and highlights.

### 10. Testing
Test the application with:
- Two identical documents.
- Two completely different documents.
- Documents with one shared sentence.
- Documents with a short common phrase.
- Empty input.
- Unsupported file type.
- Text shorter than the selected matching window.

Expected behavior: identical documents show high overlap; unrelated documents show low or zero overlap; shared passages are highlighted; invalid or empty input produces an error message.

### 11. Advantages
- Easy to use through a web browser.
- Demonstrates hashing and string matching.
- Highlights exact matching passages.
- Does not require an external service or database.
- Supports pasted text and text-file uploads.

### 12. Limitations
It does not search online sources and may miss paraphrased content. Exact matching can also identify common phrases or quotations. Human review is required before drawing conclusions.

### 13. Future enhancements
PDF/DOCX upload, semantic matching, multiple-document comparison, database storage, downloadable reports, and user authentication.

### 14. Conclusion
The Plagiarism Detection Tool demonstrates how rolling hashing and string matching can be combined in a practical Python web application. It helps users locate exact text overlap and understand the result through a visual report.

### 15. References
- Python documentation: https://docs.python.org/3/
- Flask documentation: https://flask.palletsprojects.com/
- Rabin–Karp string-search algorithm: https://en.wikipedia.org/wiki/Rabin%E2%80%93Karp_algorithm
