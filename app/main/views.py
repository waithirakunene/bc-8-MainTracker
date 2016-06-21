from flask import render_template, url_for, redirect, abort, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.main import main
from app.models import User, Facility

from app.main.forms import (
   AddFacilityDetailsForm, AddRepairPersons
)

@main.route('/add_facility', methods=['GET','POST'])
@login_required
def add_facility():
    form = AddFacilityDetailsForm()
    if form.validate_on_submit():
        facility = Facility( 
                facility_name = form.facility_name.data,
                facility_description = form.facility_description.data,
                facility_serial_no = form.facility_serial_no.data
             
        )
        db.session.add(facility)
        db.session.commit()
        flash('You have added an asset')
        return redirect(url_for('main.add_facility'))
    return render_template('main/add_facility.html', form=form)
        
        

@main.route('/add_repair_persons', methods=['GET','POST'])
@login_required
def add_repair_persons():
    form = AddRepairPersons()
    if form.validate_on_submit():
        repair_persons = RepairPersons(
            name = form.name.data,
            phone_no = form.name.data
            )
        db.session.add(repair_persons)
        db.session.commit()
        flash ('Added one repair person')
        return redirect(url_for('main.add_repair_persons'))
    return render_template('main/add_repair_persons.html', form=form)
       



       
   

