from datetime import date
from extensions import db


class Vaccine(db.Model):
    __tablename__ = 'vaccines'

    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    vaccine_name = db.Column(db.String(120), nullable=False)
    vaccine_date = db.Column(db.Date, nullable=False)
    next_due_date = db.Column(db.Date, nullable=True)
