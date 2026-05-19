from extensions import db


class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pet_name = db.Column(db.String(120), nullable=False)
    species = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    weight = db.Column(db.Float, nullable=True)
    image = db.Column(db.String(200), nullable=True)

    appointments = db.relationship('Appointment', backref='pet', lazy=True)
    vaccines = db.relationship('Vaccine', backref='pet', lazy=True)
