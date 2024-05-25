from django import forms
from .models import CandidateMaster

class CandidateMasterForm(forms.ModelForm):
    class Meta:
        model = CandidateMaster
        fields = ['City_Id','State_Id','Course_Id','FirstName','LastName',
                  'Candidate_Email','Phone_no','Address1','Address2','pincode','adhar_Number'
                  ,'DOB','Job_role','Training_Status','Placed_Status',
                  'Training_Scheme_Name','Gender']
    def __init__(self, *args, **kwargs):
        super(CandidateMasterForm, self).__init__(*args, **kwargs)

        self.fields['City_Id'].widget.attrs.update({'class': 'form-select',
                                                     'style':'border-radius: 50px;'})
        self.fields['State_Id'].widget.attrs.update({'class': 'form-select',
                                                     'style':'border-radius: 50px;'})
        self.fields['Course_Id'].widget.attrs.update({'class': 'form-select',
                                                     'style':'border-radius: 50px;'})
        self.fields['FirstName'].widget.attrs.update({'class': 'form-control',
                                                     'style':'border-radius: 50px;'})
        self.fields['LastName'].widget.attrs.update({'class': 'form-control',
                                                            'style':'border-radius: 50px;'})
        self.fields['Candidate_Email'].widget.attrs.update({'class': 'form-control',
                                                                    'style':'border-radius: 50px;'})
        self.fields['Phone_no'].widget.attrs.update({'class': 'form-control',
                                                                    'style':'border-radius: 50px;'})
        self.fields['Address1'].widget.attrs.update({'class': 'form-control',
                                                                    'style':'border-radius: 25px;'})
        self.fields['Address2'].widget.attrs.update({'class': 'form-control',
                                                                    'style':'border-radius: 25px;'})
        self.fields['pincode'].widget.attrs.update({'class': 'form-control',
                                                                    'style':'border-radius: 50px;'})
        self.fields['adhar_Number'].widget.attrs.update({'class': 'form-control',
                                                                    'style':'border-radius: 50px;'})
        self.fields['DOB'].widget.attrs.update({'class': 'form-control',
                                                                    'style':'border-radius: 50px;'})
        self.fields['Job_role'].widget.attrs.update({'class': 'form-control',
                                                                    'style':'border-radius: 50px;'})
        self.fields['Training_Status'].widget.attrs.update({'class': 'form-control',
                                                                    'style':'border-radius: 50px;'})
        self.fields['Placed_Status'].widget.attrs.update({'class': 'form-control',
                                                                    'style':'border-radius: 50px;'})
        self.fields['Training_Scheme_Name'].widget.attrs.update({'class': 'form-control',
                                                                    'style':'border-radius: 50px;'})

        self.fields['Gender'].widget.attrs.update({'class': 'form-control',
                                                                    'style':'border-radius: 50px;'})

