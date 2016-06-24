from flask import render_template, url_for, redirect, abort, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.main import main
from ..models import User, Facility, Maintainer, RepairRequests, RepairStatus, RepairAssignments

from app.main.forms import (
   AddFacilityDetailsForm, AddMaintainerForm, AssignToForm, RepairDetailsForm, RequestRepairForm, RejectRepairForm 
)

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = AddFacilityDetailsForm()
    template = 'main/add_facility.html'
    if current_user.is_admin:
        if form.validate_on_submit():
            facility = Facility( 
                    facility_name= form.facility_name.data,
                    facility_description = form.facility_description.data
                    )
            db.session.add(facility)
            db.session.commit()
            flash('You have added a facility')
            return redirect(url_for('main.index'))
    else:
        template = 'main/request_repair.html'
        form = RequestRepairForm()
        if form.validate_on_submit():
            repair = RepairRequests(
                requested_by=current_user.id,
                facility_id=form.facility.data,
                description=form.description.data,
                
            )
            db.session.add(repair)
            db.session.commit()     
            flash('Request Received.')
            return redirect(url_for('main.index'))

    return render_template(template, form=form)
  
        
@main.route('/add_repair_persons', methods=['GET','POST'])
@login_required
def add_maintainer():
    form = AddMaintainerForm()
    if form.validate_on_submit():
        repairPerson = Maintainer( 
            name= form.name.data,
            phone_no = form.phone_no.data 
        )
        db.session.add(repairPerson)
        db.session.commit()
        flash('You have added a maintainer')
        return redirect(url_for('main.add_maintainer'))
    return render_template('main/add_maintainer.html', form=form)

       
@main.route('/view-repairs/<int:repair_id>')
@login_required
def view_repairs(repair_id):
    repair = RepairRequests.query.get_or_404(repair_id)
    if not (current_user.is_admin):
        if RepairRequests.requested_by != current_user.id:
            abort(403)
    return render_template('main/repair_detail.html', repair=repair)


@main.route('/new-requests', methods=['GET', 'POST'])
@login_required
def view_new_requests():
    if current_user.is_admin:
        repairs = RepairRequests.query.filter_by(progress=0, confirmed=False).order_by(RepairRequests.date_requested.desc()).all()
    
    return render_template('main/new_requests.html', repairs=repairs)


@main.route('/repairs/reject/<int:repairs_id>', methods=['GET', 'POST'])
@login_required
def reject_repair_request(repairs_id):
    if not current_user.is_admin:
        abort(403)
    repair = RepairRequests.query.get_or_404(repairs_id)
    form = RejectRepairForm()

    if request.method == 'GET':
        temp = {
            'description': repair.description,
            'date_requested': repair.date_requested,
            'facility': repair.facility,
            'reasons': form.reasons.data
        }
        db.session.delete(repair)
        db.session.commit()
        return redirect(url_for('main.view_new_requests'))
    return render_template('main/new_requests.html', repair=repair, form=form)


@main.route('/request-progress')
@login_required
def view_request_progress():
    if current_user.is_admin:
        repairs = RepairAssignments.query.all()

    return render_template('main/request_progress.html', repairs=repairs)  

@main.route('/assign', methods=['GET', 'POST'])
@login_required
def assign_maintainer():
    repairs_id = request.args.get('id')
    form = AssignToForm()
    if form.validate_on_submit():
        assign = RepairAssignments(
            maintainer_id = form.name.data,
            message =form.message.data,
            repair_id = repairs_id
            )
        db.session.add(assign)
        db.session.commit()

        repair = RepairRequests.query.filter_by(id=repairs_id).first()
        repair.progress = 1
        db.session.commit()

        return redirect(url_for('main.view_new_requests'))

    return render_template('main/assign_repair.html', form=form)


@main.route('/notifications', methods=['GET', 'POST'])
@login_required
def view_notifications():
    repair_requests = RepairRequests.query.filter(RepairRequests.requested_by == current_user.id).all()
    results = []
    for req in repair_requests:
        results.append(req.id)

    repairs = RepairAssignments.query.filter(RepairAssignments.id.in_(results)).all()
    return render_template('main/notifications.html', repairs=repairs) 