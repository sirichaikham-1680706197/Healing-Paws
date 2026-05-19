import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from extensions import db
from models.pet import Pet
from models.doctor import Doctor
from models.appointment import Appointment
from models.treatment import Treatment
from models.vaccine import Vaccine
from models.payment import Payment
from models.user import User

user_bp = Blueprint('user', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def role_required(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash('คุณไม่มีสิทธิ์ใช้งานหน้านี้', 'danger')
                return redirect(url_for('user.dashboard'))
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator


@user_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    pets = Pet.query.filter_by(owner_id=current_user.id).all()
    appointments = Appointment.query.join(Pet).filter(Pet.owner_id == current_user.id).order_by(Appointment.appointment_date.desc()).limit(5).all()
    vaccines = Vaccine.query.join(Pet).filter(Pet.owner_id == current_user.id).order_by(Vaccine.vaccine_date.desc()).limit(5).all()
    payments = Payment.query.join(Appointment).join(Pet).filter(Pet.owner_id == current_user.id).order_by(Payment.payment_date.desc()).limit(5).all()
    return render_template('dashboard.html', pets=pets, appointments=appointments, vaccines=vaccines, payments=payments)


@user_bp.route('/pets')
@login_required
def pets():
    pets = Pet.query.filter_by(owner_id=current_user.id).all()
    return render_template('pets.html', pets=pets)


@user_bp.route('/pets/add', methods=['GET', 'POST'])
@login_required
def add_pet():
    if request.method == 'POST':
        pet_name = request.form.get('pet_name')
        species = request.form.get('species')
        breed = request.form.get('breed')
        age = request.form.get('age')
        gender = request.form.get('gender')
        weight = request.form.get('weight')
        image_file = request.files.get('image')
        image_filename = ''

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            image_filename = filename

        pet = Pet(owner_id=current_user.id, pet_name=pet_name, species=species, breed=breed or '', age=int(age) if age else None, gender=gender or '', weight=float(weight) if weight else None, image=image_filename)
        db.session.add(pet)
        db.session.commit()
        flash('เพิ่มข้อมูลสัตว์เลี้ยงเรียบร้อย', 'success')
        return redirect(url_for('user.pets'))

    return render_template('pet_form.html', pet=None)


@user_bp.route('/pets/edit/<int:pet_id>', methods=['GET', 'POST'])
@login_required
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if pet.owner_id != current_user.id and not current_user.is_admin():
        flash('คุณไม่มีสิทธิ์แก้ไขข้อมูลนี้', 'danger')
        return redirect(url_for('user.pets'))

    if request.method == 'POST':
        pet.pet_name = request.form.get('pet_name')
        pet.species = request.form.get('species')
        pet.breed = request.form.get('breed')
        pet.age = int(request.form.get('age')) if request.form.get('age') else None
        pet.gender = request.form.get('gender')
        pet.weight = float(request.form.get('weight')) if request.form.get('weight') else None
        image_file = request.files.get('image')
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            pet.image = filename
        db.session.commit()
        flash('แก้ไขข้อมูลสัตว์เลี้ยงเรียบร้อย', 'success')
        return redirect(url_for('user.pets'))

    return render_template('pet_form.html', pet=pet)


@user_bp.route('/pets/delete/<int:pet_id>')
@login_required
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    if pet.owner_id != current_user.id and not current_user.is_admin():
        flash('คุณไม่มีสิทธิ์ลบข้อมูลนี้', 'danger')
        return redirect(url_for('user.pets'))
    db.session.delete(pet)
    db.session.commit()
    flash('ลบสัตว์เลี้ยงเรียบร้อย', 'success')
    return redirect(url_for('user.pets'))


@user_bp.route('/appointments')
@login_required
def appointments():
    appointments = Appointment.query.join(Pet).filter(Pet.owner_id == current_user.id).order_by(Appointment.appointment_date.desc()).all()
    return render_template('appointments.html', appointments=appointments)


@user_bp.route('/treatments')
@login_required
def treatments():
    treatments = Treatment.query.join(Appointment).join(Pet).filter(Pet.owner_id == current_user.id).order_by(Treatment.treatment_date.desc()).all()
    return render_template('treatments.html', treatments=treatments)


@user_bp.route('/vaccines')
@login_required
def vaccines():
    vaccines = Vaccine.query.join(Pet).filter(Pet.owner_id == current_user.id).order_by(Vaccine.vaccine_date.desc()).all()
    return render_template('vaccines.html', vaccines=vaccines)


@user_bp.route('/payments')
@login_required
def payments():
    payments = Payment.query.join(Appointment).join(Pet).filter(Pet.owner_id == current_user.id).order_by(Payment.payment_date.desc()).all()
    return render_template('payments.html', payments=payments)
