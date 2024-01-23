from django import forms
from Auth.models import Employee, Department, Position, TypePrime

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        
class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PositionForm, self).__init__(*args, **kwargs)

class TypePrimeForm(forms.ModelForm):
    class Meta:
        model = TypePrime
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TypePrimeForm, self).__init__(*args, **kwargs)