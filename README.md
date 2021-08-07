# MetioTube django template app


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
- In order to use email confirmation and password reseting you need to have gmail account.
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

## License
[MIT](https://github.com/Sheko1/MetioTube/blob/main/LICENSE)
