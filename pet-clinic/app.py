import os
from datetime import datetime
from flask import Flask, render_template
from flask_login import current_user
from config import Config
from extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        from routes.auth import auth_bp
        from routes.user import user_bp
        from routes.admin import admin_bp
        from routes.appointment import appointment_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(appointment_bp)

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        db.create_all()
        create_sample_data()

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    return app


def create_sample_data():
    from models.user import User
    from models.doctor import Doctor
    from models.pet import Pet
    from models.appointment import Appointment
    from models.treatment import Treatment
    from models.vaccine import Vaccine
    from models.payment import Payment

    if User.query.first():
        return

    admin = User(username='admin', email='admin@clinic.com', role='admin')
    admin.set_password('admin123')
    user = User(username='petlover', email='user@clinic.com', role='user')
    user.set_password('user123')
    db.session.add_all([admin, user])
    db.session.commit()

    doc1 = Doctor(doctor_name='Dr. Anna', specialty='Surgery', phone='0912345678', email='anna@clinic.com')
    doc2 = Doctor(doctor_name='Dr. Ben', specialty='Dermatology', phone='0987654321', email='ben@clinic.com')
    db.session.add_all([doc1, doc2])
    db.session.commit()

    pet = Pet(owner_id=user.id, pet_name='Milo', species='Dog', breed='Beagle', age=3, gender='Male', weight=12.4, image='')
    db.session.add(pet)
    db.session.commit()

    appointment = Appointment(pet_id=pet.id, doctor_id=doc1.id, appointment_date=datetime.utcnow().date(), appointment_time='10:30', status='Completed', note='Annual checkup')
    db.session.add(appointment)
    db.session.commit()

    treatment = Treatment(appointment_id=appointment.id, symptoms='Coughing', diagnosis='Mild infection', treatment_detail='Rest and fluids', medicine='Antibiotics', treatment_date=datetime.utcnow().date())
    vaccine = Vaccine(pet_id=pet.id, vaccine_name='Rabies', vaccine_date=datetime.utcnow().date(), next_due_date=datetime.utcnow().date())
    payment = Payment(appointment_id=appointment.id, amount=1200.00, payment_status='Paid', payment_date=datetime.utcnow().date())
    db.session.add_all([treatment, vaccine, payment])
    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
