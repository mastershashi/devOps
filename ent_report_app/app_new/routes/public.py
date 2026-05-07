from flask import Blueprint, render_template, request
from models import Clinic, Doctor, Testimonial, FAQ

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    """Landing page"""
    clinic = get_clinic_from_request()
    doctors = Doctor.query.filter_by(clinic_id=clinic.id, is_active=True).all() if clinic else []
    testimonials = Testimonial.query.filter_by(clinic_id=clinic.id, is_approved=True).all() if clinic else []
    return render_template('public/index.html', clinic=clinic, doctors=doctors, testimonials=testimonials)

@public_bp.route('/doctors')
def doctors_list():
    """All doctors listing"""
    clinic = get_clinic_from_request()
    doctors = Doctor.query.filter_by(clinic_id=clinic.id, is_active=True).all() if clinic else []
    return render_template('public/doctors.html', clinic=clinic, doctors=doctors)

@public_bp.route('/doctor/<int:doctor_id>')
def doctor_detail(doctor_id):
    """Individual doctor profile"""
    doctor = Doctor.query.get_or_404(doctor_id)
    return render_template('public/doctor_detail.html', doctor=doctor)

@public_bp.route('/about')
def about():
    """About clinic page"""
    clinic = get_clinic_from_request()
    return render_template('public/about.html', clinic=clinic)

@public_bp.route('/services')
def services():
    """Services offered"""
    clinic = get_clinic_from_request()
    return render_template('public/services.html', clinic=clinic)

@public_bp.route('/contact')
def contact():
    """Contact page"""
    clinic = get_clinic_from_request()
    return render_template('public/contact.html', clinic=clinic)

def get_clinic_from_request():
    """Get current clinic from request"""
    from app import get_current_clinic_slug
    from models import Clinic
    clinic_slug = get_current_clinic_slug()
    clinic = Clinic.query.filter_by(slug=clinic_slug).first()
    if not clinic:
        clinic = Clinic.query.first()  # Fallback to first clinic
    return clinic
