from flask import Flask, render_template
from helpers import db as dbhelper

app = Flask(__name__)

@app.route("/")
def home():
    news = dbhelper.get_entries().limit(10)
    return render_template("index.html", news=news)

if __name__ == "__main__":
    app.run(debug=True)
