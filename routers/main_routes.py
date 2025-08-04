from flask import Blueprint, render_template

# Create a Blueprint for our main routes
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return "UrbanSphere is running! Your webhook is at /webhook."

@main_bp.route('/dashboard')
def show_dashboard():
    return render_template('dashboard.html')