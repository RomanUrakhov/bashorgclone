from wtforms import Form, StringField, TextAreaField
# для того, чтобы выстроить соответствие между нашими моделями
# и html формами


class PostForm(Form):
    title = StringField('Заголовок рофляны')
    body = TextAreaField('Текст рофляны')
