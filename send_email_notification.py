import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_notification(sender_email, sender_password, receiver_email, medium_post_link):
    """
    이메일 알림을 보내는 함수.

    Args:
        sender_email (str): 발신자 이메일 주소
        sender_password (str): 발신자 이메일 비밀번호
        receiver_email (str): 수신자 이메일 주소
        medium_post_link (str): 게시된 Medium 게시물 링크

    Returns:
        None
    """
    subject = "New Medium Post Published"
    body = f"A new post has been published on Medium: {medium_post_link}"

    # 이메일 메시지 구성
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # SMTP 서버 설정 및 이메일 전송
    try:
        with smtplib.SMTP("smtp.example.com", 587) as server:  # SMTP 서버 주소와 포트 수정 필요
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")

