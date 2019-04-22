from flask import Blueprint, render_template

from models import Post, Tag

from flask import request

# первый параметр -- имя блюпринта, в app.py -- регистрация этого изолированного куска(блюпринта)
posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/')
def index():
    posts_list = Post.query.all()
    return render_template('posts/post.html', coolstory=posts_list)


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
