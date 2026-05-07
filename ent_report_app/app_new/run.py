#!/usr/bin/env python3
"""
ENT Clinic Booking System - Startup Script
"""
import os
import sys
from app import create_app, db
from models import Clinic, Admin, Doctor, FAQ, Testimonial
from werkzeug.security import generate_password_hash

def init_demo_data():
    """Initialize demo data for testing"""
    
    # Create default clinic if doesn't exist
    clinic = Clinic.query.filter_by(slug='default').first()
    if not clinic:
        clinic = Clinic(
            name='City ENT Clinic',
            slug='default',
            email='admin@entclinic.com',
            phone='+91-9876543210',
            address='123 Medical Street, Healthcare Plaza',
            city='New Delhi',
            state='Delhi',
            zip_code='110001',
            description='Leading ENT clinic with experienced specialists'
        )
        db.session.add(clinic)
        db.session.commit()
        print("✓ Created default clinic")
    
    # Create demo admin if doesn't exist
    admin = Admin.query.filter_by(email='admin@entclinic.com').first()
    if not admin:
        admin = Admin(
            clinic_id=clinic.id,
            username='admin',
            email='admin@entclinic.com',
            password_hash=generate_password_hash('admin123'),
            is_super_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Created demo admin (email: admin@entclinic.com, password: admin123)")
    
    # Create demo doctors
    if Doctor.query.filter_by(clinic_id=clinic.id).count() == 0:
        doctors = [
            {
                'name': 'Dr. Sourabh Kumar',
                'specialization': 'Otolaryngologist',
                'bio': 'Senior ENT specialist with 12 years of experience in sinus, allergy, and voice care.',
                'experience_years': 12,
                'consultation_fee': 500,
                'email': 'sourabh@entclinic.com',
                'phone': '+91-9876500001'
            },
            {
                'name': 'Dr. Priya Singh',
                'specialization': 'Pediatric ENT',
                'bio': 'Specialized in treating ear, nose, and throat issues in children',
                'experience_years': 10,
                'consultation_fee': 400,
                'email': 'priya@entclinic.com',
                'phone': '+91-9876543212'
            },
            {
                'name': 'Dr. Amit Patel',
                'specialization': 'Audiologist',
                'bio': 'Expert in hearing assessment and hearing aid fitting',
                'experience_years': 12,
                'consultation_fee': 300,
                'email': 'amit@entclinic.com',
                'phone': '+91-9876543213'
            }
        ]
        
        for doc_data in doctors:
            doctor = Doctor(clinic_id=clinic.id, **doc_data)
            db.session.add(doctor)
        
        db.session.commit()
        print(f"✓ Created {len(doctors)} demo doctors")
    
    # Create demo FAQs
    if FAQ.query.filter_by(clinic_id=clinic.id).count() == 0:
        faqs = [
            {
                'category': 'Booking',
                'question': 'How do I book an appointment?',
                'answer': 'You can book an appointment through our online portal. Select the doctor, date, and preferred time slot. No registration required to check availability.',
                'keywords': 'book, appointment, online',
                'is_active': True
            },
            {
                'category': 'Services',
                'question': 'What services do you provide?',
                'answer': 'We provide comprehensive ENT services including hearing tests, hearing aids, sinus treatment, voice therapy, and pediatric ENT care.',
                'keywords': 'services, treatment, consultation',
                'is_active': True
            },
            {
                'category': 'General',
                'question': 'What is the consultation fee?',
                'answer': 'Consultation fees vary by doctor. Usually ranging from ₹300 to ₹500. You can see the fee details when booking an appointment.',
                'keywords': 'fee, cost, price, payment',
                'is_active': True
            }
        ]
        
        for faq_data in faqs:
            faq = FAQ(clinic_id=clinic.id, **faq_data)
            db.session.add(faq)
        
        db.session.commit()
        print(f"✓ Created {len(faqs)} demo FAQs")
    
    # Create demo testimonials
    if Testimonial.query.filter_by(clinic_id=clinic.id).count() == 0:
        testimonials = [
            {
                'patient_name': 'Rajesh Sharma',
                'rating': 5,
                'message': 'Excellent service! Dr. Rajesh Kumar diagnosed my sinus problem accurately and the treatment was very effective. The staff is also very friendly and professional.',
                'is_approved': True
            },
            {
                'patient_name': 'Priya Patel',
                'rating': 5,
                'message': 'Very satisfied with the pediatric ENT care for my child. Dr. Priya Singh is amazing with kids and made the entire experience comfortable. Highly recommended!',
                'is_approved': True
            },
            {
                'patient_name': 'Amit Singh',
                'rating': 4,
                'message': 'Great hearing aid consultation. Dr. Amit Patel took time to understand my needs and recommended the perfect solution. The clinic is well-equipped and clean.',
                'is_approved': True
            },
            {
                'patient_name': 'Sunita Verma',
                'rating': 5,
                'message': 'Outstanding ENT clinic! The doctors are highly skilled and the appointment booking system is very convenient. Got my hearing test done professionally.',
                'is_approved': True
            },
            {
                'patient_name': 'Vikram Joshi',
                'rating': 5,
                'message': 'Best ENT specialists in Delhi. Dr. Rajesh Kumar treated my chronic ear infection effectively. The follow-up care was excellent. Thank you team!',
                'is_approved': True
            }
        ]
        
        for testimonial_data in testimonials:
            testimonial = Testimonial(clinic_id=clinic.id, **testimonial_data)
            db.session.add(testimonial)
        
        db.session.commit()
        print(f"✓ Created {len(testimonials)} demo testimonials")

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created")
        
        # Initialize demo data
        init_demo_data()
        
        print("\n" + "="*50)
        print("✓ Setup complete!")
        print("="*50)
        print("\nDemo Admin Credentials:")
        print("  Email: admin@entclinic.com")
        print("  Password: admin123")
        print("\nStarting development server...")
        print("  URL: http://localhost:5000")
        print("  Admin: http://localhost:5000/auth/login")
        print("="*50 + "\n")
        
        # Run the app
        app.run(debug=True, port=5000)
