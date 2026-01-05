from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)
API_URL = "http://localhost:5000"

@app.route("/")
def index():
    productos = requests.get(f"{API_URL}/productos").json()
    return render_template("index.html", productos=productos)

@app.route("/agregar", methods=["POST"])
def agregar():
    data = {
        "nombre": request.form["nombre"],
        "cantidad": int(request.form["cantidad"]),
        "precio": float(request.form["precio"])
    }
    requests.post(f"{API_URL}/productos", json=data)
    return redirect("/")

@app.route("/eliminar/<int:id>")
def eliminar(id):
    requests.delete(f"{API_URL}/productos/{id}")
    return redirect("/")

if __name__ == "__main__":
    app.run(port=8080, debug=False)
