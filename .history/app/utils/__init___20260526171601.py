# This file makes the utils directory a Python packagefrom flask import Blueprint, render_template
from flask_login import login_required

from app.utils.admin_required import admin_required

dashboard_bp = Blueprint(
    'dashboard',
    __name__
)

@dashboard_bp.route('/dashboard')

@login_required
@admin_required

def dashboard():

    return render_template(
        'dashboard/dashboard.html'
    )