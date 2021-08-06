from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_email(user, request, mail_subject, message_template):
    current_site = get_current_site(request)

    message = render_to_string(message_template, {
        'domain': current_site.domain,
        'pk': user.id,
        'token': default_token_generator.make_token(user),
    })

    EmailMessage(
        mail_subject,
        message,
        to=(user.email,)
    ).send()
