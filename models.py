from app_factory import db

class Games(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(40), nullable=False)
    platform = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Game {self.name}>'
    
class Users(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'  