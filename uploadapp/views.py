from django.shortcuts import render
from django.core.mail import send_mail
from .forms import UploadFileForm
import pandas as pd

def handle_uploaded_file(f):
    data = pd.read_excel(f)

    summary = data.groupby(['Cust State', 'Cust Pin'])['DPD'].sum().reset_index()
    summary_html = summary.to_html(index=False, classes='summary-table')

    return summary_html

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            summary = handle_uploaded_file(request.FILES['file'])
            return render(request, 'uploadapp/success.html', {'summary': summary})
    else:
        form = UploadFileForm()
    return render(request, 'uploadapp/upload.html', {'form': form})

