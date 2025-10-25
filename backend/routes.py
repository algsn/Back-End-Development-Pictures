from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


data = [
    {
        "id": 1,
        "pic_url": "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Fremont",
        "event_date": "10/10/2030"
    },
    {
        "id": 2,
        "pic_url": "https://images.unsplash.com/photo-1499084732479-de2c02d45fc4",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Fremont",
        "event_date": "10/11/2030"
    },
    {
        "id": 3,
        "pic_url": "https://images.unsplash.com/photo-1473181488821-2d23949a045a",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Fremont",
        "event_date": "10/12/2030"
    },
    {
        "id": 4,
        "pic_url": "https://images.unsplash.com/photo-1503023345310-bd7c1de61c7d",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Fremont",
        "event_date": "10/13/2030"
    },
    {
        "id": 5,
        "pic_url": "https://images.unsplash.com/photo-1516117172878-fd2c41f4a759",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Fremont",
        "event_date": "10/14/2030"
    },
    {
        "id": 6,
        "pic_url": "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Fremont",
        "event_date": "10/15/2030"
    },
    {
        "id": 7,
        "pic_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Fremont",
        "event_date": "10/16/2030"
    },
    {
        "id": 8,
        "pic_url": "https://images.unsplash.com/photo-1493244040629-496f6d136cc3",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Fremont",
        "event_date": "10/17/2030"
    },
    {
        "id": 9,
        "pic_url": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Fremont",
        "event_date": "10/18/2030"
    },
    {
        "id": 10,
        "pic_url": "https://images.unsplash.com/photo-1481349518771-20055b2a7b24",
        "event_country": "United States",
        "event_state": "California",
        "event_city": "Fremont",
        "event_date": "10/19/2030"
    },
]



@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """
    Mengembalikan daftar gambar dalam format JSON.
    """
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Mengembalikan gambar berdasarkan ID"""
    # cari gambar berdasarkan ID
    picture = next((item for item in data if item["id"] == id), None)
    
    if picture:
        return jsonify(picture), 200  # jika ditemukan
    
    # jika tidak ditemukan, kembalikan error 404
    return jsonify({"error": "Picture not found"}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Menambahkan gambar baru ke daftar data"""
    picture = request.get_json()

    # Validasi data request
    if not picture or "id" not in picture:
        return jsonify({"Message": "Missing picture id"}), 400

    # Cek apakah ID sudah ada
    existing = next((item for item in data if item["id"] == picture["id"]), None)
    if existing:
        # Ubah pesan ke bahasa Inggris sesuai ekspektasi test
        return (
            jsonify({"Message": f"picture with id {picture['id']} already present"}),
            302,
        )

    # Jika belum ada, tambahkan ke data
    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Memperbarui data gambar berdasarkan ID"""
    updated_picture = request.get_json()

    # Cari gambar berdasarkan ID
    picture = next((item for item in data if item["id"] == id), None)

    # Jika tidak ditemukan
    if picture is None:
        return jsonify({"message": "picture not found"}), 404

    # Perbarui field gambar dengan data dari request
    picture.update(updated_picture)
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Menghapus gambar berdasarkan ID"""
    # Cari gambar berdasarkan ID
    picture = next((item for item in data if item["id"] == id), None)

    # Jika tidak ditemukan
    if picture is None:
        return jsonify({"message": "picture not found"}), 404

    # Hapus dari daftar
    data.remove(picture)
    # Kembalikan tanpa body (204 No Content)
    return "", 204
