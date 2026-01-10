from bottle import route, run, static_file, request, template, TEMPLATE_PATH, response, redirect
from datetime import datetime
import json
import socket
import re

import os 
import sys
if getattr(sys, 'frozen', False):  # Check if running as a frozen executable
        # Get the path to the executable
        executable_path = sys.executable
        # Extract the directory containing the executable
        dir_path= os.path.dirname(executable_path)
else:
    # Running as a regular Python script
    dir_path = os.getcwd()

if not os.path.isdir(os.path.join(dir_path, 'resources')):
    os.makedirs(os.path.join(dir_path, 'resources', 'uploads'))
    with open(os.path.join(dir_path, 'resources', 'acc.db'), 'x') as f:
        pass

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

secret_key = 'jb_web_private_key'
uids = []
users = []
mnums = []
year = datetime.now().year
moth = datetime.now().month
date = datetime.now().date
TEMPLATE_PATH.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), './web/'))
def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))

@route('/')
def index():
    user_code = request.get_cookie('ugr_cd', secret=secret_key)
    if not user_code or not user_code in uids:
        return template('./account/login.html', error_message=None)
    return template('index.html', user_name=users[uids.index(user_code)])
@route('/sign-up')    
def sign_up():
    return template('./account/sign_up.html', error_message=None)

@route('/<file:path>')
def resources(file):
    return static_file(file, root=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'web/'))

@route('/login', method='POST')
def login():
    if request.forms['mobile'] not in mnums:
        return template('./account/login.html', error_message='Invalid username or password')
    id = mnums.index(request.forms['mobile'])
    if request.forms['username'] == users[id]:
        response.set_cookie('ugr_cd', uids[id], secret=secret_key, maxage=2592000)
        response.set_cookie('usr_id', uids[id], maxage=2592000) # 30days
        response.set_cookie('usr_name', users[id], maxage=2592000)
    return redirect("/")

@route('/sign-up', method='POST')
def create_account():
    global seed
    if request.forms['mobile'] in mnums:
        return template('./account/sign_up.html', error_message='The mobile number is already registered. Please try other one')
    if not has_numbers(request.forms['mobile']):
        return template('./account/sign_up.html', error_message='Only numbers can be accepted. Please try other one')
    if bool(re.search('[;,?/<>%^*()-+]', request.forms['username'])):
        return template('./account/sign_up.html', error_message='User name can\'t contain ;,?/<>%^*()-+. Please try other one')
        
    seed+=1
    users.append(str(request.forms['username']).strip())
    mnums.append(request.forms['mobile'])
    uids.append(str(seed))
    response.set_cookie('ugr_cd', str(seed), secret=secret_key, maxage=2592000)
    response.set_cookie('usr_cd', str(seed), maxage=2592000)
    response.set_cookie('usr_name', request.forms['username'], maxage=2592000)
    with open(os.path.join(dir_path,'resources', 'acc.db'), 'a') as f:
        f.write(f"{request.forms['username']}={request.forms['mobile']}={seed};")
    return redirect('/')
    
    
@route('/file_upload', method='POST')
def file_upload():
    upload = request.files
    files = []
    for key, value in dict(upload).items():
        value.filename = f"{str(datetime.now()).replace(':', '-')}_{value.filename}"
        files.append(value.filename)
        value.save(os.path.join(dir_path,'uploads/')) # appends upload.filename automatically
        # name, ext = os.path.splitext(value.filename)

        # save_path = get_save_path_for_category(category)
    return json.dumps(files)

@route('/get', method='GET')
def get_file():
    return static_file(request.query.file, root=os.path.join(dir_path,'uploads/'))

global seed
seed = 1000

with open(os.path.join(dir_path,'resources', 'acc.db'), 'r') as f:
    data = f.read()
    if data:
        accts = [x.split('=') for x in data.split(';')[:-1]]
        for user, pas, seed in accts:
            users.append(user)
            mnums.append(pas)
            uids.append(seed)
        seed = int(seed)

if __name__ == '__main__':
    from  threading import Thread
    import soket
    t1 = Thread(target=soket.server.run_forever)
    t1.start()
    run(host=IPAddr, port=8080, debug=False,reloader=False)
