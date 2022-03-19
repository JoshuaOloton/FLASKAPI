import json
from flask import jsonify, current_app, url_for, g, request
from flask_login import current_user
from app import db
from app.api import api
from app.models import Comment, Permission, Post
from app.api.decorators import permission_required
from app.api.errors import forbidden

@api.route('/comments/<int:id>')
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())

@api.route('/comments/')
def get_comments():
    page = request.args.get('page',1,type=int)
    pagination = Comment.query.order_by(Comment.date_created.desc()).paginate(
        page,per_page=current_app.config['COMMENTS_PER_PAGE'],error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_comments',page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_comments',page=page+1)
    return jsonify({
        'comments':[comment.to_json() for comment in comments],
        'prev':prev,
        'next':next,
        'count':pagination.total
    })

@api.route('/comments/<int:id>',methods=['PUT'])
@permission_required(Permission.WRITE)
def edit_comments(id):
    comment = Comment.query.get_or_404(id)
    if g.current_user != comment.author and not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    comment.body = request.json.get('body',comment.body)
    db.session.commit()
    return jsonify(comment.to_json())

@api.route('/posts/<int:id>/comments/',methods=['POST'])
@permission_required(Permission.WRITE)
def new_comment(id):
    post = Post.query.get_or_404(id)
    comment = Comment.from_json(request.json)
    comment.author = g.current_user
    comment.post = post
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_json()), 201, \
        {'location':url_for('api.get_comment',id=comment.id)}

@api.route('/posts/<int:id>/comments/')
def get_post_comments(id):
    post = Post.query.get_or_404(id)
    page = request.args.get('page',1)
    pagination = post.comments.order_by(Comment.date_created.desc()).paginate(
        page,per_page=current_app.config['COMMENTS_PER_PAGE'], error_out = False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_comment',page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_comment',page=page+1)
    return jsonify({
        'comments': [comment.to_json() for comment in comments],
        'prev_url': prev,
        'next_url': next,
        'count': pagination.total
    })

@api.route('/posts/<int:id>/comments/',methods=['DELETE'])
@permission_required(Permission.WRITE)
def delete_comment(id):
    comment = Comment.query.get_or_404(1336)
    if comment.author != g.current_user and not g.current_user.can(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message':'comment successfully deleted'})