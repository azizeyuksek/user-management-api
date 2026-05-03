from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


@app.route("/users", methods=["GET"]) # VERİ GETİRİR
def get_users():
    conn= sqlite3.connect("users.db")
    cursor= conn.cursor()

    cursor.execute("SELECT * FROM users")
    rows=cursor.fetchall()

    users=[]

    for row in rows:
        users.append({
            "id":row[0],
            "name":row[1]
        })

    conn.close()
    return jsonify(users), 200

@app.route("/users", methods=["POST"])
def post_users():
    data = request.json

    if not data or "id" not in data or "name" not in data:
        return jsonify({"error": "Eksik veri"}), 400

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (id, name) VALUES (?, ?)",
            (data["id"], data["name"])
        )
        conn.commit()

        return jsonify({
            "message": "Kullanıcı eklendi",
            "data": data
        }), 201

    except:
        return jsonify({"error": "Bu ID zaten var"}), 400

    finally:
        conn.close()


@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json

    if not data or "name" not in data:
        return jsonify({"error": "Eksik veri"}), 400

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET name = ? WHERE id = ?",
        (data["name"], id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Kullanıcı bulunamadı"}), 404

    conn.close()

    return jsonify({
        "message": "Kullanıcı güncellendi",
        "data": {
            "id": id,
            "name": data["name"]
        }
    }), 200
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"error": "Kullanıcı bulunamadı"}), 404

    conn.close()

    return jsonify({
        "message": "Kullanıcı silindi",
        "deleted_id": id
    }), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)


    # EN ÖNEMLİ STATUS CODELERİ # 

    # 200 ---> ok , başarılı
    # 201 ---> oluşturuldu (POST sonrası)
    # 400 ---> kötü istek(eksik veri)
    # 404 ---> bulunamadı 
    # 500 ---> server hatası

     # jsonify veriyi JSON formatına çevirir.
     # request.json  kullanıcının gönderdiği JSON veriyi alır. Python sözlüğüne döndürür.