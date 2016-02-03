import json
from pprint import pprint

import requests
from flask import Flask, render_template, request, redirect, url_for

from wikihistoryvis import article_revision_parser, user_revision_parser
from wikihistoryvis.forms import WikiArticleForm, WikiUserForm

app = Flask(__name__)
app.config.update(WTF_CSRF_ENABLED=True,
                  SECRET_KEY="lol")


@app.route('/', methods=["GET", "POST"])
def index():
    article_form = WikiArticleForm()
    user_form = WikiUserForm()
    if request.method == "POST" and not article_form.article_name.errors and article_form.article_name.data:
        return redirect(url_for("show_article_summary", article=article_form.article_name.data))
    elif request.method == "POST" and not user_form.errors and user_form.user_name.data:
        return redirect(url_for("show_user_summary", username=user_form.user_name.data))
    else:
        return render_template("index.html", article_form=article_form, user_form=user_form)


@app.route('/user/<username>', methods=["GET", "POST"])
def show_user_summary(username):
    address = "http://si410wiki.sites.uofmhosting.net/api.php?" \
              "action=query&" \
              "list=usercontribs&" \
              "uclimit=500&" \
              "format=json&" \
              "ucuser={}".format(username)

    data = requests.get(address).json()['query']['usercontribs']
    pprint(data)

    parser = user_revision_parser.Parser(data, username)

    form = WikiUserForm()
    if request.method == "POST" and not form.user_name.errors:
        return redirect(url_for("show_user_summary", username=form.user_name.data))

    return render_template("user_summary.html", parser=parser, form=form)


@app.route('/article/<article>', methods=["GET", "POST"])
def show_article_summary(article):
    address = "http://si410wiki.sites.uofmhosting.net/api.php?" \
               "action=query&" \
               "prop=revisions&" \
               "rvlimit=max&" \
               "rvprop=ids|flags|timestamp|comment|user|userid|size&" \
               "format=json&" \
               "titles={}".format(article)

    data = requests.get(address).json()
    parser = article_revision_parser.Parser(data)

    form = WikiArticleForm()
    if request.method == "POST" and not form.article_name.errors:
        return redirect(url_for("show_article_summary", article=form.article_name.data))

    return render_template("article_summary.html", parser=parser, form=form)


if __name__ == '__main__':
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