from flask import Blueprint, render_template, request, jsonify
from models import FAQ
from difflib import SequenceMatcher

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/ask', methods=['POST'])
def ask():
    """Chatbot API endpoint"""
    data = request.json
    question = data.get('question', '').lower()
    clinic_id = data.get('clinic_id', 1)
    
    if not question:
        return jsonify({'response': 'Please ask a question'}), 400
    
    # Search FAQs
    faqs = FAQ.query.filter_by(clinic_id=clinic_id, is_active=True).all()
    best_match = None
    best_score = 0.4  # Minimum similarity threshold
    
    for faq in faqs:
        score = SequenceMatcher(None, question, faq.question.lower()).ratio()
        if score > best_score:
            best_score = score
            best_match = faq
    
    if best_match:
        return jsonify({
            'response': best_match.answer,
            'confidence': best_score
        })
    else:
        return jsonify({
            'response': 'I\'m not sure about that. Please contact us directly.',
            'confidence': 0
        }), 200

@chatbot_bp.route('/faq-list')
def faq_list():
    """Get all FAQs by category"""
    clinic_id = request.args.get('clinic_id', 1, type=int)
    faqs = FAQ.query.filter_by(clinic_id=clinic_id, is_active=True).all()
    
    # Group by category
    categories = {}
    for faq in faqs:
        cat = faq.category or 'General'
        if cat not in categories:
            categories[cat] = []
        categories[cat].append({
            'id': faq.id,
            'question': faq.question,
            'answer': faq.answer
        })
    
    return jsonify(categories)
