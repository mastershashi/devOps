from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Clinic(db.Model):
    """Multi-tenant clinic/organization"""
    __tablename__ = 'clinics'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    logo_url = db.Column(db.String(500))
    website = db.Column(db.String(255))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    doctors = db.relationship('Doctor', backref='clinic', lazy=True, cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', backref='clinic', lazy=True, cascade='all, delete-orphan')
    slots = db.relationship('AppointmentSlot', backref='clinic', lazy=True, cascade='all, delete-orphan')
    testimonials = db.relationship('Testimonial', backref='clinic', lazy=True, cascade='all, delete-orphan')
    admins = db.relationship('Admin', backref='clinic', lazy=True, cascade='all, delete-orphan')
    faqs = db.relationship('FAQ', backref='clinic', lazy=True, cascade='all, delete-orphan')


class Admin(UserMixin, db.Model):
    """Admin users per clinic"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_super_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Doctor(db.Model):
    """Doctors per clinic"""
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    qualifications = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    consultation_fee = db.Column(db.Float, default=500.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    slots = db.relationship('AppointmentSlot', backref='doctor', lazy=True, cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', backref='doctor', lazy=True, cascade='all, delete-orphan')


class Patient(db.Model):
    """Patient information"""
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20), nullable=False, unique=True)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))  # M/F/Other
    address = db.Column(db.Text)
    medical_history = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy=True, cascade='all, delete-orphan')


class AppointmentSlot(db.Model):
    """Available appointment slots per doctor"""
    __tablename__ = 'appointment_slots'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    max_patients = db.Column(db.Integer, default=1)
    current_bookings = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='slot', lazy=True)


class Appointment(db.Model):
    """Patient appointments"""
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('appointment_slots.id'), nullable=False)
    status = db.Column(db.String(50), default='confirmed')  # confirmed, cancelled, completed
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reports = db.relationship('MedicalReport', backref='appointment', lazy=True, cascade='all, delete-orphan')


class MedicalReport(db.Model):
    """Medical reports generated by doctors"""
    __tablename__ = 'medical_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    diagnosis = db.Column(db.Text)
    findings = db.Column(db.Text)
    prescription = db.Column(db.Text)
    report_html = db.Column(db.LargeBinary)  # Stored as HTML
    report_file = db.Column(db.String(500))  # File path
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Testimonial(db.Model):
    """Patient testimonials for clinic"""
    __tablename__ = 'testimonials'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    patient_name = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, default=5)  # 1-5
    message = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class FAQ(db.Model):
    """Frequently asked questions and chatbot responses"""
    __tablename__ = 'faqs'
    
    id = db.Column(db.Integer, primary_key=True)
    clinic_id = db.Column(db.Integer, db.ForeignKey('clinics.id'), nullable=False)
    category = db.Column(db.String(100))  # e.g., Booking, Symptoms, Services
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    keywords = db.Column(db.String(500))  # comma-separated for search
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
