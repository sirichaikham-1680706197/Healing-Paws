from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from models.pet import Pet
from models.doctor import Doctor
from models.appointment import Appointment
from models.treatment import Treatment
from models.vaccine import Vaccine
from models.payment import Payment

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def admin_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('หน้านี้สำหรับผู้ดูแลระบบเท่านั้น', 'danger')
            return redirect(url_for('user.dashboard'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    user_count = User.query.count()
    pet_count = Pet.query.count()
    appointment_count = Appointment.query.count()
    doctor_count = Doctor.query.count()
    payment_count = Payment.query.count()
    recent_appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).limit(5).all()
    return render_template('admin/dashboard.html', user_count=user_count, pet_count=pet_count, appointment_count=appointment_count, doctor_count=doctor_count, payment_count=payment_count, recent_appointments=recent_appointments)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    query = request.args.get('q', '')
    users = User.query
    if query:
        users = users.filter((User.username.contains(query)) | (User.email.contains(query)))
    users = users.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users, query=query)


@admin_bp.route('/users/delete/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin():
        flash('ไม่สามารถลบผู้ดูแลระบบได้', 'warning')
        return redirect(url_for('admin.users'))
    db.session.delete(user)
    db.session.commit()
    flash('ลบผู้ใช้งานเรียบร้อยแล้ว', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/pets')
@login_required
@admin_required
def pets():
    pets = Pet.query.order_by(Pet.pet_name).all()
    return render_template('admin/pets.html', pets=pets)


@admin_bp.route('/doctors', methods=['GET', 'POST'])
@login_required
@admin_required
def doctors():
    if request.method == 'POST':
        name = request.form.get('doctor_name')
        specialty = request.form.get('specialty')
        phone = request.form.get('phone')
        email = request.form.get('email')
        if not name or not specialty:
            flash('กรุณากรอกข้อมูลแพทย์ให้ครบ', 'danger')
            return redirect(url_for('admin.doctors'))
        doctor = Doctor(doctor_name=name, specialty=specialty, phone=phone, email=email)
        db.session.add(doctor)
        db.session.commit()
        flash('เพิ่มข้อมูลแพทย์เรียบร้อย', 'success')
        return redirect(url_for('admin.doctors'))
    doctors = Doctor.query.order_by(Doctor.doctor_name).all()
    return render_template('admin/doctors.html', doctors=doctors)


@admin_bp.route('/doctors/delete/<int:doctor_id>')
@login_required
@admin_required
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    flash('ลบข้อมูลแพทย์เรียบร้อย', 'success')
    return redirect(url_for('admin.doctors'))


@admin_bp.route('/appointments')
@login_required
@admin_required
def appointments():
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    return render_template('admin/appointments.html', appointments=appointments)


@admin_bp.route('/appointments/treatment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_treatment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        diagnosis = request.form.get('diagnosis')
        treatment_detail = request.form.get('treatment_detail')
        medicine = request.form.get('medicine')
        treatment_date = request.form.get('treatment_date')
        if not symptoms or not diagnosis or not treatment_detail:
            flash('กรุณากรอกข้อมูลการรักษาให้ครบ', 'danger')
            return redirect(url_for('admin.add_treatment', appointment_id=appointment.id))
        treatment = Treatment(
            appointment_id=appointment.id,
            symptoms=symptoms,
            diagnosis=diagnosis,
            treatment_detail=treatment_detail,
            medicine=medicine,
            treatment_date=datetime.fromisoformat(treatment_date).date() if treatment_date else datetime.utcnow().date()
        )
        db.session.add(treatment)
        db.session.commit()
        flash('บันทึกการรักษาสำเร็จ', 'success')
        return redirect(url_for('admin.appointments'))
    return render_template('admin/treatment_form.html', appointment=appointment)


@admin_bp.route('/vaccines', methods=['GET', 'POST'])
@login_required
@admin_required
def vaccines():
    if request.method == 'POST':
        pet_id = request.form.get('pet_id')
        vaccine_name = request.form.get('vaccine_name')
        vaccine_date = request.form.get('vaccine_date')
        next_due_date = request.form.get('next_due_date')
        if not pet_id or not vaccine_name or not vaccine_date:
            flash('กรุณากรอกข้อมูลวัคซีนให้ครบ', 'danger')
            return redirect(url_for('admin.vaccines'))
        vaccine = Vaccine(pet_id=pet_id, vaccine_name=vaccine_name, vaccine_date=datetime.fromisoformat(vaccine_date).date(), next_due_date=datetime.fromisoformat(next_due_date).date() if next_due_date else None)
        db.session.add(vaccine)
        db.session.commit()
        flash('บันทึกข้อมูลวัคซีนเรียบร้อย', 'success')
        return redirect(url_for('admin.vaccines'))
    vaccines = Vaccine.query.order_by(Vaccine.vaccine_date.desc()).all()
    pets = Pet.query.order_by(Pet.pet_name).all()
    return render_template('admin/vaccines.html', vaccines=vaccines, pets=pets)


@admin_bp.route('/vaccines/delete/<int:vaccine_id>')
@login_required
@admin_required
def delete_vaccine(vaccine_id):
    vaccine = Vaccine.query.get_or_404(vaccine_id)
    db.session.delete(vaccine)
    db.session.commit()
    flash('ลบวัคซีนเรียบร้อย', 'success')
    return redirect(url_for('admin.vaccines'))


@admin_bp.route('/payments', methods=['GET', 'POST'])
@login_required
@admin_required
def payments():
    if request.method == 'POST':
        appointment_id = request.form.get('appointment_id')
        amount = request.form.get('amount')
        status = request.form.get('payment_status')
        payment_date = request.form.get('payment_date')
        if not appointment_id or not amount or not status:
            flash('กรุณากรอกข้อมูลการชำระเงินให้ครบ', 'danger')
            return redirect(url_for('admin.payments'))
        payment = Payment(appointment_id=appointment_id, amount=float(amount), payment_status=status, payment_date=datetime.fromisoformat(payment_date).date() if payment_date else datetime.utcnow().date())
        db.session.add(payment)
        db.session.commit()
        flash('บันทึกการชำระเงินเรียบร้อย', 'success')
        return redirect(url_for('admin.payments'))
    payments = Payment.query.order_by(Payment.payment_date.desc()).all()
    appointments = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    return render_template('admin/payments.html', payments=payments, appointments=appointments)
