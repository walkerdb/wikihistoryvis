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
    address = "http://si410wiki.sites.uofmhosting.net/api.php?" \
               "action=query&" \
               "prop=revisions&" \
               "rvlimit=max&" \
               "rvprop=ids|flags|timestamp|comment|user|userid|size&" \
               "format=json&" \
               "titles={}".format(article)
    data = requests.get(address)
    parser = data_parser.Parser()
    return article


if __name__ == '__main__':
    app.run()

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