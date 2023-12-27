from django.core.mail import send_mail
from django.template.loader import get_template


def send_email_captcha(username, from_email, recv_email, captcha):
    try:
        template = get_template('captcha.html')
        html_content = template.render({
            'username': username,
            'captcha': captcha
        })
        send_mail(
            subject='Skylark平台重置密码验证码',
            message=None,
            html_message=html_content,
            from_email=from_email,
            recipient_list=recv_email
        )
        return True
    except (Exception,):
        return False
