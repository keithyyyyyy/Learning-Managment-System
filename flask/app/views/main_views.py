# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required
from flask.json import jsonify

from app import db
from app.models.user_models import UserProfileForm
# from app.models.employee import Employee
from app.models.database import *

main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    employeeList = Learner.query.all()
    return render_template('main/home_page.html', content=employeeList)


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/learner')
# @login_required  # Limits access to authenticated users
def learner_page():
    return render_template('main/learner.html')

@main_blueprint.route('/learner/enrolment')
def enrolment_page():
    enrolment = Enrolment.query.all()
    return render_template('main/learner.html', enrolment=enrolment)

@main_blueprint.route('/learner/courses')
def courses_page():
    courses = Course.query.all()
    return render_template('main/learner.html', courses=courses)

# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('main/admin_page.html')


@main_blueprint.route('/main/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html',
                           form=form)

# @main_blueprint.route('/layout')

# def layout():
#     return render_template('layout.html')
