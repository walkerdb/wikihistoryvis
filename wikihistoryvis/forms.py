from flask.ext.wtf import Form
from wtforms import validators, StringField, DateField


class WikiUserForm(Form):
    def generate_csrf_token(self, csrf_context=None):
        super().generate_csrf_token(csrf_context)

    user_name = StringField("username", validators=[
        validators.DataRequired(message="You need to enter a username!")
    ])


class WikiArticleForm(Form):
    def generate_csrf_token(self, csrf_context=None):
        super().generate_csrf_token(csrf_context)

    article_name = StringField("Article Name", validators=[
        validators.DataRequired(message="You need to enter an article name!")
    ])


class DateFacetForm(Form):
    def generate_csrf_token(self, csrf_context=None):
        super().generate_csrf_token(csrf_context)

    start_date = DateField("start date")
    end_date = DateField("end date")
