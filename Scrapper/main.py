
# required libraries
from flask import Flask, request, render_template, jsonify
from bs4 import BeautifulSoup as bs
import requests
from flask_cors import CORS, cross_origin
from urllib.request import urlopen as uo

app = Flask(__name__)


# landing page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# result page
@app.route("/reviews", methods=["GET","POST"])
def reviews():
    if request.method == "POST":
        product_name = request.form["product_name"]
        return product_name

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7000)