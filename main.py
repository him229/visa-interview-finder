import requests
from datetime import datetime
import time
import smtplib, ssl
import os
from dotenv import load_dotenv

dotenv_path = os.environ.get('DOTENV_PATH')
load_dotenv(dotenv_path, override=True)

EMAIL_ADD = os.environ.get('EMAIL_ADD')
EMAIL_PASS = os.environ.get('EMAIL_PASS')
URL = os.environ.get('URL')
COOKIE = os.environ.get('COOKIE')
CURRENT_DATE = os.environ.get('CURRENT_DATE')
PHONE_1 = os.environ.get('PHONE_1')
PHONE_2 = os.environ.get('PHONE_2')

print("all", all([EMAIL_ADD, EMAIL_PASS, CURRENT_DATE, COOKIE, URL, PHONE_1, PHONE_2]))
print(EMAIL_ADD, COOKIE, URL)
class Mail:
    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = EMAIL_ADD
        self.password = EMAIL_PASS
        self.carriers = {
            'att': '@mms.att.net',
            'tmobile': ' @tmomail.net',
            'verizon': '@vtext.com',
            'sprint': '@page.nextel.com'
        }

    def send(self, emails, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        for email in emails:
            msg = f"From: {self.sender_mail}\r\nTo: {email}\r\nSubject: {subject}\n\n{content}"
            result = service.sendmail(self.sender_mail, email, msg)
        service.quit()
    
    def send_text(self, numbers, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        for pair_ in numbers:
            num_, carrier = pair_["number"], self.carriers[pair_["carrier"]]
            email = f"{num_}{carrier}"
            msg = f"From: {self.sender_mail}\r\nTo: {email}\r\nSubject: {subject}\n\n{content}"
            result = service.sendmail(self.sender_mail, email, msg)
        service.quit()

url = URL

mail = Mail()

phone_numbers = [
    {
        "number": PHONE_1,
        "carrier": "verizon"
    },
    {
        "number": PHONE_2,
        "carrier": "verizon"
    },
]

payload={}

headers = {
  'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="97", "Chromium";v="97"',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'X-CSRF-Token': 'udN9U40yvVi/vqCrsVNhXMpBhQ7cV6wIeoH59Rh4nO61dGMkcDOv21xiuw4ManivdqJoMraZwYkntrURE4gYpA==',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua-platform': '"macOS"',
  'Cookie': COOKIE
}

response = requests.request("GET", url, headers=headers, data=payload)
resp_json = response.json()
print(response.status_code, response.json(), response)

# resp_json = [{'date': '2023-02-17', 'business_day': True}, {'date': '2023-02-27', 'business_day': True}, {'date': '2023-03-01', 'business_day': True}, {'date': '2023-03-03', 'business_day': True}, {'date': '2023-03-06', 'business_day': True}, {'date': '2023-03-08', 'business_day': True}, {'date': '2023-03-10', 'business_day': True}, {'date': '2023-03-13', 'business_day': True}, {'date': '2023-03-17', 'business_day': True}, {'date': '2023-03-20', 'business_day': True}, {'date': '2023-03-22', 'business_day': True}, {'date': '2023-03-24', 'business_day': True}, {'date': '2023-03-27', 'business_day': True}, {'date': '2023-03-29', 'business_day': True}, {'date': '2023-03-31', 'business_day': True}]


if response.status_code != 200:
    mail.send_text(phone_numbers, "FAILURE", f"Response code = {response.status_code}")
    print(f"FAILURE = Status code {response.status_code}")
    exit()

dates = sorted([datetime.strptime(date_["date"], '%Y-%m-%d') for date_ in resp_json])
current_date = datetime.strptime(CURRENT_DATE, '%Y-%m-%d')
if dates:
    earlier_dates = list(filter(lambda x: x <= current_date, dates))
    if earlier_dates:
        earlier_dates = [d.strftime('%m/%d/%Y') for d in earlier_dates]
        print(f"SUCCESS = Dates - {earlier_dates}")
        mail.send_text(phone_numbers, "SUCCESS", f"Appointment is available on {earlier_dates}")
