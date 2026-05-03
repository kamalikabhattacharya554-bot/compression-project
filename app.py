from flask import Flask, render_template, request, send_file
from algorithms import huffman, shannon_fano
from striprtf.striprtf import rtf_to_text
import time
import io

app = Flask(__name__)

huff_data = ""
shan_data = ""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    global huff_data, shan_data

    text = ""

    # 📂 FILE INPUT
    if "file" in request.files:
        file = request.files["file"]
        if file and file.filename != "":
            content = file.read().decode("utf-8")
            if file.filename.endswith(".rtf"):
                text = rtf_to_text(content)
            else:
                text = content

    # ✍️ TEXT INPUT
    if text.strip() == "":
        text = request.form.get("text", "")

    if text.strip() == "":
        return render_template("index.html", error="Enter text or upload file")

    # 🔥 HUFFMAN
    start = time.time()
    huff_encoded, huff_codes, huff_root = huffman.compress(text)
    huff_decoded = huffman.decompress(huff_encoded, huff_root)
    huff_time = round(time.time() - start, 5)

    # 🔥 SHANNON
    start = time.time()
    shan_encoded, shan_codes = shannon_fano.compress(text)
    shan_decoded = shannon_fano.decompress(shan_encoded, shan_codes)
    shan_time = round(time.time() - start, 5)

    # Save for download
    huff_data = huff_encoded
    shan_data = shan_encoded

    # 📊 RATIOS
    original_bits = len(text) * 8
    huff_ratio = round(len(huff_encoded) / original_bits, 3)
    shan_ratio = round(len(shan_encoded) / original_bits, 3)

    return render_template(
        "index.html",
        original=text,

        huff_encoded=huff_encoded,
        huff_decoded=huff_decoded,
        huff_ratio=huff_ratio,
        huff_codes=huff_codes,
        huff_time=huff_time,

        shan_encoded=shan_encoded,
        shan_decoded=shan_decoded,
        shan_ratio=shan_ratio,
        shan_codes=shan_codes,
        shan_time=shan_time
    )


# 📥 DOWNLOAD ROUTES
@app.route("/download/huffman")
def download_huffman():
    return send_file(io.BytesIO(huff_data.encode()),
                     as_attachment=True,
                     download_name="huffman.txt",
                     mimetype="text/plain")


@app.route("/download/shannon")
def download_shannon():
    return send_file(io.BytesIO(shan_data.encode()),
                     as_attachment=True,
                     download_name="shannon.txt",
                     mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True)