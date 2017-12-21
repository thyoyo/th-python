from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail
import platform


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, cc=None, **kwargs):
    if not isinstance(to, list):
        to = [to]
    if cc is not None and not isinstance(cc, list):
        cc = [cc]
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=to, cc=cc)
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    sys_str = platform.system()
    if sys_str == "Windows":
        image1_path = 'E:\workspaces\img\email_background1.png'
    elif sys_str == "Linux":
        image2_path = '/data/project/email_background2.png'
    else:
        image1_path = None
        image2_path = None

    if image1_path is not None:
        with app.open_resource(image1_path) as fp:
            msg.attach("image.png", "image/png", fp.read(), 'inline', headers=[('Content-ID', 'image1')])

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
