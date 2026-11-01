# Sample test files

Use these pairs to test the Plagiarism Detection Tool:

1. `sample_01_original.txt` + `sample_02_high_similarity.txt` — substantial shared passage.
2. `sample_01_original.txt` + `sample_03_moderate_similarity.txt` — partial overlap.
3. `sample_04_no_similarity.txt` + `sample_01_original.txt` — unrelated content.
4. `sample_05_identical.txt` + `sample_06_identical_copy.txt` — identical documents.
5. `sample_07_case_and_punctuation.txt` + `sample_08_case_and_punctuation_variant.txt` — case and punctuation normalization.
6. `sample_09_short_text.txt` + `sample_10_unrelated_short_text.txt` — short unrelated documents.

In the website, upload one file into Document A and the other into Document B.
The current application accepts UTF-8 `.txt` files only. For short documents,
set the matching window to 1 or 2 words; the default 3-word window may not
find a match in very short passages.
