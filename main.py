import requests
from flask import Flask, render_template, request, redirect

base_url = "http://hn.algolia.com/api/v1"


# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api


def make_detail_url(id):
    return f"{base_url}/items/{id}"


db = {}
app = Flask("DayNine")

# popular 혹은 new를 넣으면 해당 리스트를 반환


def popular_or_new(either):
    result = requests.get(either)
    if either == popular:
        db["popular"] = result.json()['hits']
    elif either == new:
        db["new"] = result.json()['hits']
    return db
    # print(db['new']['hits'][0]['title'])


# print(db)
print("시작")
# db = popular_or_new(new)
db = popular_or_new(popular)
db = popular_or_new(new)


@app.route("/")
def home():
    word = request.args.get('order_by')
    if word == None:
        word = 'popular'

    return render_template("index.html", order=['popular', 'new'], dbs=db[word], dbs_len=len(db[word]))


@app.route("/<id>")
def detail(id):
    indexer = dict((p['objectID'], i)
                   for i, p in enumerate(db['popular']))
    index = indexer.get(id, -1)
    title = db['popular'][index]['title']
    points = db['popular'][index]['points']
    author = db['popular'][index]['author']
    url = db['popular'][index]['url']

    comment_url = make_detail_url(id)
    result = requests.get(comment_url)
    comments = result.json()['children']
    return render_template("detail.html", title=title, points=points, author=author, url=url, comments=comments)


app.run(host="127.0.0.1")
