from flask import Flask

app = Flask("NewsScrapper")


@app.route("/")
def home():
    return "서당캣 해커 늬우스"


app.run(host="127.0.0.1")
