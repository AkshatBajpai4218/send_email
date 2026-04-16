# Gmail SMTP Setup Guide

Gmail does **not** allow regular account passwords for third-party apps like Django. You must use an **App Password** instead.

## Steps to Generate a Gmail App Password

### 1. Enable 2-Factor Authentication (Required)
- Go to [Google Account Security](https://myaccount.google.com/security)
- Sign in if prompted
- In the left menu, click **Security**
- Ensure "2-Step Verification" is **enabled**
  - If not, click "2-Step Verification" and follow the prompts

### 2. Create an App Password
- Go back to [Google Account Security](https://myaccount.google.com/security)
- Scroll down and find **App passwords** (only appears if 2FA is enabled)
- Select **Mail** and **Windows Computer** (or your device type)
- Google will generate a 16-character password
- **Copy this password exactly as shown** (with spaces removed if any)

Example: `abc defg hij klmn` → use as `abcdefghijklmn`

### 3. Set Environment Variables in PowerShell

Open PowerShell **in the project folder** and run:

```powershell
$env:EMAIL_HOST = "smtp.gmail.com"
$env:EMAIL_PORT = "587"
$env:EMAIL_USE_TLS = "True"
$env:EMAIL_HOST_USER = "your_email@gmail.com"
$env:EMAIL_HOST_PASSWORD = "your_app_password_here"
$env:DEFAULT_FROM_EMAIL = "your_email@gmail.com"
```

Replace:
- `your_email@gmail.com` with your actual Gmail address
- `your_app_password_here` with the 16-character App Password from step 2

### 4. Start the Django Server

```powershell
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser and test sending an email.

## Troubleshooting

### "Authentication failed" error
- Double-check that you used the **App Password**, not your regular Gmail password
- Ensure 2-Factor Authentication is enabled on your account
- Verify you copied the password correctly (remove any spaces)

### "Bad credentials" (535 error)
- This is the same as above—you need to use an App Password, not a regular password

### "Connection refused" error
- Check that `EMAIL_HOST` is `smtp.gmail.com`
- Check that `EMAIL_PORT` is `587`
- Ensure `EMAIL_USE_TLS` is `True`

### Environment Variables Not Persisting
PowerShell environment variables only persist during the current session. To make them permanent:

1. Search for "Environment Variables" in Windows Start menu
2. Click "Edit the system environment variables"
3. Click "Environment Variables" button
4. Add your email variables under "User variables"
5. Restart PowerShell after adding

## Alternative: Using .env File (Optional)

If you prefer not to use environment variables every time, create a `.env` file in the project root:

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

Then modify `settings.py` to load from `.env`:

```python
from dotenv import load_dotenv

load_dotenv()
```

Install python-dotenv:
```powershell
pip install python-dotenv
```

## Using a Different Email Provider

If you want to use a different SMTP provider (Outlook, Yahoo, SendGrid, etc.), change the `EMAIL_HOST`:

- **Outlook/Hotmail**: `smtp.office365.com` (port 587)
- **Yahoo Mail**: `smtp.mail.yahoo.com` (port 587, requires App Password)
- **SendGrid**: `smtp.sendgrid.net` (port 587, username: `apikey`)
- **Mailgun**: `smtp.mailgun.org` (port 587)

## Security Note

**⚠️ Never commit passwords or SMTP credentials to version control.**

- Use environment variables or `.env` (add `.env` to `.gitignore`)
- Never hardcode credentials in `settings.py`
- Regenerate App Passwords if they're ever exposed
