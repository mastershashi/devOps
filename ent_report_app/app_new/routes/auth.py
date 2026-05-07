from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Admin, Clinic

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        clinic_slug = request.form.get('clinic', 'default')
        
        admin = Admin.query.filter_by(email=email).first()
        
        if admin and check_password_hash(admin.password_hash, password):
            login_user(admin)
            return redirect(url_for('admin.dashboard', clinic_slug=clinic_slug))
        else:
            flash('Invalid credentials', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('public.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register_clinic():
    """Register new clinic (super admin only)"""
    if request.method == 'POST':
        try:
            clinic = Clinic(
                name=request.form.get('clinic_name'),
                slug=request.form.get('clinic_slug'),
                email=request.form.get('clinic_email'),
                phone=request.form.get('clinic_phone'),
                address=request.form.get('address'),
                city=request.form.get('city'),
                state=request.form.get('state'),
                zip_code=request.form.get('zip_code')
            )
            
            admin = Admin(
                clinic=clinic,
                username=request.form.get('admin_username'),
                email=request.form.get('admin_email'),
                password_hash=generate_password_hash(request.form.get('password')),
                is_super_admin=True
            )
            
            db.session.add(clinic)
            db.session.add(admin)
            db.session.commit()
            
            flash('Clinic registered successfully!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('auth/register_clinic.html')
