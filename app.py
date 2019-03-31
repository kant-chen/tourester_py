from flask import Flask
from flask_restful import Api
#from flask_jwt import JWT

#from security import authenticate, identity
from resources.item import ItemList, ItemBuy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'kant'
api = Api(app)


#@app.before_first_request
#def create_tables():
#    db.create_all()


#jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(ItemList, '/items')
api.add_resource(ItemBuy, '/buy')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
