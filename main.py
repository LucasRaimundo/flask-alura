from app_factory import app, db # <--- Mude esta linha!
from views import *

if __name__ == '__main__':
    app.run(debug=True)