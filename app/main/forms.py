from flask import flash
from flask_wtf import Form
from .. models import Facility
from wtforms import SubmitField, SelectField, StringField, TextAreaField, IntegerField
from wtforms.validators import Required, Length, ValidationError, Regexp, Email, NumberRange




class AddFacilityDetailsForm(Form):
    Facility_name = StringField("Asset Name",validators=[Required(), Length(8, 50)])
    Facility_description = TextAreaField("Detailed Information")
    Facility_serial_no = StringField(
        "Serial No.", 
        validators= [
            Required(), 
            Length(10, 15), 
            Regexp(
                '^[A-Za-z][A-Za-z0-9_.]*$', 
                0,
                'Usernames must have only letters, ''numbers, dots or underscores')]),
                
    
    submit = SubmitField("Submit")


class AddRepairPersons(Form):
    name = StringField("Name Asset", validators=[()])
    phone_no = IntegerField(
            "Phone Number", 
            validators=
            [Required(),
            Length(10, 13)])
    
    submit = SubmitField("Add")

