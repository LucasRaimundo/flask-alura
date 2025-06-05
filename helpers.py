import os
from app_factory import app

def recoverImage(id):
    for namefile in os.listdir(app.config['UPLOAD_PATH']):
        if namefile == f'cover{id}.jpeg':
            return namefile
    return 'ask.png'