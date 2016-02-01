import json

import requests
from flask import Flask, render_template, request, redirect, url_for

from wikihistoryvis import data_parser
from wikihistoryvis.forms import WikiArticleForm

app = Flask(__name__)
app.config.update(WTF_CSRF_ENABLED=True,
                  SECRET_KEY="lol")


@app.route('/', methods=["GET", "POST"])
def index():
    form = WikiArticleForm()
    if request.method == "POST" and not form.article_name.errors:
        return redirect(url_for("show_article_summary", article=form.article_name.data))
    else:
        return render_template("index.html", form=form)


@app.route('/user/<username>')
def show_user_summary(username):
    return username


@app.route('/article/<article>', methods=["GET", "POST"])
def show_article_summary(article):
    auth_cookies = log_in()


    address = "http://si410wiki.sites.uofmhosting.net/api.php?" \
               "action=query&" \
               "prop=revisions&" \
               "rvlimit=max&" \
               "rvprop=ids|flags|timestamp|comment|user|userid|size&" \
               "format=json&" \
               "titles={}".format(article)

    data = requests.get(address, cookies=auth_cookies).json()
    print(data)
    parser = data_parser.Parser(data)

    return render_template("summary.html", revisions=parser.revisions, title=article)


def log_in():
    with open("wikihistoryvis/login_data.txt", mode="r") as f:
        login_data = json.load(f)

    password = login_data["pass"]
    username = login_data["user"]

    url = "http://si410wiki.sites.uofmhosting.net/api.php?action=login&lgname={}&lgpassword={}&format=json".format(username, password)
    r1 = requests.post(url)
    token = r1.json()['login']['token']
    confirmation_url = "http://si410wiki.sites.uofmhosting.net/api.php?action=login&lgname={}&lgpassword={}&format=json&lgtoken={}".format(username, password, token)
    r2 = requests.post(confirmation_url, cookies=r1.cookies)

    return r2.cookies


if __name__ == '__main__':
    log_in()
    app.run(debug=True)

# All recent changes:
# http://si410wiki.sites.uofmhosting.net/api.php?
    # action=query&
    # list=recentchanges&
    # rcprop=title|ids|sizes|flags|user|timestamp|sizes&
    # rclimit=1000&
    # format=json

# All page revisions:
# http://si410wiki.sites.uofmhosting.net/api.php?
    # action=query&
    # prop=revisions&
    # titles=Internet_Archive&
    # rvlimit=max&
    # rvprop=ids|flags|timestamp|comment|user|userid|size&
    # format=json