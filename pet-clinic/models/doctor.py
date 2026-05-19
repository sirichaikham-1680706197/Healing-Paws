from extensions import db


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), nullable=True)

    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
