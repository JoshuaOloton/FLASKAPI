from flask_httpauth import HTTPBasicAuth
from flask_login import current_user
from app.models import User,Post,Comment
from app.api.errors import unauthorized, forbidden
from app.api import api
from flask import jsonify

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email,password):
    if email == '':
        return False
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)

@auth.route('/tokens')
def get_token():
    if not current_user.is_anonymous and not current_user.token_used:
        return jsonify({'token':current_user.generate_auth_token(expiration=3600),'expiration':3600})

@api.before_app_request
@auth.login_required
def before_request():
    if not current_user.anonymous and not current_user.confirmed:
        return forbidden('Unconfirmed Account')

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

    
