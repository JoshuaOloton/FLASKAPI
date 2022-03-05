from flask import jsonify, current_app, request, url_for
from app.api import api, comments
from app.models import User, Post, Comment

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/user/<int:id>/timeline')
def get_user_followed_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page',1)
    pagination = user.followed_posts.paginate(page,per_page=current_app.config['POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_followed_posts',page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_followed_posts',page=page+1)
    return jsonify({
        'posts':[post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/user/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page',1)
    pagination = user.posts.order_by(Post.date_created.desc()).paginate(page,per_page=current_app.config['POSTS_PER_PAGE'],error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_posts',id=user.id,page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_posts',id=user.id,page=page+1)
    return jsonify({
        'posts':[post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
            })

@api.route('/user/<int:id>/comments/')
def get_user_comments(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page',1)
    pagination = user.comments.order_by(Comment.date_created.desc()).paginate(
        page,per_page=current_app.config['POSTS_PER_PAGE'], error_out=False
    )
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_comments',page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_comments',page=page+1)
    return jsonify({
        'user_comments': [comment.to_json() for comment in comments],
        'prev':prev,
        'next':next,
        'count':pagination.total
        })
