from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from models.pet import Pet
from models.doctor import Doctor
from models.appointment import Appointment
from models.user import User

appointment_bp = Blueprint('appointment', __name__)


@appointment_bp.route('/appointments/book', methods=['GET', 'POST'])
@login_required
def book_appointment():
    pets = Pet.query.filter_by(owner_id=current_user.id).all()
    doctors = Doctor.query.order_by(Doctor.doctor_name).all()
    if request.method == 'POST':
        pet_id = request.form.get('pet_id')
        doctor_id = request.form.get('doctor_id')
        appointment_date = request.form.get('appointment_date')
        appointment_time = request.form.get('appointment_time')
        note = request.form.get('note')
        if not pet_id or not doctor_id or not appointment_date or not appointment_time:
            flash('กรุณากรอกข้อมูลการนัดหมายให้ครบ', 'danger')
            return redirect(url_for('appointment.book_appointment'))
        appointment = Appointment(
            pet_id=pet_id,
            doctor_id=doctor_id,
            appointment_date=datetime.fromisoformat(appointment_date).date(),
            appointment_time=appointment_time,
            status='Pending',
            note=note,
        )
        db.session.add(appointment)
        db.session.commit()
        flash('จองนัดสำเร็จ', 'success')
        return redirect(url_for('user.appointments'))
    return render_template('book_appointment.html', pets=pets, doctors=doctors)


@appointment_bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    results = []
    if query:
        results = Appointment.query.join(Pet).join(Doctor).filter(
            (Pet.pet_name.contains(query)) |
            (Doctor.doctor_name.contains(query)) |
            (Appointment.status.contains(query))
        ).all()
    return render_template('search_results.html', results=results, query=query)
