import smtplib, ssl

port = 587  
smtp_server = "smtp.gmail.com"
sender_email = "fromemail@gmail.com"
receiver_email = "toemail@gmail.com"
password = 'yourpassword'

def send_email_to_user(data, date_range):

    SUBJECT = 'COVID Vaccine available: ' + date_range
    TEXT = data
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

    return True