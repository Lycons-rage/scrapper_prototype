
# required libraries
from flask import Flask, request, render_template, jsonify
from bs4 import BeautifulSoup as bs
import requests
from flask_cors import CORS, cross_origin
from urllib.request import urlopen as uo

app = Flask(__name__)



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7000)