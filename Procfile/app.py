from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

KATALOG = {
    "gedruk": {
        "id": "gedruk",
        "nama": "Kostum Gedruk 1 set",
        "deskripsi": "",
        "harga_dasar": 70000,
        "gambar_url": "/static/img/baju.jpeg",
        "tersedia_ukuran": ["XS", "S", "M", "L", "XL", "XXL"],
        "stok": {"XS": 3, "S": 5, "M": 8, "L": 6, "XL": 4, "XXL": 2},
        "kategori": "Gedruk",
    },
    "jawa": {
        "id": "jawa",
        "nama": "Baju Adat Jawa",
        "deskripsi": "Kebaya, beskap, dan jarik khas Jawa Tengah & Yogyakarta",
        "harga_dasar": 100000,
        "gambar_url": "/static/img/jawa.jpg",
        "tersedia_ukuran": ["XS", "S", "M", "L", "XL", "XXL"],
        "stok": {"XS": 3, "S": 5, "M": 8, "L": 6, "XL": 4, "XXL": 2},
        "kategori": "Jawa",
    },
    "bali": {
        "id": "bali",
        "nama": "Baju Adat Bali",
        "deskripsi": "Pakaian adat Bali lengkap dengan udeng dan kamen",
        "harga_dasar": 120000,
        "gambar_url": "/static/img/bali.jpg",
        "tersedia_ukuran": ["S", "M", "L", "XL", "XXL"],
        "stok": {"S": 3, "M": 7, "L": 5, "XL": 4, "XXL": 2},
        "kategori": "Bali",
    },
    "minang": {
        "id": "minang",
        "nama": "Baju Adat Minang",
        "deskripsi": "Pakaian adat Minangkabau yang mewah dengan hiasan songket",
        "harga_dasar": 150000,
        "gambar_url":"/static/img/minang.jpg",
        "tersedia_ukuran": ["XS", "S", "M", "L", "XL", "XXL"],
        "stok": {"XS": 2, "S": 3, "M": 5, "L": 4, "XL": 3, "XXL": 1},
        "kategori": "Minang",
    },
    "topeng": {
        "id": "topeng",
        "nama": "Topeng Gedruk",
        "deskripsi": "",
        "harga_dasar": 25000,
        "gambar_url": "/static/img/topeng.jpeg",
        "tersedia_ukuran": ["S", "M", "L", "XL", "XXL"],
        "stok": {"S": 3, "M": 7, "L": 5, "XL": 4, "XXL": 2},
        "kategori": "Topeng",
    },
    "krincingan": {
        "id": "krincingan",
        "nama": "Krincingan Besar",
        "deskripsi": "",
        "harga_dasar": 50000,
        "gambar_url": "/static/img/krincingan.jpeg",
        "tersedia_ukuran": ["XS", "S", "M", "L", "XL", "XXL"],
        "stok": {"XS": 2, "S": 3, "M": 5, "L": 4, "XL": 3, "XXL": 1},
        "kategori": "Krincingan",
    },
    "kenong": {
        "id": "kenong",
        "nama": "Gamelan Kenong 1 Set",
        "deskripsi": "",
        "harga_dasar": 95000,
        "gambar_url": "/static/img/kenong.jpg",
        "stok": 4,
        "kategori": "Kenong",
    },
    "saron": {
        "id": "saron",
        "nama": "Gamelan Saron",
        "deskripsi": "",
        "harga_dasar": 50000,
        "gambar_url": "/static/img/saron.jpg",
        "stok": 4,
        "kategori": "Saron",
    },
    "gendang": {
        "id": "gendang",
        "nama": "Gendang 1 Set",
        "deskripsi": "",
        "harga_dasar": 150000,
        "gambar_url": "/static/img/gendang.jpg",
        "stok": 4,
        "kategori": "Gendang",
    },
    "gedruk": {
        "id": "gedruk",
        "nama": "Kostum Gedruk 1 set",
        "deskripsi": "",
        "harga_dasar": 70000,
        "gambar_url": "/static/img/baju.jpeg",
        "tersedia_ukuran": ["XS", "S", "M", "L", "XL", "XXL"],
        "stok": {"XS": 3, "S": 5, "M": 8, "L": 6, "XL": 4, "XXL": 2},
        "kategori": "Gedruk",
    }
}

PAKET_BUNDLING = {
    "paket_gedruk": {
        "id": "paket_gedruk",
        "nama": "Paket Gedruk",
        "deskripsi": "",
        "harga": 100000,
        "durasi": "24 jam",
        "isi": ["Kostum Gedruk 1 set", "Topeng", "Krincingan"],
        "badge": "Populer"
    }
}

NOMOR_WA = "6285600445602"  

@app.route("/")
def index():
    return render_template("index.html",
                           katalog=KATALOG,
                           paket=PAKET_BUNDLING,
                           nomor_wa=NOMOR_WA)

@app.route("/api/katalog")
def api_katalog():
    return jsonify(list(KATALOG.values()))

@app.route("/api/baju/<baju_id>")
def api_baju_detail(baju_id):
    baju = KATALOG.get(baju_id)
    if not baju:
        return jsonify({"error": "Kostum tidak ditemukan"}), 404
    return jsonify(baju)

@app.route("/api/estimasi-harga", methods=["POST"])
def estimasi_harga():
    data = request.get_json()
    baju_id = data.get("baju_id")
    durasi_hari = int(data.get("durasi_hari", 1))
    jumlah = int(data.get("jumlah", 1))
    paket_id = data.get("paket_id")

    if paket_id and paket_id in PAKET_BUNDLING:
        paket = PAKET_BUNDLING[paket_id]
        total = paket["harga"]
        return jsonify({
            "tipe": "paket",
            "nama": paket["nama"],
            "harga_satuan": paket["harga"],
            "total": total,
            "rincian": f"Paket {paket['nama']} - {paket['durasi']}"
        })

    if not baju_id or baju_id not in KATALOG:
        return jsonify({"error": "Kostum tidak ditemukan"}), 400

    baju = KATALOG[baju_id]
    harga_dasar = baju["harga_dasar"]

    
    diskon = 0
    if durasi_hari >= 7:
        diskon = 0.20
    elif durasi_hari >= 3:
        diskon = 0.10
    elif jumlah >= 5:
        diskon = 0.15

    harga_setelah_diskon = harga_dasar * (1 - diskon)
    total = harga_setelah_diskon * durasi_hari * jumlah

    return jsonify({
        "tipe": "satuan",
        "nama": baju["nama"],
        "harga_dasar": harga_dasar,
        "harga_per_hari": harga_setelah_diskon,
        "durasi_hari": durasi_hari,
        "jumlah": jumlah,
        "diskon_persen": int(diskon * 100),
        "total": total,
        "rincian": f"Rp{harga_setelah_diskon:,.0f} × {durasi_hari} hari × {jumlah} baju"
    })

@app.route("/api/booking", methods=["POST"])
def booking():
    data = request.get_json()
    nama = data.get("nama", "")
    no_hp = data.get("no_hp", "")
    tanggal_mulai = data.get("tanggal_mulai", "")
    tanggal_selesai = data.get("tanggal_selesai", "")
    baju_id = data.get("baju_id", "")
    ukuran = data.get("ukuran", "")
    catatan = data.get("catatan", "")
    paket_id = data.get("paket_id", "")

    
    if paket_id and paket_id in PAKET_BUNDLING:
        paket = PAKET_BUNDLING[paket_id]
        pesan_wa = f"""Halo, saya ingin memesan:

*PAKET: {paket['nama']}*
Nama: {nama}
No. HP: {no_hp}
Tanggal Mulai: {tanggal_mulai}
Tanggal Selesai: {tanggal_selesai}
Catatan: {catatan if catatan else '-'}

Mohon konfirmasi ketersediaan. Terima kasih!"""
    else:
        baju = KATALOG.get(baju_id, {})
        pesan_wa = f"""Halo, saya ingin menyewa:

*{baju.get('nama', baju_id)}*
Nama: {nama}
No. HP: {no_hp}
Ukuran: {ukuran}
Tanggal Mulai: {tanggal_mulai}
Tanggal Selesai: {tanggal_selesai}
Catatan: {catatan if catatan else '-'}

Mohon konfirmasi ketersediaan. Terima kasih!"""

    import urllib.parse
    wa_link = f"https://wa.me/{NOMOR_WA}?text={urllib.parse.quote(pesan_wa)}"

    return jsonify({
        "success": True,
        "wa_link": wa_link,
        "pesan": "Booking berhasil dibuat! Klik link WA untuk konfirmasi."
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
