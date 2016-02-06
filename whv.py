import datetime
import requests
from chronyk import Chronyk
from flask import Flask, render_template, request, redirect, url_for
from wikihistoryvis import article_revision_parser, user_revision_parser, recent_changes_parser
from wikihistoryvis.forms import WikiArticleForm, WikiUserForm, DateFacetForm

app = Flask(__name__)
app.config.update(WTF_CSRF_ENABLED=True,
                  SECRET_KEY="lol")


@app.route('/', methods=["GET", "POST"])
def index():
    newest_date, oldest_date = get_dates_from_request(default_days_before_today=7)

    address = "http://si410wiki.sites.uofmhosting.net/api.php?" \
              "action=query&" \
              "list=recentchanges&" \
              "rcprop=title|ids|sizes|flags|user|timestamp|comment&" \
              "rclimit=1000&" \
              "rctype=edit|external|new&" \
              "rcstart={}&" \
              "rcend={}&" \
              "format=json".format(newest_date.datetime().strftime("%Y%m%d%H%M%S"), oldest_date.datetime().strftime("%Y%m%d000000"))

    data = requests.get(address).json()['query']['recentchanges']
    parser = recent_changes_parser.Parser(data, oldest_date, newest_date)
    # pprint(data)
    # print(len(data))

    article_form = WikiArticleForm()
    user_form = WikiUserForm()
    dates_form = DateFacetForm()

    if request.method == "POST":
        if not article_form.article_name.errors and article_form.article_name.data:
            return redirect(url_for("show_article_summary", article=article_form.article_name.data))
        elif not user_form.errors and user_form.user_name.data:
            return redirect(url_for("show_user_summary", username=user_form.user_name.data))
    else:
        return render_template("index.html", article_form=article_form, user_form=user_form, dates_form=dates_form, parser=parser)


@app.route('/user/<username>', methods=["GET", "POST"])
def show_user_summary(username):
    newest_date, oldest_date = get_dates_from_request(default_days_before_today=3000)

    address = "http://si410wiki.sites.uofmhosting.net/api.php?" \
              "action=query&" \
              "list=usercontribs&" \
              "uclimit=500&" \
              "ucprop=ids|title|timestamp|comment|sizediff|flags&" \
              "format=json&" \
              "ucstart={}&" \
              "ucend={}&" \
              "ucuser={}".format(newest_date.datetime().strftime("%Y%m%d%H%M%S"), oldest_date.datetime().strftime("%Y%m%d000000"), username)

    data = requests.get(address).json()['query']['usercontribs']
    # pprint(data)

    parser = user_revision_parser.Parser(data, username, oldest_date, newest_date)

    form = WikiUserForm()
    dates_form = DateFacetForm()

    if request.method == "POST" and not form.user_name.errors:
        return redirect(url_for("show_user_summary", username=form.user_name.data))

    return render_template("user_summary.html", parser=parser, form=form, dates_form=dates_form)


@app.route('/article/<article>', methods=["GET", "POST"])
def show_article_summary(article):
    newest_date, oldest_date = get_dates_from_request(default_days_before_today=3000)

    address = "http://si410wiki.sites.uofmhosting.net/api.php?" \
              "action=query&" \
              "prop=revisions&" \
              "rvlimit=max&" \
              "rvprop=ids|flags|timestamp|comment|user|userid|size&" \
              "format=json&" \
              "rvstart={}&" \
              "rvend={}&" \
              "titles={}".format(newest_date.datetime().strftime("%Y%m%d%H%M%S"), oldest_date.datetime().strftime("%Y%m%d000000"), article)

    data = requests.get(address).json()
    parser = article_revision_parser.Parser(data, article, oldest_date, newest_date)

    form = WikiArticleForm()
    dates_form = DateFacetForm()

    if request.method == "POST" and not form.article_name.errors:
        return redirect(url_for("show_article_summary", article=form.article_name.data))

    return render_template("article_summary.html", parser=parser, form=form, dates_form=dates_form)


def get_dates_from_request(default_days_before_today):
    oldest_date = request.args.get('start_date', '')
    oldest_date = Chronyk(oldest_date) if oldest_date else Chronyk(datetime.datetime.now() - datetime.timedelta(days=default_days_before_today))
    newest_date = request.args.get('end_date', '')
    newest_date = Chronyk(newest_date) if newest_date else Chronyk(datetime.datetime.now())
    return newest_date, oldest_date


if __name__ == '__main__':
    app.run(debug=True)

    # All recent changes:
    # http://si410wiki.sites.uofmhosting.net/api.php?
    #     action=query&
    #     list=recentchanges&
    #     rcprop=title|ids|sizes|flags|user|timestamp&
    #     rclimit=1000&
    #     format=json

    # All page revisions:
    # http://si410wiki.sites.uofmhosting.net/api.php?
    # action=query&
    # prop=revisions&
    # titles=Internet_Archive&
    # rvlimit=max&
    # rvprop=ids|flags|timestamp|comment|user|userid|size&
    # format=json
