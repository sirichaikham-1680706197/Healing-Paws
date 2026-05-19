from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from extensions import db
from models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def home():
    return render_template('index.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password or not confirm_password:
            flash('กรุณากรอกข้อมูลให้ครบทุกช่อง', 'danger')
            return redirect(url_for('auth.register'))

        if password != confirm_password:
            flash('รหัสผ่านไม่ตรงกัน', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('มีชื่อผู้ใช้หรืออีเมลนี้แล้ว', 'danger')
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email, role='user')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('สมัครสมาชิกเรียบร้อยแล้ว โปรดยืนยันเข้าสู่ระบบ', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('เข้าสู่ระบบสำเร็จ', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('user.dashboard'))
        flash('อีเมลหรือรหัสผ่านไม่ถูกต้อง', 'danger')
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('ออกจากระบบแล้ว', 'success')
    return redirect(url_for('auth.login'))
