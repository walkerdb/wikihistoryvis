from flask.ext.wtf import Form
from wtforms import validators, StringField


class WikiArticleForm(Form):
    def generate_csrf_token(self, csrf_context=None):
        super().generate_csrf_token(csrf_context)

    article_name = StringField("Article Name", validators=[
        validators.DataRequired(message="You need to enter an article name!")
    ])