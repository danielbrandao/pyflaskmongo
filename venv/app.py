from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.veiculos
carros_collection = db.carros

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add")
def add():
    return render_template("/add.html")

@app.route('/carros', methods=['POST'])
def inserir_carro():
    carro = {
        'marca': request.form['marca'],
        'modelo': request.form['modelo'],
        'ano': int(request.form['ano']),
        'preco': float(request.form['preco']),
        'categoria': request.form['categoria'],
        'combustivel': request.form['combustivel'],
        'cambio': request.form['cambio']
    }
    carros_collection.insert_one(carro)
    return redirect('/carros')


@app.route('/carros', methods=['GET'])
def listar_carros():
    carros = list(carros_collection.find())
    return render_template('list.html', carros=carros)


@app.route('/carros/<id>', methods=['GET'])
def obter_carro(id):
    carro = carros_collection.find_one({'_id': id})
    return render_template('view.html', carro=carro)


@app.route('/carros/<id>', methods=['PUT'])
def atualizar_carro(id):
    carro_atualizado = {
        'marca': request.form['marca'],
        'modelo': request.form['modelo'],
        'ano': int(request.form['ano']),
        'preco': float(request.form['preco']),
        'categoria': request.form['categoria'],
        'combustivel': request.form['combustivel'],
        'cambio': request.form['cambio']
    }
    carros_collection.update_one({'_id': id}, {'$set': carro_atualizado})
    return redirect('/carros')


@app.route('/carros/<id>', methods=['DELETE'])
def deletar_carro(id):
    carros_collection.delete_one({'_id': id})
    return redirect('/carros')


if __name__ == '__main__':
    app.run(debug=True)
