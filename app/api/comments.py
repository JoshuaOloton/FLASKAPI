from urllib import request
from flask import jsonify, current_app, url_for
from flask_login import current_user
from app import db
from app.api import api
from app.models import Comment, Permission
from app.api.decorators import permission_required
from app.api.errors import forbidden

@api.route('/comments')
def get_comments():
    page = request.args.get('page',1)
    pagination = Comment.query.paginate(
        page,per_page=current_app.config['POSTS_PER_PAGE'],error_out=False)
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
    if not current_user != comment.author and \
        not current_user.has_permissions(Permission.ADMIN):
        return forbidden('Insufficient permissions')
    
    db.session.commit()

