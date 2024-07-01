#Install necessary library
#pip install pytz
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
from datetime import datetime
import pytz
import threading


source_email = 'senderemail@gmail.com'
destination_email = 'receiveremail@gmail.com'

def send_instant_email(source_email, sender_password, destination_email, mail_subject, body_content):
    try:
        # Setup the MIME
        msg = MIMEMultipart()
        msg['From'] = source_email
        msg['To'] = destination_email
        msg['Subject'] = mail_subject
        
        # Attach the body with the msg instance
        msg.attach(MIMEText(body_content, 'plain'))
        
        # Creating SMTP session for sending the mail
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Using Gmail's SMTP server with TLS
        server.starttls()  # Enable STARTTLS encryption
        
        # Login with email and password
        server.login(source_email, sender_password)
        
        # Converting the multipart msg into a string
        mail_text = msg.as_string()
        
        # Sending the email
        server.sendmail(source_email, destination_email, mail_text)
        server.quit()
        print(f"Success! Email successfully sent to {destination_email}.")
    
    except smtplib.SMTPAuthenticationError:
        print("Failed to send email: Authentication error. Please check your email and password or use an app-specific password.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def schedule_email(source_email, sender_password, destination_email, mail_subject, body_content, scheduled_time_str):
    ist_timezone = pytz.timezone('Asia/Kolkata')
    
    # Convert the send time to IST
    try:
        scheduled_time_ist = ist_timezone.localize(datetime.strptime(scheduled_time_str, '%Y-%m-%d %H:%M:%S'))
    except ValueError:
        print("Incorrect time format. Please use YYYY-MM-DD HH:MM:SS")
        return
    
    curr_ist_time = datetime.now(ist_timezone)
    
    
    print(f"Current IST time: {curr_ist_time}")
    print(f"Scheduled IST time: {scheduled_time_ist}")
    
    delay = (scheduled_time_ist - curr_ist_time).total_seconds()
    
    if delay < 0:
        print("Send time(scheduled) is in the past. Please provide a future time.")
        return
    
    print(f'Email scheduled to be sent at {scheduled_time_ist} (IST)')
    threading.Timer(delay, send_instant_email, args=[source_email, sender_password, destination_email, mail_subject, body_content]).start()

# Main loop for scheduling emails
while True:
    # input from the user
    sender_password = getpass.getpass("Please enter your email account password:  ")
    destination_email = input("Please provide the recipient's email address: ")
    mail_subject = input("Enter the subject of the email: ")
    body_content = input("Enter the body of the email: ")
    
    # Email Preview
    print("\n--- Email Preview ---")
    print(f"From: {source_email}")
    print(f"To: {destination_email}")
    print(f"Subject of the Email: {mail_subject}")
    print(f"Body:\n{body_content}")
    print("\n************************\n")
    
    confirm_send = input("Do you want to send or schedule this email? (send/schedule): ").strip().lower()
    
    if confirm_send == 'send':
        send_instant_email(source_email, sender_password, destination_email, mail_subject, body_content)
    elif confirm_send == 'schedule':
        scheduled_time_str = input("Enter the scheduled send time in IST (YYYY-MM-DD HH:MM:SS): ")
        schedule_email(source_email, sender_password, destination_email, mail_subject, body_content, scheduled_time_str)
    else:
        print("Invalid input. Please enter 'send' or 'schedule'.")
    
    schedule_another = input("Do you want to schedule another email? (yes/no): ").strip().lower()
    if schedule_another != 'yes':
        print("Thank you for using Automated Email Sender")
        break
