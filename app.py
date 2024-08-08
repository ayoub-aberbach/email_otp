import ssl
import smtplib
import secrets
from email.header import Header
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def otpToken() -> int:
    otp = secrets.randbelow(9999999)

    while True:
        otp = secrets.randbelow(9999999)

        if len(str(otp)) == 7:
            otp = secrets.randbelow(9999999)
            break

    return otp


def sendEmail(receiver_email: str, sender_email: str, sender_email_password: str):
    try:
        if receiver_email and sender_email and sender_email_password:
            otp: int = otpToken()

            email_message = MIMEMultipart()
<<<<<<< HEAD
            #  change AppName to whatever you like
            email_message["From"] = formataddr((str(Header("AppName", "utf-8")), request_data["sender_email"]))
            email_message["To"] = request_data["receiver_email"]
=======
            email_message["From"] = formataddr((str(Header("AppName", "utf-8")), sender_email))
            email_message["To"] = receiver_email
>>>>>>> d034c80033a95e06baacdb55ab57fa012eb35c6a
            email_message["Subject"] = "Email Verification"

            body1 = MIMEText(
                """<center><div style="width: auto;"><table role="presentation" width="100%" border="0" style="padding: 10px; border-collapse: collapse;"><tr><td style="text-align: center;"><div style="font-family: Helvetica, Arial, sans-serif; width: auto; overflow: hidden; line-height: 2;"><div style="margin: 0 auto; width: auto; padding: 10px; border-bottom: 1px solid #ddd; display: inline-block;"><p style="margin: 0; font-size: 16px">""",
                "html",
                "utf-8",
            )
            body2 = MIMEText(str(otp), "plain")
            body3 = MIMEText("""</p></div></div></td></tr></table></div></center>""", "html", "utf-8")

            email_message.attach(body1)
            email_message.attach(body2)
            email_message.attach(body3)

            context = ssl.create_default_context()

            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.ehlo()
                    server.starttls(context=context)
                    server.ehlo()
                    server.login(sender_email, sender_email_password)
                    server.sendmail(sender_email, receiver_email, email_message.as_string())

<<<<<<< HEAD
                    return {"message": "sent", "otp": str(otp), "to": request_data["receiver_email"]}, 200
            except Exception as error:
                return {"message": "failed", "error": str(error)}, 422
    except Exception as error:
        return {"message": "failed", "error": str(error)}, 500
=======
                    return {"message": "sent", "otp": str(otp), "to": receiver_email}
            except Exception as error:
                return {"message": "failed", "error": str(error)}
    except Exception as error:
        return {"message": "failed", "error": str(error)}
>>>>>>> d034c80033a95e06baacdb55ab57fa012eb35c6a


if __name__ == "__main__":
    print(sendEmail("""receiver_email""", """sender_email""", """sender_email_password"""))
