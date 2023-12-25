
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
        product_name = request.form["product_name"].replace(" ","")
        try:
            # flipkart url along with search keywords
            flipkart_url = "https://www.flipkart.com/search?q="+product_name
            # trying to hit on url using urllib
            u_client = uo(flipkart_url)
            #reading the html page
            required_flipkart_page = u_client.read()
            # urllib client closed
            u_client.close()
            flipkart_html_dataset = bs(required_flipkart_page,"html.parser") # beautified the html scrap using beautiful soup
            bigboxes = flipkart_html_dataset.find_all("div", {"class":"_1AtVbE col-12-12"}) # locating the product link
            del bigboxes[0:3]
            box = bigboxes[0]
            productlink = "https://www.flipkart.com"+box.div.div.div.a['href']
            product_request = requests.get(productlink)
            u_client = uo(productlink)
            productData = u_client.read()
            productData = bs(productData, "html.parser")
            product_bigbox = productData.find_all("div", {"class":"_16PBlm"})
            
            reviews = []
            for elements in product_bigbox:
                try:
                    # extracting rating from reviews
                    rating = elements.div.div.div.div.text
                
                except:
                    rating = "NO RATING FOUND"
                    
                try:
                    # extracting name from reviews
                    name = elements.div.div.find_all("p", {"class" : "_2sc7ZR _2V5EHH"})[0].text
                
                except:
                    name = "NO NAME FOUND"   
                    
                try:
                    # extracting actual review from reviews
                    review = elements.div.div.find_all("div", {"class" : ""})[0].div.text
                
                except:
                    review = "NO REVIEW FOUND"
            
                collection = {"Name" : name,
                              "Rating" : rating,
                              "Review" : review}
                reviews.append(collection)
        
        except Exception as e:
            return f"FATAL ERROR! I DON'T KNOW WHAT TO DO! ERROR INFO: {e}"
        
        return render_template("result.html", reviews = reviews[0:len(reviews)-1])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000)