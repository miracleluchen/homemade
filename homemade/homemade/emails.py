# -*- coding: utf-8 -*-
import smtplib
import mimetypes
from email import Encoders
from email.Encoders import encode_base64
from email.MIMEAudio import MIMEAudio
from email.MIMEBase import MIMEBase
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.utils import COMMASPACE

from xml.dom import minidom
from xml.dom.minidom import Document

import os
import httplib
import urllib
import urlparse
import hashlib
import time
import json
import sys
import datetime
import traceback
from django.conf import settings

def send_sendgrid(from_addr, to_addrs, mime): 
    try:
        # smtp.dev.garenanow.com:465.
        server = smtplib.SMTP('smtp.dev.garenanow.com', 465)
        server.ehlo()
        server.sendmail(from_addr, to_addrs, mime.as_string())
        server.quit()
    except:
        traceback.print_exc(file=sys.stdout)
        return False
    return True 

def get_attachment(attachment_file_path):
    content_type, encoding = mimetypes.guess_type(attachment_file_path)
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    file = open(attachment_file_path, 'rb')
    if main_type == 'text':
        attachment = MIMEText(file.read())
    elif main_type == 'message':
        attachment = email.message_from_file(file)
    elif main_type == 'image':
        attachment = MIMEImage(file.read(),_sub_type=sub_type)
    elif main_type == 'audio':
        attachment = MIMEAudio(file.read(),_sub_type=sub_type)
    else:
        attachment = MIMEBase(main_type, sub_type)
        attachment.set_payload(file.read())
        encode_base64(attachment)
    file.close()
    attachment.add_header(
        'Content-Disposition', 
        'attachment',     
        filename=os.path.basename(attachment_file_path)
    )
    return attachment    

def send_mail(subject, msg, from_addr, to_addrs, cc_addrs=[], bcc_addrs=[], attachments=[], func=send_sendgrid, *a, **b):
    if not settings.ENABLE_EMAIL:
        return True
    mime = MIMEMultipart()
    
    to_addrs_final = []
    if settings.ENABLE_TEST_EMAIL:
        for addr in to_addrs:
            if addr in settings.TEST_EMAIL_ACCOUNT:
                to_addrs_final.append(addr)
    else:
        to_addrs_final = to_addrs

    mime['From'] = from_addr
    mime['To'] = ', '.join(to_addrs_final)
    if len(cc_addrs) > 0:
        mime['Cc'] = ', '.join(cc_addrs)
    if len(bcc_addrs) > 0: 
        mime['Bcc'] = ', '.join(bcc_addrs)
        
    mime['Subject'] = subject
    body = MIMEText(msg, _subtype='html', _charset='utf-8')
    mime.attach(body)
    
    for file_name in attachments:
        mime.attach(get_attachment(file_name))
    
    _to_addrs = to_addrs_final + cc_addrs + bcc_addrs
    result = func(from_addr, _to_addrs, mime)
    return result

def send_verification_email(to_addrs):
    mail_subject = "%s Information Update Validation Request" % settings.EMAIL_PREFIX
    mail_from = settings.REPORT_EMAIL_FROM
    mail_to = to_addrs
    mail_text = 'There is some information updates request, please click <a href="%s#/validate">here</a> to take a look.' % settings.HRIS_DOMAIN
    return send_mail(mail_subject, mail_text, mail_from, mail_to)

def send_verification_approve_email(to_addrs, staff_id):
    mail_subject = "%s Information Update Approval Notification" % settings.EMAIL_PREFIX
    mail_from = settings.REPORT_EMAIL_FROM
    mail_to = to_addrs
    mail_text = 'Your update request has been approved, please click <a href="%s#/detail/%s">here</a> to view your profile.' % (settings.HRIS_DOMAIN, staff_id)
    return send_mail(mail_subject, mail_text, mail_from, mail_to)

def send_verification_reject_email(to_addrs, staff_id):
    mail_subject = "%s Information Update Reject Notification" % settings.EMAIL_PREFIX
    mail_from = settings.REPORT_EMAIL_FROM
    mail_to = to_addrs
    mail_text = 'Your update request has been rejected, please click <a href="%s#/detail/%s">here</a> to view your profile.' % (settings.HRIS_DOMAIN, staff_id)
    return send_mail(mail_subject, mail_text, mail_from, mail_to)

def send_share_request_email(to_addrs, requester, tree_name, target):
    mail_subject = "%s Function Tree Share Request" % settings.EMAIL_PREFIX
    mail_from = settings.REPORT_EMAIL_FROM
    mail_to = to_addrs
    mail_text = '%s would like to share tree %s to %s, approve, reject.' % (requester, tree_name, target)
    return send_mail(mail_subject, mail_text, mail_from, mail_to)
