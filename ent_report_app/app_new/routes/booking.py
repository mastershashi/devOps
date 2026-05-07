from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from app import get_current_clinic_slug
from models import db, Patient, Appointment, AppointmentSlot, Doctor, Clinic
from datetime import datetime, timedelta

booking_bp = Blueprint('booking', __name__)


def get_current_clinic():
    clinic_slug = get_current_clinic_slug()
    clinic = Clinic.query.filter_by(slug=clinic_slug).first()
    if not clinic:
        clinic = Clinic.query.first()
    return clinic


def get_demo_date():
    return datetime.today().date().isoformat()

@booking_bp.route('/appointment')
def check_slots():
    """Check available slots without registration"""
    clinic = get_current_clinic()
    doctors = Doctor.query.filter_by(clinic_id=clinic.id, is_active=True).all() if clinic else []
    return render_template('booking/check_slots.html', doctors=doctors, today=get_demo_date())

@booking_bp.route('/api/doctor/<int:doctor_id>')
def get_doctor_api(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    return jsonify({
        'id': doctor.id,
        'name': doctor.name,
        'specialization': doctor.specialization,
        'experience_years': doctor.experience_years,
        'consultation_fee': doctor.consultation_fee,
        'bio': doctor.bio,
        'email': doctor.email,
        'phone': doctor.phone
    })

@booking_bp.route('/api/slots/<int:doctor_id>/<date>')
def get_slots_api(doctor_id, date):
    """Get available slots for a doctor on a date"""
    try:
        appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
        slots = AppointmentSlot.query.filter_by(
            doctor_id=doctor_id,
            date=appointment_date,
            is_available=True
        ).all()
        
        slot_data = [{
            'id': s.id,
            'start_time': s.start_time.strftime('%H:%M'),
            'end_time': s.end_time.strftime('%H:%M'),
            'available': s.current_bookings < s.max_patients
        } for s in slots]
        
        return jsonify({'slots': slot_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@booking_bp.route('/register', methods=['GET', 'POST'])
def register_patient():
    """Patient registration for appointment"""
    if request.method == 'POST':
        try:
            clinic = get_current_clinic()
            phone = request.form.get('phone')
            existing_patient = Patient.query.filter_by(phone=phone).first()
            
            if existing_patient:
                return redirect(url_for('booking.book_appointment', patient_id=existing_patient.id))
            
            patient = Patient(
                clinic_id=clinic.id if clinic else 1,
                name=request.form.get('name'),
                phone=phone,
                email=request.form.get('email'),
                age=request.form.get('age'),
                gender=request.form.get('gender'),
                address=request.form.get('address')
            )
            
            db.session.add(patient)
            db.session.commit()
            
            flash('Registration successful! Now book your appointment.', 'success')
            return redirect(url_for('booking.book_appointment', patient_id=patient.id))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('booking.register_patient'))
    
    return render_template('booking/register.html')

@booking_bp.route('/book/<int:patient_id>', methods=['GET', 'POST'])
def book_appointment(patient_id):
    """Book appointment for registered patient"""
    patient = Patient.query.get_or_404(patient_id)
    
    if request.method == 'POST':
        try:
            slot_id = request.form.get('slot_id')
            doctor_id = request.form.get('doctor_id')
            
            slot = AppointmentSlot.query.get_or_404(slot_id)
            
            if slot.current_bookings >= slot.max_patients:
                flash('Slot is full', 'error')
                return redirect(url_for('booking.book_appointment', patient_id=patient_id))
            
            appointment = Appointment(
                clinic_id=patient.clinic_id,
                patient_id=patient_id,
                doctor_id=doctor_id,
                slot_id=slot_id,
                status='confirmed'
            )
            
            slot.current_bookings += 1
            if slot.current_bookings >= slot.max_patients:
                slot.is_available = False
            
            db.session.add(appointment)
            db.session.commit()
            
            flash('Appointment booked successfully!', 'success')
            return render_template('booking/confirmation.html', appointment=appointment)
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    clinic = get_current_clinic()
    doctors = Doctor.query.filter_by(clinic_id=clinic.id, is_active=True).all() if clinic else []
    return render_template('booking/book_appointment.html', patient=patient, doctors=doctors)

@booking_bp.route('/my-appointments/<phone>')
def my_appointments(phone):
    """Patient's appointments history"""
    patient = Patient.query.filter_by(phone=phone).first_or_404()
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    return render_template('booking/my_appointments.html', patient=patient, appointments=appointments)
