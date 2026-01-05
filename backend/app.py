from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conn = psycopg2.connect(
    host="localhost",
    database="inventario",
    user="inventario_user",
    password="1234"
)
cursor = conn.cursor()

# =========================
# CREAR TABLA
# =========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    cantidad INTEGER,
    precio NUMERIC
)
""")
conn.commit()

# =========================
# LISTAR PRODUCTOS
# =========================
@app.route("/productos", methods=["GET"])
def listar_productos():
    cursor.execute("SELECT id, nombre, cantidad, precio FROM productos")
    productos = cursor.fetchall()

    data = []
    for p in productos:
        data.append({
            "id": p[0],
            "nombre": p[1],
            "cantidad": p[2],
            "precio": float(p[3])
        })
    return jsonify(data)

# =========================
# AGREGAR PRODUCTO
# =========================
@app.route("/productos", methods=["POST"])
def agregar_producto():
    data = request.json
    cursor.execute(
        "INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s)",
        (data["nombre"], data["cantidad"], data["precio"])
    )
    conn.commit()
    return jsonify({"mensaje": "Producto agregado"})

# =========================
# OBTENER PRODUCTO
# =========================
@app.route("/productos/<int:id>", methods=["GET"])
def obtener_producto(id):
    cursor.execute(
        "SELECT id, nombre, cantidad, precio FROM productos WHERE id=%s",
        (id,)
    )
    p = cursor.fetchone()
    if not p:
        return jsonify({"error": "No encontrado"}), 404

    return jsonify({
        "id": p[0],
        "nombre": p[1],
        "cantidad": p[2],
        "precio": float(p[3])
    })

# =========================
# ACTUALIZAR PRODUCTO
# =========================
@app.route("/productos/<int:id>", methods=["PUT"])
def actualizar_producto(id):
    data = request.json
    cursor.execute("""
        UPDATE productos
        SET nombre=%s, cantidad=%s, precio=%s
        WHERE id=%s
    """, (data["nombre"], data["cantidad"], data["precio"], id))
    conn.commit()
    return jsonify({"mensaje": "Producto actualizado"})

# =========================
# ELIMINAR PRODUCTO
# =========================
@app.route("/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    cursor.execute("DELETE FROM productos WHERE id=%s", (id,))
    conn.commit()
    return jsonify({"mensaje": "Producto eliminado"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
