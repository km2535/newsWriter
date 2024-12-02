import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import os

def send_email(subject, body):
    sender_email = os.getenv("SENDER_EMAIL")  # 발신자 이메일 (환경 변수에서 가져옴)
    sender_name = os.getenv("SENDER_NAME", "News Bot")  # 발신자 이름
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")  # SMTP 서버 주소
    smtp_port = int(os.getenv("SMTP_PORT", 587))  # SMTP 포트 (기본: 587)
    smtp_password = os.getenv("SMTP_PASSWORD")  # 발신자 이메일 비밀번호
    recipient_email = os.getenv('RECIPIENT_EMAIL')
    # 이메일 메시지 생성
    msg = MIMEMultipart("alternative")
    msg["From"] = formataddr((sender_name, sender_email))
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # HTML 형식의 이메일 본문 추가
    msg.attach(MIMEText(body, "html"))

    try:
        # SMTP 서버 연결
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # TLS 시작
            server.login(sender_email, smtp_password)  # 로그인
            server.sendmail(sender_email, recipient_email, msg.as_string())  # 이메일 발송
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
