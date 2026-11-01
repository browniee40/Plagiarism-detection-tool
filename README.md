# Plagiarism Detection Tool (Python Web Project)

## 1. Project overview
A web-based text comparison application built with Python and Flask. It compares two text documents, detects matching consecutive word sequences, highlights matching words, and reports a similarity score.

## 2. Technologies
- Python 3.9+
- Flask
- HTML5 and CSS3
- Rabin-Karp style rolling hashing
- Exact sequence verification (string matching)

## 3. Requirements
- Python 3.9 or newer
- pip
- A web browser

## 4. Installation and execution
1. Extract the project ZIP.
2. Open a terminal in the `plagiarism_detection_tool` folder.
3. (Recommended) Create a virtual environment:
   - Windows: `py -m venv venv` then `venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv venv` then `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.
7. Paste text into both boxes or upload two UTF-8 `.txt` files, select the matching window, and click **Analyze documents**.

## 5. How the algorithm works
1. **Tokenization:** Text is converted to lowercase word tokens. Punctuation is ignored.
2. **Shingle creation:** Consecutive groups of N words are considered. N is selected in the interface (1–10).
3. **Rolling hash:** A polynomial rolling hash calculates a compact numeric fingerprint for each group. The first document's hashes are stored in a dictionary.
4. **String matching / verification:** Hashes from the second document are looked up. Every possible hash match is verified by comparing the actual token sequences, so hash collisions are not falsely reported.
5. **Passage extension:** Verified matching windows are extended in both directions to identify the full matching run.
6. **Highlighting:** Matching token positions are highlighted in both documents.
7. **Similarity calculation:** `matching token positions in Document B / max(word count A, word count B) × 100`.

## 6. Example
Document A:
`Machine learning helps computers learn from data. Python is popular for machine learning.`

Document B:
`Machine learning helps computers learn from data. Java is another programming language.`

With a 3-word window, the common passage `machine learning helps computers learn from data` is detected.

## 7. Output
The report displays:
- Overall text similarity percentage
- Matching-word counts and coverage for each document
- Number of matching passages
- Matching passage snippets
- Both documents with matching words highlighted
- A print / save report option

## 8. Limitations
- This is a text-overlap demonstration, not a commercial plagiarism service.
- It compares only the two supplied documents; it does not search the internet, books, journals, or institutional databases.
- It detects exact normalized word sequences. Paraphrased text may not be detected.
- Common phrases, quotations, and properly cited text can match.
- Similarity is an indicator for human review, not proof of plagiarism.
- Only UTF-8 `.txt` uploads are supported. PDF and DOCX support can be added as future work.

## 9. Future scope
- PDF and DOCX extraction
- Compare multiple documents
- Semantic similarity for paraphrased content
- Downloadable PDF reports
- User login and report history
- Larger document indexing

## 10. Project conclusion
The project demonstrates practical use of tokenization, hashing, rolling hash, and string matching in a web application. It provides a simple way to identify exact textual overlap between two documents.
