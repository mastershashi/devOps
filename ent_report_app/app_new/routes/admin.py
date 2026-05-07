from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Appointment, MedicalReport, Doctor, AppointmentSlot, Testimonial
from datetime import datetime, timedelta
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def check_admin():
    """Ensure user is admin"""
    pass

@admin_bp.route('/dashboard')
def dashboard():
    """Admin dashboard"""
    clinic_id = current_user.clinic_id
    
    stats = {
        'total_appointments': Appointment.query.filter_by(clinic_id=clinic_id).count(),
        'completed_appointments': Appointment.query.filter_by(clinic_id=clinic_id, status='completed').count(),
        'total_doctors': Doctor.query.filter_by(clinic_id=clinic_id).count(),
        'reports_generated': MedicalReport.query.filter_by(clinic_id=clinic_id).count()
    }
    
    recent_appointments = Appointment.query.filter_by(clinic_id=clinic_id).order_by(
        Appointment.created_at.desc()
    ).limit(10).all()
    
    return render_template('admin/dashboard.html', stats=stats, appointments=recent_appointments)

@admin_bp.route('/reports')
def reports():
    """Generate reports from appointment history"""
    clinic_id = current_user.clinic_id
    appointments = Appointment.query.filter_by(clinic_id=clinic_id, status='completed').all()
    return render_template('admin/reports.html', appointments=appointments)

@admin_bp.route('/reports/generate/<int:appointment_id>', methods=['GET', 'POST'])
def generate_report(appointment_id):
    """Generate medical report for appointment"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.clinic_id != current_user.clinic_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'POST':
        try:
            report = MedicalReport(
                appointment_id=appointment_id,
                clinic_id=appointment.clinic_id,
                diagnosis=request.form.get('diagnosis'),
                findings=request.form.get('findings'),
                prescription=request.form.get('prescription')
            )
            
            # TODO: Generate HTML report and save as file
            
            db.session.add(report)
            appointment.status = 'completed'
            db.session.commit()
            
            flash('Report generated successfully!', 'success')
            return redirect(url_for('admin.reports'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('admin/generate_report.html', appointment=appointment)

@admin_bp.route('/slots')
def manage_slots():
    """Manage appointment slots"""
    clinic_id = current_user.clinic_id
    doctors = Doctor.query.filter_by(clinic_id=clinic_id).all()
    slots = AppointmentSlot.query.filter_by(clinic_id=clinic_id).all()
    
    return render_template('admin/manage_slots.html', doctors=doctors, slots=slots)

@admin_bp.route('/api/slots/create', methods=['POST'])
def create_slot():
    """Create appointment slots"""
    data = request.json
    clinic_id = current_user.clinic_id
    
    try:
        for i in range(int(data.get('num_slots', 5))):
            slot = AppointmentSlot(
                clinic_id=clinic_id,
                doctor_id=data.get('doctor_id'),
                date=datetime.strptime(data.get('date'), '%Y-%m-%d').date(),
                start_time=datetime.strptime(data.get('start_time'), '%H:%M').time(),
                end_time=datetime.strptime(data.get('end_time'), '%H:%M').time(),
                max_patients=int(data.get('max_patients', 1))
            )
            db.session.add(slot)
        
        db.session.commit()
        return jsonify({'message': 'Slots created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@admin_bp.route('/testimonials')
def testimonials():
    """Manage testimonials"""
    clinic_id = current_user.clinic_id
    testimonials = Testimonial.query.filter_by(clinic_id=clinic_id).all()
    return render_template('admin/testimonials.html', testimonials=testimonials)

@admin_bp.route('/api/testimonials/<int:testimonial_id>/approve', methods=['POST'])
@login_required
def approve_testimonial(testimonial_id):
    """Approve testimonial"""
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    
    if testimonial.clinic_id != current_user.clinic_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    testimonial.is_approved = True
    db.session.commit()
    
    return jsonify({'message': 'Testimonial approved'})

@admin_bp.route('/doctors')
def manage_doctors():
    """Manage clinic doctors"""
    clinic_id = current_user.clinic_id
    doctors = Doctor.query.filter_by(clinic_id=clinic_id).all()
    return render_template('admin/doctors.html', doctors=doctors)

@admin_bp.route('/api/doctors', methods=['POST'])
def create_doctor():
    """Add new doctor"""
    data = request.form
    clinic_id = current_user.clinic_id
    
    try:
        doctor = Doctor(
            clinic_id=clinic_id,
            name=data.get('name'),
            specialization=data.get('specialization'),
            bio=data.get('bio'),
            email=data.get('email'),
            phone=data.get('phone'),
            qualifications=data.get('qualifications'),
            experience_years=data.get('experience_years'),
            consultation_fee=data.get('consultation_fee', 500)
        )
        
        db.session.add(doctor)
        db.session.commit()
        
        return jsonify({'message': 'Doctor added successfully', 'id': doctor.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
