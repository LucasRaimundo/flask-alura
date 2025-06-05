import os
from app_factory import app

def recoverImage(id):
    for namefile in os.listdir(app.config['UPLOAD_PATH']):
        if f'cover{id}.jpeg'in namefile:
            return namefile
    return 'ask.png'

def deleteFile(id):
    file = recoverImage(id)
    if file != 'ask.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))
        return True