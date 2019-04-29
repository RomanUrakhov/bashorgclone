from flask import Blueprint, render_template

from models import Post, Tag

from flask import request
from posts.forms import PostForm
from app import db

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


@posts.route('/')
def index():
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    posts_list = Post.query.order_by(Post.date.desc())
    pages = posts_list.paginate(page=page, per_page=2)

    return render_template('posts/post.html', pages=pages)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first()
    tags = post.tags
    return render_template('posts/detail.html', coolstory=post, tags=tags)


@posts.route('/tag/<slug>')
def posts_by_tag(slug):
    tag = Tag.query.filter(Tag.slug == slug).first()
    posts_list = tag.relevant_posts.all()
    return render_template('posts/topics.html', tag=tag, coolstories=posts_list)


@posts.route('/search')
def post_search():
    query = request.args.get('text')
    if query:
        posts_list = Post.query.filter(Post.body.contains(query)).all()

    else:
        posts_list = ''
    return render_template('search.html', coolstories=posts_list)


_paragraph_re = re.compile(r'(?:\r\n|\r(?!\n)|\n){2,}')


@posts.app_template_filter('nl2br')
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n')
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result
