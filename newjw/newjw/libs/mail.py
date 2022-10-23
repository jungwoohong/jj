from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def mailSend(frm,to,subject,content):
    message = Mail(
        from_email=frm,
        to_emails=to,
        subject=subject,
        html_content=content)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        print("mail false")