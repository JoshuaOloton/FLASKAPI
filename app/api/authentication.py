from flask_httpauth import HTTPBasicAuth
from app.models import User,Post,Comment
from app.api.errors import unauthorized, forbidden
from app.api import api
from flask import jsonify, g

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token,password):
    if email_or_token == '':
        return False
    # if no password is provided, use token authentication
    if password == '':
        user = User.verify_auth_token(email_or_token)
        g.current_user = user
        g.token_used = True
        return user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
    # error if user is nor confirmed must before every request
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden('Unconfirmed Account')

@api.route('/tokens/',methods=['POST'])
def get_token():
    # token can be generated and used instead of password
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credential')
    return jsonify({'token':g.current_user.generate_auth_token(expiration=3600), 'expiration':3600})

