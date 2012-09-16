#!/usr/bin/env python

# (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

VERSION = '0.1'

DEBUG=True
DEFAULT_USER='admin'
DEFAULT_PASS='gateisdown'

import os
import flask
from flask import request
import json
import random
from functools import wraps
from acom import data as acom_data
from acom.types.users import Users
from acom.types.inventory import Hosts, Groups

app = flask.Flask(__name__) # static_url_path=os.path.join(os.getcwd(),'ui'))
random.seed()

def log(msg):
    os.system("logger -t acom %s" % msg)    

def jdata():
    try:
        return json.loads(request.data)
    except ValueError:
        raise Exception("failed to parse JSON: %s" % request.data)

def check_auth(username, password):
    u = Users()
    all = u.list(internal=True)
    if len(all) == 0 and (username == DEFAULT_USER and password == DEFAULT_PASS):
        u.add(dict(name=DEFAULT_USER, _password=DEFAULT_PASS))
        return True
    if not u.login(username, password):
        log("login failed: %s" % (username))
        return False
    else:
        log("login successful: %s" % (username))
    return True

def authenticate(msg='Authenticate'):
    message = dict(message=msg)
    resp = flask.jsonify(message)
    # while it's technically wrong, returning 403 vs 401 such that browser popups don't occur
    resp.status_code = 403
    resp.headers['WWW-Authenticate'] = 'Basic realm="Ansible Commander"'
    return resp

def requires_inventory_secret(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = flask.request.data
        if data != acom_data.inventory_secret:
            abort(403)
        return f(*args, **kwargs)
    return decorated

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = flask.request.authorization
        if auth:
            log("DEBUG ONLY, u=%s p=%s" % (auth.username, auth.password))
        if not auth: 
            log("DEBUG missing auth tokens")
            return authenticate()
        elif not check_auth(auth.username, auth.password):
            return authenticate("Authentication Failed.")
        return f(*args, **kwargs)
    return decorated

def returns_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            return json.dumps(result)
        except acom_data.DoesNotExist, e:
            flask.abort(404)
    return decorated

@app.route('/', methods=['GET'])
def return_index():
    return flask.redirect('static/index.html')

@app.route('/api/', methods=['GET'])
@requires_auth
@returns_json
def hello_world():
    log("api called")
    return dict(
        rest_resources = dict(
            users  = dict(href='/api/users/', fields=Users().FIELDS),
            hosts  = dict(href='/api/hosts/', fields=Hosts().FIELDS),
            groups = dict(href='/api/groups/', fields=Groups().FIELDS),
        ),
        version=VERSION,
    )


@app.route('/api/users/<name>', methods=['GET','PUT','DELETE'])
@requires_auth
@returns_json
def user_service(name):
    if request.method == 'GET':
        return Users().lookup(name)
    elif request.method == 'PUT':
        return Users().edit(name, jdata())
    elif request.method == 'DELETE':
        return Users().delete(name)

@app.route('/api/users/', methods=['GET', 'POST'])
@requires_auth
@returns_json
def users_service():
    if request.method == 'GET':
        return Users().list()
    elif request.method == 'POST':
        return Users().add(jdata())

@app.route('/api/groups/', methods=['GET','POST'])
@requires_auth
@returns_json
def groups_service():
    if request.method == 'GET':
        return Groups().list()
    elif request.method == 'POST':
        return Groups().add(jdata())

@app.route('/api/groups/<name>', methods=['GET','PUT','DELETE'])
@requires_auth
@returns_json
def group_service(name):
    if request.method == 'GET':
        return Groups().lookup(name)
    elif request.method == 'PUT':
        return Groups().edit(name, jdata())
    elif request.method == 'DELETE':
        return Groups().delete(name)

@app.route('/api/hosts/', methods=['GET','POST'])
@requires_auth
@returns_json
def hosts_service():
    if request.method == 'GET':
        return Hosts().list()
    elif request.method == 'POST':
        return Hosts().add(jdata())

@app.route('/api/hosts/<name>', methods=['GET','PUT','DELETE'])
@requires_auth
@returns_json
def host_service(name):
    if request.method == 'GET':
        return Hosts().lookup(name)
    elif request.method == 'PUT':
        return Hosts().edit(name, jdata())
    elif request.method == 'DELETE':
        return Hosts().delete(name)

@app.route('/api/inventory/hosts/<name>', methods=['POST'])
@requires_inventory_secret
@returns_json
def inventory_host_info(name):
    return Hosts().lookup(name)['_blended_vars']

@app.route('/api/inventory/index', methods=['POST'])
@requires_inventory_secret
@returns_json
def inventory_index():
    groups = Groups().list()
    results = {}
    for g in groups:
        results[g['name']] = g['_indirect_hosts']
    return results

if __name__ == '__main__':
    app.debug = DEBUG
    app.run(debug=DEBUG)
