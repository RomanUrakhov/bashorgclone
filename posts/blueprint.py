from flask import Blueprint, render_template

from models import Post

from flask import request
from posts.forms import PostForm
from app import db
import config

from flask import redirect
from flask import url_for

import re
from jinja2 import evalcontextfilter, Markup, escape

# первый параметр -- имя блюпринта, в app.py -- регистрация этого изолированного куска(блюпринта)
posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
def post_add():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        post = Post(title=title, body=body)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.index'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form)


@posts.errorhandler(500)
def page_not_found(e):
    return render_template('error.html', error=e), 500


@posts.route('/<slug>/edit/', methods=['POST', 'GET'])
def edit_post(slug):
    post = Post.query.filter(Post.slug == slug).first()

    if request.method == 'POST':
        # Если у объекта, который присваивается в obj есть атрибуты, соответствующие
        # атрибутам формы, то они подставляются (поля title и body)
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()

        return redirect(url_for('posts.post_detail', slug=post.slug))

    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', post=post, form=form)


@posts.route('/')
def index():
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    posts_list = Post.query.order_by(Post.date.desc())
    pages = posts_list.paginate(page, config.Configuration.POSTS_PER_PAGE)

    return render_template('posts/post.html', pages=pages)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()

    if post is not None:
        return render_template('posts/detail.html', post=post)

    return redirect(url_for('posts.index'))


@posts.route('/search')
@posts.route('/search/<int:page>')
def post_search(page=1):
    query = request.args.get('text')
    if query:
        posts_list = Post.query.filter(Post.body.contains(query))
        if posts_list.all():
            pages = posts_list.paginate(page, config.Configuration.POSTS_PER_PAGE)
            return render_template('search.html', coolstories=posts_list, pages=pages, q=query)
        else:
            return render_template('search.html', messgae=query)

    return render_template('search.html')


_paragraph_re = re.compile(r'(?:\r\n|\r(?!\n)|\n){2,}')


@posts.app_template_filter('nl2br')
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n')
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result
