from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB total request size
ALLOWED_EXTENSIONS = {"txt"}
BASE = 257
MOD = 1_000_000_007


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def read_document(text_field, uploaded_file, label):
    """Use pasted text first; otherwise read an uploaded UTF-8 .txt file."""
    if uploaded_file and uploaded_file.filename:
        if not allowed_file(uploaded_file.filename):
            raise ValueError(f"{label}: only .txt files are supported.")
        raw = uploaded_file.read()
        if len(raw) > 1_000_000:
            raise ValueError(f"{label}: file is larger than 1 MB.")
        try:
            return raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise ValueError(f"{label}: file must be saved as UTF-8 text.")
    return text_field or ""


def tokenize(text):
    """Normalize to lowercase word tokens; punctuation is ignored."""
    return re.findall(r"[a-z0-9]+(?:'[a-z0-9]+)?", text.lower())


def rolling_hash(tokens, size):
    """Yield (start_position, polynomial_hash) for each token window."""
    if len(tokens) < size:
        return

    # Hash each token to an integer, then hash the token sequence.
    values = [sum((i + 1) * ord(ch) for i, ch in enumerate(token)) % MOD
              for token in tokens]
    highest_power = pow(BASE, size - 1, MOD)

    current = 0
    for value in values[:size]:
        current = (current * BASE + value) % MOD
    yield 0, current

    for start in range(1, len(values) - size + 1):
        outgoing = values[start - 1]
        incoming = values[start + size - 1]
        current = (current - outgoing * highest_power) % MOD
        current = (current * BASE + incoming) % MOD
        yield start, current


def find_matching_segments(tokens_a, tokens_b, shingle_size=3):
    """
    Rabin-Karp style rolling-hash search.
    Hash matches are always verified against the original token sequences,
    preventing hash collisions from being reported as plagiarism.
    """
    if not tokens_a or not tokens_b:
        return [], set(), set(), 0

    size = min(shingle_size, len(tokens_a), len(tokens_b))
    index = {}
    for pos, value in rolling_hash(tokens_a, size):
        index.setdefault(value, []).append(pos)

    candidate_pairs = []
    for pos_b, value in rolling_hash(tokens_b, size):
        for pos_a in index.get(value, []):
            if tokens_a[pos_a:pos_a + size] == tokens_b[pos_b:pos_b + size]:
                candidate_pairs.append((pos_a, pos_b))

    # Extend every verified seed to the full matching run on its diagonal.
    runs = {}
    for pos_a, pos_b in candidate_pairs:
        start_a, start_b = pos_a, pos_b
        while (start_a > 0 and start_b > 0 and
               tokens_a[start_a - 1] == tokens_b[start_b - 1]):
            start_a -= 1
            start_b -= 1

        end_a, end_b = pos_a + size, pos_b + size
        while (end_a < len(tokens_a) and end_b < len(tokens_b) and
               tokens_a[end_a] == tokens_b[end_b]):
            end_a += 1
            end_b += 1

        key = (start_a, start_b)
        runs[key] = max(runs.get(key, 0), end_a - start_a)

    # Remove runs fully contained in another run on the same diagonal.
    segments = []
    for (start_a, start_b), length in runs.items():
        if length >= size:
            segments.append({
                "start_a": start_a, "start_b": start_b, "length": length,
                "text": " ".join(tokens_b[start_b:start_b + length])
            })
    segments.sort(key=lambda item: (item["start_b"], -item["length"]))

    covered_a, covered_b = set(), set()
    for segment in segments:
        covered_a.update(range(segment["start_a"], segment["start_a"] + segment["length"]))
        covered_b.update(range(segment["start_b"], segment["start_b"] + segment["length"]))

    # Unique display snippets: avoid repeating identical text in the report.
    unique_segments = []
    seen_text = set()
    for segment in segments:
        if segment["text"] not in seen_text:
            unique_segments.append(segment)
            seen_text.add(segment["text"])

    return unique_segments, covered_a, covered_b, size


def highlight_tokens(tokens, covered):
    """Return safe text pieces with a flag for HTML highlighting."""
    return [{"word": word, "matched": i in covered} for i, word in enumerate(tokens)]


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    doc1_text = ""
    doc2_text = ""
    shingle_size = 3

    if request.method == "POST":
        doc1_text = request.form.get("doc1_text", "")
        doc2_text = request.form.get("doc2_text", "")
        try:
            shingle_size = int(request.form.get("shingle_size", "3"))
            if not 1 <= shingle_size <= 10:
                raise ValueError("Matching window must be between 1 and 10 words.")

            doc1_text = read_document(
                doc1_text, request.files.get("doc1_file"), "Document 1"
            )
            doc2_text = read_document(
                doc2_text, request.files.get("doc2_file"), "Document 2"
            )
            if not doc1_text.strip() or not doc2_text.strip():
                raise ValueError("Please provide text or upload a .txt file for both documents.")

            tokens_a = tokenize(doc1_text)
            tokens_b = tokenize(doc2_text)
            if not tokens_a or not tokens_b:
                raise ValueError("Both documents must contain at least one word.")

            segments, covered_a, covered_b, used_size = find_matching_segments(
                tokens_a, tokens_b, shingle_size
            )
            matched_a = len(covered_a)
            matched_b = len(covered_b)
            similarity = (matched_b / max(len(tokens_a), len(tokens_b))) * 100
            coverage_a = (matched_a / len(tokens_a)) * 100
            coverage_b = (matched_b / len(tokens_b)) * 100

            if similarity >= 40:
                status = "High text overlap"
                status_class = "high"
            elif similarity >= 15:
                status = "Moderate text overlap"
                status_class = "medium"
            else:
                status = "Low text overlap"
                status_class = "low"

            result = {
                "similarity": round(similarity, 1),
                "coverage_a": round(coverage_a, 1),
                "coverage_b": round(coverage_b, 1),
                "matched_a": matched_a,
                "matched_b": matched_b,
                "total_a": len(tokens_a),
                "total_b": len(tokens_b),
                "segments": segments,
                "highlight_a": highlight_tokens(tokens_a, covered_a),
                "highlight_b": highlight_tokens(tokens_b, covered_b),
                "status": status,
                "status_class": status_class,
                "window": used_size,
            }
        except (ValueError, TypeError) as exc:
            error = str(exc)

    return render_template(
        "index.html", result=result, error=error,
        doc1_text=doc1_text, doc2_text=doc2_text,
        shingle_size=shingle_size
    )


if __name__ == "__main__":
    app.run(debug=True)
