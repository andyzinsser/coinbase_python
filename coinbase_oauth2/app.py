__author__ = 'gsibble'

from flask import Flask, render_template, request, make_response

from oauth2client.client import OAuth2WebServerFlow
import httplib2

app = Flask(__name__)
app.debug = True

import logging
logging.basicConfig()

# Create your own secrets.py that contains your Coinbase OAuth app credentials
# https://coinbase.com/oauth/applications
from secrets import CLIENT_ID, CLIENT_SECRET

coinbase_client = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, 'all',
                                      redirect_uri='http://coinbase-python.herokuapp.com/consumer_auth',
                                      auth_uri='https://www.coinbase.com/oauth/authorize',
                                      token_uri='https://www.coinbase.com/oauth/token')


@app.route('/')
def register_me():

    auth_url = coinbase_client.step1_get_authorize_url()

    return render_template('register.jinja2', auth_url=auth_url)


@app.route('/consumer_auth')
def receive_token():

    oauth_code = request.args['code']

    print oauth_code

    http = httplib2.Http(ca_certs='/etc/ssl/certs/ca-certificates.crt')

    token = coinbase_client.step2_exchange(oauth_code, http=http)

    return make_response(token.to_json())

if __name__ == '__main__':
    app.run()
