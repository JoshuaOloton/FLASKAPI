from flask import current_app, render_template, url_for
import requests, os

def send_reset_email(token,email):
	return requests.post(
		f"https://api.mailgun.net/v3/{os.environ.get('SANDBOX_DOMAIN_NAME')}/messages",
		auth=("api", f"{os.environ.get('API_KEY')}"),
		data={"from": f"Flask App <mailgun@{os.environ.get('SANDBOX_DOMAIN_NAME')}>",
			"to": [f"{email}"],
			"subject": "Reset your Password",
			"text": f""" Please follow this link to reset your account
{url_for("auth.password_reset",token=token)} 
Please ignore this mail if you did not make the following request."""})

def send_confirmation_email(token,email):
	return requests.post(
		f"https://api.mailgun.net/v3/{os.environ.get('SANDBOX_DOMAIN_NAME')}/messages",
		auth=("api", f"{os.environ.get('API_KEY')}"),
		data={"from": f"Flask App <mailgun@{os.environ.get('SANDBOX_DOMAIN_NAME')}>",
			"to": [f"{email}"],
			"subject": "Confirm Your Account",
			"text": f""" Please follow this link to verify your account
{url_for("auth.confirm",_external=True,token=token)} 
Please ignore this mail if you did not make the following request."""})
