
import time

from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack

appList = [
    {
        "name"  : "First app name",
        "desc"  : "Short description about the first app",
        "url"   : "/firstApp",
        "color" : "blue"
    },
    {
        "name"  : "Second app name",
        "desc"  : "Short description about the second app",
        "url"   : "/secondApp",
        "color" : "green"
    },
    {
        "name"  : "Third app name",
        "desc"  : "Short description about the third app",
        "url"   : "/thirdApp",
        "color" : "yellow"
    },
    {
        "name"  : "Forth app name",
        "desc"  : "Short description about the forth app",
        "url"   : "/fourthApp",
        "color" : "red"
    }
]

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", appList=appList)

@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
