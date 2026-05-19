from datetime import date
from extensions import db


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Pending')
    note = db.Column(db.Text, nullable=True)

    treatment = db.relationship('Treatment', backref='appointment', uselist=False)
    payment = db.relationship('Payment', backref='appointment', uselist=False)
