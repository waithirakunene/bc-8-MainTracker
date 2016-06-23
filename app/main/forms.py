from flask import flash
from flask_wtf import Form
from ..models import Facility, RepairPersons, Repairs, RepairStatus
from wtforms import SubmitField, SelectField, StringField, TextAreaField, IntegerField, BooleanField
from wtforms.validators import Required, Length, ValidationError, Regexp, Email, NumberRange


class AddFacilityDetailsForm(Form):
    facility_name = StringField("Facility Name",validators=[Required(), Length(8, 50)])
    facility_description = TextAreaField("Detailed Information")
    
    submit = SubmitField("Submit")
    #validate facility name
    def validate_name(self, field):
        if Facility.query.filter_by(facility_name=field.data).first():
            raise ValidationError("Facility exists.")



class AddRepairPersons(Form):
    name = StringField("Name ", validators=[Required(), Length(8, 50)])
    phone_no  = IntegerField(
            "phone_no", validators = []
            )
            
    
    submit = SubmitField("Add")


class RepairDetailsForm(Form):
    description = StringField("Description", validators=[Required(), Length(10, 255)])
    facility = SelectField("Facility", coerce=int)

    def __init__(self, *args, **kwargs):
        super(RepairDetailsForm, self).__init__(*args, **kwargs)
        self.facility.choices = [
            (i.id, i.facility_name) for i in Facility.query.order_by(Facility.facility_name).all()
        ]


class RequestRepairForm(RepairDetailsForm):
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(RequestRepairForm, self).__init__(*args, **kwargs)

class RejectRepairForm(Form):
    reasons = TextAreaField("Write a Comments.")
   
class AssignToForm(Form):
    # def __init__(self):
    name = SelectField("Name", coerce=int)
    message = TextAreaField("message")

    def __init__(self, *args, **kwargs):
        super(AssignToForm, self).__init__(*args, **kwargs)
        self.name.choices = [
            (i.id, i.name) for i in RepairPersons.query.order_by(RepairPersons.name).all()
        ]

   
    



class AddFacilityDetailsForm(Form):
    facility_name = StringField("Facility Name",validators=[Required(), Length(8, 50)])
    facility_description = TextAreaField("Detailed Information")
    
    submit = SubmitField("Submit")
   

    #validate facility name
    def validate_name(self, field):
        if Facility.query.filter_by(facility_name=field.data).first():
            raise ValidationError("Facility exists.")

