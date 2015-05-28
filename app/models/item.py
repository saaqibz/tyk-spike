from app import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    name = db.Column(db.String)
    
    description = db.Column(db.String)
    
    thumbnail = db.Column(db.String)
    

    def to_dict(self):
        return dict(
            id = self.id,
            name = self.name,
            description = self.description,
            thumbnail = self.thumbnail,
        )

    def __repr__(self):
        return '<Item %r>' % (self.id)
