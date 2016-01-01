from django import forms

class UploadFileForm(forms.Form):
	myfilefield=forms.FileField()
class UploadMapForm(forms.Form):
	mymapfield=forms.FileField()
class UploadReduceForm(forms.Form):
	myreducefield=forms.FileField()
