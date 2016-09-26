import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class emailPictures:
    
    def SendMail(self, ImgFileName):
        img_data = open(ImgFileName, 'rb').read()
        msg = MIMEMultipart()
        msg['Subject'] = 'ImageTest'
        #msg['From'] = 'olireza1996@gmail.com'
        #msg['To'] = 'alireza.bahremand@outlook.com'

        text = MIMEText("test")
        msg.attach(text)
        image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
        msg.attach(image)
        From = 'olireza1996@gmail.com'
        To = 'alireza.bahremand@outlook.com'
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login('olireza1996@gmail.com', 'Aspire2inspire')
        s.sendmail(From, To, msg.as_string())
        s.quit()

    # Since we are calling the SendMail method from a different file we don't want
    # to have a main method that will be executing.
    #if __name__ == '__main__':
        # Fill info...
        #SendMail("Snapshots/tstpic.jpg")

