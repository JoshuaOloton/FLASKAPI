from urllib import request, response
from flask import render_template,jsonify
from app.main import main


@main.app_errorhandler(404)
def error_404(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error':'unauthorized'})
        return response
    return render_template('errors/404.html'), 404

    
@main.app_errorhandler(500)
def error_500(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error':'server error'})
        return response({'error':'forbidden'})
    return render_template('errors/500.html'), 500

