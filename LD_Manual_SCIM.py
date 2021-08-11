'''
Borrowed HEAVILY from:
https://requests-oauthlib.readthedocs.io/en/latest/examples/real_world_example.html
'''

from flask import Flask, request, redirect, session, url_for, render_template
from flask.json import jsonify
import json
import requests
from requests_oauthlib import OAuth2Session
import os

app = Flask(__name__)

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
authorization_base_url = 'https://app.launchdarkly.com/trust/oauth/authorize'
token_url = 'https://app.launchdarkly.com/trust/oauth/token'
redirect_uri = 'http://localhost:5000/callback' # CHANGE THIS based on your own callback URI


@app.route('/')
def index():
    return 'Hello - you found the home page!'

@app.route("/auth")
def auth():
    '''Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    '''
    launchdarkly = OAuth2Session(client_id, redirect_uri=redirect_uri)

    authorization_url, state = launchdarkly.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    ''' Step 2: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    '''

    launchdarkly = OAuth2Session(client_id, state=session['oauth_state'], redirect_uri=redirect_uri)
    token = launchdarkly.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url, include_client_id=True)

    session['oauth_token'] = token

    return redirect(url_for('.user'))


@app.route("/user")
def user():
    ''' Step 3: Creating a user

    We have now successfully obtained a token, and can subsequently use that to access protected resources. In this case, creating a user.
    '''

    SCIMPayload = json.dumps({
     "userName":"TotallyRealEmailAddress@example.com",
     "name":{
       "familyName":"Tester",
       "givenName":"Tester"
     },
     "emails":[
       {
           "value":"TotallyRealEmailAddress@example.com"
       }
     ]
   })

    url = "https://app.launchdarkly.com/trust/scim/v2/Users"


    launchdarkly = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(launchdarkly.post(url=url, data=SCIMPayload).json())


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = os.urandom(24)
    app.run(host='0.0.0.0', port=5000, debug=True)