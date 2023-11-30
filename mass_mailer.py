import smtplib
import os,time, getpass
from string import Template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor
# import sqlite3

options = webdriver.ChromeOptions()
options.add_argument('--headless')
stream = os.popen('echo $USER')
output = stream.read()
userr=output.split('\n')[0]
options.add_argument("user-data-dir=/home/"+userr+"/.config/google-chrome/Default")
driver = webdriver.Chrome("/home/"+userr+"/Documents/chromedriver",chrome_options=options)

def get_contacts(x,y):
	"""
    Assumes Names in Column x and Emails in column y
	"""
	sheet_url = input("Google Sheet url: \t")
	driver.get(sheet_url)
	name_list=[]
	email_list=[]
	i=2
	while(1):
		driver.get("https://docs.google.com/spreadsheets/d/1W8Anx5b_PBIqAZYdUw7RiaSlfqXjvlfFgynBWPxYpSQ/edit#gid=0&range="+x+str(i))
		name=driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/div[4]/div[3]/div[4]/div/div/div").text
		time.sleep(2) # throttling
		driver.get("https://docs.google.com/spreadsheets/d/1W8Anx5b_PBIqAZYdUw7RiaSlfqXjvlfFgynBWPxYpSQ/edit#gid=0&range="+y+str(i))
		email=driver.find_element(By.XPATH, "/html/body/div[1]/div[6]/div[4]/div[3]/div[4]/div/div/div").text
		if(name==""):
			break
		if(email==""):
			break
		name_list.append(name)
		email_list.append(email)
		i += 1
		time.sleep(2)
	print("Fetched all contacts... \nStarting to send emails")
	driver.quit()
	return name_list,email_list


# set up the SMTP server
def read_template():
	filename=input("Enter template filepath : \t")
	#a sample message template is there in the directory
	with open(filename, 'r', encoding='utf-8') as template_file:
		template_file_content = template_file.read()
		return Template(template_file_content)
	
def send_email(name, email, my_email, password, subject, message_template):
    try:
		# s = smtplib.SMTP(host='smtp.gmail.com', port=587) 
        # use Gmail if you have allowed access to insecure apps in google accounts.
        #First time you will get error go to the link provided and allow insecure apps to access.
        #Then it will work 
        with smtplib.SMTP(host='smtp-mail.outlook.com', port=587) as s:
            s.starttls()
            s.login(my_email, password)
            
            msg = MIMEMultipart()
            message = message_template.substitute(PERSON_NAME=name.title())
            print(message)
            
            msg['From'] = my_email
            msg['To'] = email
            msg['Subject'] = "[ONEMAIL BULK] " + subject
            
            msg.attach(MIMEText(message, 'plain'))
            s.send_message(msg)
        
        print(f"Email sent to {email}")
    except Exception as e:
        print(f"Error sending email to {email}: {e}")
		
def driver():
	name_list,email_list=get_contacts()
	message_template=read_template()
	
	

	# s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
	#Outlook smtp is handy,only thing is that you should have microsoft account with that email

	
	# s.starttls()
	my_email=input("Enter Sender's Email :\t")
	password = getpass.getpass(prompt="Password : \t")
	# s.login(my_email,password)
	subject = input("Enter Subject of your Email :\t")
	
	with ThreadPoolExecutor() as executor:
		futures = []
		for name, email in zip(name_list, email_list):
			future = executor.submit(send_email, name, email, my_email, password, subject, message_template)
			futures.append(future)

		# Wait for all emails to be sent
		for future in futures:
			future.result()

	# for name,email in zip(name_list,email_list):
	# 	msg=MIMEMultipart()
	# 	message=message_template.substitute(PERSON_NAME=name.title())
	# 	print(message)
	# 	msg['From'] = my_email
	# 	msg['To'] = email
	# 	msg['Subject'] = "[ONEMAIL BULK] "+subject
		
	# 	msg.attach(MIMEText(message,'plain'))
	# 	s.send_message(msg)
	# 	del msg
	# s.quit()
	
if __name__ == '__main__':
    driver()