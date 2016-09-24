import smtplib


server = smtplib.SMTP("smtp.gmail.com", 587)

server.starttls()

server.login('olireza1996@gmail.com', 'Aspire2inspire')

server.sendmail('olireza1996"gmail.com','alireza.bahremand@outlook.com', 'Test message')
