from flask import jsonify, current_app, request, url_for
from app.api import api
from app.models import User, Post

@api.route('/users')
def get_user():
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/user_posts')
def get_user_followed_posts():
    page = request.args.get('page',1)
    users = User.query.paginate(page,per_page=current_app.config['POSTS_PER_PAGE'],error_out=False)
    return jsonify({post.to_json()})


@api.route('/user_posts')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page',1)
    pagination = user.posts.order_by(Post.date_created.desc()).paginate(page,per_page=current_app.config['POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    next = None
    if pagination.has_next():
        next = url_for('api.get_user_posts',id=user.id,page=page+1)
    prev = None
    if pagination.has_prev():
        prev = url_for('api.get_user_posts',id=user.id,page=page-1)
    return jsonify({
        'posts':[post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
            })