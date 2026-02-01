from flask import Flask, render_template, request, send_file
from processor import process_sched
import tempfile
import os

app = Flask(__name__)

@app.route("/")
def index():
    # Tampilkan halaman upload
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    # Ambil file dari form
    file = request.files.get("file")
    if not file:
        return "File tidak ditemukan", 400

    # Simpan file input sementara
    tmp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    file.save(tmp_input.name)
    tmp_input.close()

    try:
        # Jalankan LOGIKA PYTHON FINAL (di processor.py)
        output_path = process_sched(tmp_input.name)

        # Kirim file hasil ke browser
        return send_file(
            output_path,
            as_attachment=True,
            download_name="hasil_penempatan_posisi_FINAL.xlsx"
        )
    finally:
        # Bersihkan file input sementara
        if os.path.exists(tmp_input.name):
            os.unlink(tmp_input.name)


if __name__ == "__main__":
    # Jalankan web server lokal
    app.run(host="0.0.0.0", port=5000, debug=False)
