from flask import render_template, url_for, redirect, abort, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.main import main
from app.models import User, Facility, RepairPersons, Repairs

from app.main.forms import (
   AddFacilityDetailsForm, AddRepairPersons, RepairDetailsForm, RequestRepairForm
)

@main.route('/add_facility', methods=['GET','POST'])
def add_facility():
    form = AddFacilityDetailsForm()
    if form.validate_on_submit():
        facility = Facility( 
                facility_name= form.facility_name.data,
                facility_description = form.facility_description.data
                
             
        )
        db.session.add(facility)
        db.session.commit()
        flash('You have added a facility')
        return redirect(url_for('main.add_facility'))
    return render_template('main/add_facility.html', form=form)
 
      
        
@main.route('/add_repair_persons', methods=['GET','POST'])
@login_required
def add_repair_persons():
    form = AddRepairPersons()
    if form.validate_on_submit():
        repairPerson = RepairPersons( 
                name= form.name.data,
                phone_no = form.phone_no.data
                
             
        )
        db.session.add(repairPerson)
        db.session.commit()
        flash('You have added one person')
        return redirect(url_for('main.add_repair_persons'))
    return render_template('main/add_repair_persons.html', form=form)

@main.route('/request-repair', methods=['GET', 'POST'])
@login_required
def request_repair():
    form = RequestRepairForm()
    if form.validate_on_submit():
        repair = Repair(
            requested_by_id=current_user.id,
            facility_id=form.facility.data,
            facility_desc=form.facility_desc.data,
            
        )
        db.session.add(repair)
        db.session.commit()     
        #Notify admin
        return redirect(url_for('main.view_repair', repair_id=repair.id))
    return render_template('main/request_repair.html', form=form)


       



       
   

