from flask import Flask,request,jsonify
from flask_cors import CORS
import model

app = Flask(__name__)
CORS(app) 
@app.route('/music/', methods=['GET'])

def recommend_movies():
    res = model.results(request.args.get('title'))
    # print(res)
    return jsonify(res)

if __name__=='__main__':
    app.run(port = 5000, debug = True)