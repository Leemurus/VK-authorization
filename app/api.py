from app import app
from flask import url_for, redirect, request
from flask_login import login_user

from app.oauth import Provider
from app.models import User
from app.utils import not_authenticated


@app.route('/api/authorize/<string:provider_name>', methods=['GET', 'POST'])
@not_authenticated
def oauth_authorize(provider_name):
    provider = Provider.get_provider(provider_name)
    if provider is None:
        return url_for('authorization')

    return provider.authorize()


@app.route('/api/callback/<string:provider_name>', methods=['GET', 'POST'])
@not_authenticated
def oauth_callback(provider_name):
    provider = Provider.get_provider(provider_name)
    if provider is None:
        return redirect(url_for('authorization'))

    data = provider.callback(request.args.get('code'))
    if data is None or None in data:
        return redirect(url_for('authorization'))

    user_information, friends = data

    user = User.query.filter_by(social_id=user_information['id']).first()
    if not user:
        user = User(social_id=user_information['id'],
                    first_name=user_information['first_name'],
                    last_name=user_information['last_name'],
                    friends=friends)

    login_user(user, remember=True)

    return redirect(url_for('index'))
