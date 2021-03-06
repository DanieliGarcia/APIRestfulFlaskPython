#!flask/bin/python
from flask import Flask, jsonify, request
from cliente import Client
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)
app.config["MONGO_URI"] = \
    "mongodb://172.18.0.35:27017/DBdani"
mongo  =PyMongo(app)


#listClient=[
   # Client(name="Danieli", email="danieli@teste.com.br", phone="992921010"),
  #  Client(name="Steffany", email="steffany@teste.com.br", phone="992921515"),
 #   Client(name="Thafila", email="thafila@teste.com.br", phone="992922020"),
#    Client(name="Guilherme", email="guilherme@teste.com.br", phone="992921010"),

#]

@app.route('/api/v1.0/clients', methods=['GET'])
def get_tasks():
    clients = []
    for c in mongo.db.cliente.find():
        newCliente = Client()
        newCliente.id = str(c['_id'])
        newCliente.name = (c['_name'])
        newCliente.phone = (c['_phone'])
        newCliente.email = (c['_email'])
        clients.append(newCliente)
    return jsonify([c.__dict__ for c in clients]), 201



@app.route('/api/v1.0/clients', methods=['POST'])
def create_client():
    newcli = Client()
    newcli.id = ObjectId()
    newcli.name = request.json ['name']
    newcli.phone = request.json ['email']
    newcli.email = request.json ['phone']


    ret = mongo.db.clients.\
        insert_one(newcli.__dict__). inserted_id
    return jsonify({'id': str(ret)}), 201



@app.route('/api/v1.0/clients/<string:_id>', methods=['PUT'])
def update_client(_id):
    updatecli = Client()
    updatecli._id = ObjectId(_id)
    updatecli.name = request.json ['name']
    updatecli.phone = request.json ['phone']
    updatecli.email = request.json ['email']

    mongo.db.clients.update_one({'_id':updatecli._id},{'$set':updatecli.__dict__},                        upsert=False)
    return jsonify({'id':str (updatecli._id)}), 201


@app.route('/api/v1.0/clients/<string:_id>', methods=['DELETE'])
def delete_client(_id):
        _id = ObjectId(_id)
        ret = mongo.db.clients.delete_one({'_id':_id}).deleted_count
        return jsonify({'delete_count':str(ret)}),201



#@app.route('/api/v1.0/client', methods=['GET'])
#def get_tasks():
 #   return jsonify({'clients':[umcli.__dict__ for umcli in listClient]})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
