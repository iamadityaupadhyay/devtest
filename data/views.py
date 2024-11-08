from django.shortcuts import render
import pandas as pd
import pandas as pd
from django.core.mail import send_mail
from django.shortcuts import render,redirect
from django.conf import settings


def home(request):
    if request.method=="POST":
        file=request.FILES['file']
        # since it is a excel file so I am converting it to pandas dataframe
        excel_data = pd.ExcelFile(file)
        # since it is excel file I decided to directly perform actions on it and not making any object in the db
        # reading sheet 1st
        
        sheet1_data = excel_data.parse('Sheet1')
        sheet1_summary = {
            "Total Rows": len(sheet1_data),
            # now getting the unique states
            "Unique States": sheet1_data['Cust State'].nunique(),
            "Date Range": f"{sheet1_data['Date'].min()} to {sheet1_data['Date'].max()}",
            "DPD Statistics": sheet1_data['DPD'].describe().to_dict()
        }

        # reading sheet 2nd
        sheet2_data = excel_data.parse('Sheet2')
        sheet2_data_cleaned = sheet2_data.iloc[2:].copy()
        sheet2_data_cleaned.columns = ['ID', 'Code', 'Cust State', 'Cust Pin', 'DPD']
        sheet2_data_cleaned['DPD'] = pd.to_numeric(sheet2_data_cleaned['DPD'], errors='coerce')

        sheet2_summary = {
            "Total Rows": len(sheet2_data_cleaned),
            "Unique States": sheet2_data_cleaned['Cust State'].nunique(),
            "DPD Statistics": sheet2_data_cleaned['DPD'].describe().to_dict()
        }
       
        summary_text = f"""
        Sheet1 Summary:
        Total Rows: {sheet1_summary['Total Rows']}
        Unique States: {sheet1_summary['Unique States']}
        Date Range: {sheet1_summary['Date Range']}
        DPD Statistics: {sheet1_summary['DPD Statistics']}

        Sheet2 Summary:
        Total Rows: {sheet2_summary['Total Rows']}
        Unique States: {sheet2_summary['Unique States']}
        DPD Statistics: {sheet2_summary['DPD Statistics']}
        """
        request.session['summary_text'] = summary_text   
        return redirect('/view/') 
    return render(request,'home.html')     #this is the page that will be displayed when the user goes to the home page.
def view(request):
    summary_text = request.session.get('summary_text')
    return render(request,'view.html',{'summary_text':summary_text})
from django.core.mail import EmailMessage
def send_emaill(request):
    summary_text = request.session.get('summary_text')
    subject = 'Python Assignment - Aditya Upadhyay'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = ['tech@themedius.ai']
    bcc_email = ['iam18aditya@gmail.com'] 

    email = EmailMessage(
        subject=subject,
        body=summary_text,
        from_email=from_email,
        to=to_email,
        bcc=bcc_email
    )

 
    email.send(fail_silently=False)
    print("Subject:", subject)
    print("To:", to_email)
    print("BCC:", bcc_email)
    print("Body:", summary_text)
    print("=====================")
    summary_text=request.session["summary_text"]
    message={
        "message":"Email sent successfully",
        "summary_text":summary_text
    }
    return render(request,'view.html',message)
    