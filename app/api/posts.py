from urllib import request
from flask import jsonify, current_app, request, url_for, g
from flask_login import current_user
from app.api.errors import forbidden
from app.models import Permission, Post, User
from app.api import api
from app.api.decorators import permission_required
from app import db


@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())

@api.route('/posts')
def get_posts():
    page = request.args.get('page',1,type=int)
    pagination = Post.query.paginate(
        page,per_page=current_app.config['POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    if posts.has_next:
        prev = url_for('api.get_posts',page=page-1)
    elif posts.has_prev:
        next = url_for('api.get_posts',page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev_url': prev,
        'next_url': next,
        'count': pagination.total
        })


@api.route('/posts',methods=['POST'])
def new_post():
    post = Post.from_json(request.json())
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())


@api.route('/posts/<int:id>',methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if not g.current_user==post.author and \
        not g.current_user.has_permissions(Permission.ADMIN):
        return forbidden('Insufficient permissions!')
    post.body = request.json.get('body',post.body)
    db.session.commit()
    return jsonify(post.to_json())