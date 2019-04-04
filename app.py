from flask import Flask, render_template
from flask_restful import Api, Resource

from resources.item import ItemList, ItemBuy

app = Flask(__name__)

app.secret_key = 'kant'
api = Api(app)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

api.add_resource(ItemList, '/items')
api.add_resource(ItemBuy, '/buy')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
