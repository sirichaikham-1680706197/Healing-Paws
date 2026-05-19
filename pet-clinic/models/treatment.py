from datetime import datetime
from extensions import db


class Treatment(db.Model):
    __tablename__ = 'treatments'

    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment_detail = db.Column(db.Text, nullable=False)
    medicine = db.Column(db.String(150), nullable=True)
    treatment_date = db.Column(db.Date, default=datetime.utcnow)
