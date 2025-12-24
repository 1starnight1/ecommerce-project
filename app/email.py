from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject=subject,
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    # 异步发送
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_order_confirmation(order, user):
    send_email(
        user.email,
        '订单确认 - ' + order.order_number,
        'email/order_confirmation',
        order=order,
        user=user
    )