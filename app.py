#!/usr/bin/python3

# Imports
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/api', methods=['GET'])
def get_date():
    data = {'message': 'just a little Api test'}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
