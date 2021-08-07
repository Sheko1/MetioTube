# MetioTube django template app

## Overview
MetioTube is a web app where you can share video content with others.

Authenticated users can upload, like, dislike and post comments.

Unauthenticated users can only view the created content.

**How to make an account?**

If you make account through /auth/register your account will not be activated.

To activate your account, you need to click on the activation link, which will be sent to the email you registered.

[Setup your gmail to work with MetioTube](#usage)

Or you can make account with manage.py, where the created account will be activated without email confirmation.

## Installation
**First**
```bash
git clone https://github.com/Sheko1/MetioTube
```
**Then**

```bash
pip install -r requirements.txt
```

## Usage
Change django secret key in settings.py.
```python
SECRET_KEY = os.environ['DJANGO_SECRET_KEY'] # - change to valid secret key
```
- In order to use email confirmation and password reset, you need a gmail account.
- Then change email and email password in settings.py

```python
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ['EMAIL'] # - change to your email
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD'] # - change to your password
EMAIL_PORT = 587
```
### Note!!
You must [**allow** less secure apps](https://myaccount.google.com/lesssecureapps) in your gmail account and [display unlock captcha](https://www.google.com/accounts/DisplayUnlockCaptcha)

Change database credentials.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB'], # - your postgres database
        'USER': os.environ['DB_USER'], # - your postgres username
        'PASSWORD': os.environ['DB_PASSWORD'], # - your postres password
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```
or use default database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## License
[MIT](https://github.com/Sheko1/MetioTube/blob/main/LICENSE)
