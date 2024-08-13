import ssl
import smtplib
import secrets
from email.header import Header
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def otpToken() -> int:
    otp = secrets.randbelow(9999999)

    while True:
        otp = secrets.randbelow(9999999)

        if len(str(otp)) == 7:
            otp = secrets.randbelow(9999999)
            break

    return otp


@app.route("/api/send_otp", methods=["POST"])
def sendEmail():
    try:
        request_data = request.get_json()
        if request.method == "POST":
            otp: int = otpToken()

            sender = request_data["sender"]
            password = request_data["password"]
            receipient = request_data["receipient"]
            custom_name = request_data["custom_name"]

            email_message = MIMEMultipart()
            email_message["From"] = formataddr((str(Header(custom_name, "utf-8")), sender))
            email_message["Subject"] = "Email Verification"
            email_message["To"] = receipient

            html_content = render_template("email.html", otp=otp)
            body = MIMEText(html_content, "html", "utf-8")

            email_message.attach(body)
            context = ssl.create_default_context()

            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.ehlo()
                    server.starttls(context=context)
                    server.ehlo()
                    server.login(sender, password)
                    server.sendmail(sender, receipient, email_message.as_string())

                    return {"message": "sent", "otp": str(otp), "to": receipient}, 200
            except Exception as error:
                return {"message": "failed", "error": str(error)}, 422
    except Exception as error:
        return {"message": "failed", "error": str(error)}, 500


if __name__ == "__main__":
    app.run(debug=True)
