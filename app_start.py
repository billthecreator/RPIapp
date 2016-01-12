
import time

from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, render_template

appList = [
    {
        "name"  : "First app name",
        "url"   : "/firstApp"
    },
    {
        "name"  : "Second app name",
        "url"   : "/secondApp"
    },
    {
        "name"  : "Third app name",
        "url"   : "/thirdApp"
    },
    {
        "name"  : "Forth app name",
        "url"   : "/fourthApp"
    }
]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", appList)

@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
