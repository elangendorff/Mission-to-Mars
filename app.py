# Import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping  # The `scraping.py` file located in the same directory as this file

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"  # The `mars_app` db should exist prior to running this
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()                 # Get some data from the `mars` collection within the Mongo database (`mars_app`)
    return render_template("index.html", mars=mars) # Use it with the `index.html` file.
                                                    # The left `mars` is the variable that will be referenced in `index.html`.
                                                    # The right `mars` is the variable that was defined on line 14.

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars                # Refers to the `mars` Mongo database collection
    mars_data = scraping.scrape_all()   # `scrape_all()` function in the `scraping.py` file
    mars.update_one(                    # Update the first record…
        {},                             # …whose field matches what's here (empty field `{}` indicates *any* field will match).
        {"$set":mars_data},             # Update it with what's in `mars_data`.
        upsert=True                     # If a document doesn't already exist, create a new one.
    )
    return redirect('/', code=302)      # When finished, go back to `/` with response code 302: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/302

if __name__ == "__main__":
    app.run()
