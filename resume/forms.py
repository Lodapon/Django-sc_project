# from django import forms

# class ResumeForm(forms.Form):
#     full_name = forms.CharField(max_length=100, label='Full Name')
#     email = forms.EmailField(label='Email Address')
#     phone_number = forms.CharField(max_length=20, required=False, label='Phone Number')
#     linkedin = forms.URLField(required=False, label='LinkedIn Profile')
#     professional_summary = forms.CharField(widget=forms.Textarea, label='Professional Summary', required=False)
#     skills = forms.CharField(widget=forms.Textarea, label='Skills')
#     experience = forms.CharField(widget=forms.Textarea, label='Work Experience')
#     education = forms.CharField(widget=forms.Textarea, label='Education')
#     certifications = forms.CharField(widget=forms.Textarea, required=False, label='Certifications')
#     projects = forms.CharField(widget=forms.Textarea, required=False, label='Projects')
#     awards = forms.CharField(widget=forms.Textarea, required=False, label='Awards')
#     languages = forms.CharField(widget=forms.Textarea, required=False, label='Languages')
#     portfolio_url = forms.URLField(required=False, label='Portfolio URL')
#     availability = forms.CharField(max_length=100, required=False, label='Availability')

from django import forms

class ResumeForm(forms.Form):
    full_name = forms.CharField(max_length=100, label='Full Name', required=False)
    email = forms.EmailField(label='Email Address', required=False)
    phone_number = forms.CharField(max_length=20, required=False, label='Phone Number')
    linkedin = forms.URLField(required=False, label='LinkedIn Profile')
    professional_summary = forms.CharField(widget=forms.Textarea, label='Professional Summary', required=False)
    skills = forms.CharField(widget=forms.Textarea, label='Skills', required=False)
    experience = forms.CharField(widget=forms.Textarea, label='Work Experience', required=False)
    education = forms.CharField(widget=forms.Textarea, label='Education', required=False)
    certifications = forms.CharField(widget=forms.Textarea, required=False, label='Certifications')
    projects = forms.CharField(widget=forms.Textarea, required=False, label='Projects')
    awards = forms.CharField(widget=forms.Textarea, required=False, label='Awards')
    languages = forms.CharField(widget=forms.Textarea, required=False, label='Languages')
    portfolio_url = forms.URLField(required=False, label='Portfolio URL')
    availability = forms.CharField(max_length=100, required=False, label='Availability')
    
    # New field for uploading a resume PDF
    resume_pdf = forms.FileField(label='Upload Resume (PDF)', required=False)
