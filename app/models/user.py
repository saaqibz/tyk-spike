from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    tokens = db.Column(db.String)
    clientId = db.Column(db.Integer)


    def to_dict(self):
        return dict(
            email = self.email,
            password = self.password,
            tokens = self.tokens,
            id = self.id,
            clientId = self.clientId
        )

    def __repr__(self):
        return '<User %r>' % (self.id, self.email)
