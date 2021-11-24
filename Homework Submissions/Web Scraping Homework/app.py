from flask import Flask, render_template, redirect
from scraperHelper import ScraperHelper
from mongoHelper import MongoHelper

app = Flask(__name__)

# global helper classes
mongoHelper = MongoHelper()
scraperHelper = ScraperHelper()

# HTML Renders
@app.route("/")
def index():
    facts = mongoHelper.findLastFacts()
    return render_template("index.html", mars=facts)

# BUTTON Routes
@app.route("/scrape")
def scrapeMars():
    data = scraperHelper.scrapeMars()
    response = mongoHelper.insertFacts(data)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
