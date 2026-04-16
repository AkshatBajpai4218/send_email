from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from smtplib import SMTPAuthenticationError

from .forms import EmailForm


def send_email_view(request):
	form = EmailForm(request.POST or None)

	if request.method == "POST" and form.is_valid():
		to_email = form.cleaned_data["to_email"]
		subject = form.cleaned_data["subject"]
		message = form.cleaned_data["message"]

		if not settings.EMAIL_HOST_USER:
			messages.error(
				request,
				"EMAIL_HOST_USER is not configured. Please set it as an environment variable.",
			)
		elif not settings.EMAIL_HOST_PASSWORD:
			messages.error(
				request,
				"EMAIL_HOST_PASSWORD is not configured. Please set it as an environment variable.",
			)
		else:
			try:
				send_mail(
					subject=subject,
					message=message,
					from_email=settings.DEFAULT_FROM_EMAIL,
					recipient_list=[to_email],
					fail_silently=False,
				)
				messages.success(request, "Email sent successfully!")
				form = EmailForm()
			except SMTPAuthenticationError:
				messages.error(
					request,
					"Authentication failed. For Gmail: use an App Password, not your regular password. "
					"See GMAIL_SETUP.md for detailed instructions.",
				)
			except Exception as e:
				messages.error(request, f"Error sending email: {str(e)}")

	return render(request, "mailer/send_email.html", {"form": form})
