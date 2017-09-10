CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

import os
#basedir = os.path.abspath(os.path.dirname(__file__))
MONGODB_SETTINGS = {
    'db': 'pick',
    'host':'mongodb://localhost:27017/pick.db'
}

UPLOAD_FOLDER = 'E:\\fss\\'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'avi','mp4'])
