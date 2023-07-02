Indian banks like stanc send me pdf statements in email which are password protected. I like to download statements every now and then for posterity and this is a quick script to help me fetch and decrypt the statements in bulk from my gmail account.

To run:

```
brew install qpdf
pyenv virtualenv env
pyenv activate env
pip install -r requirements.txt
ACCT4=1111 python download_stmt.py # put last for of your account number
ACCT4=1111 PDFPASS=some_password bash unlock.sh 2022
```

Notes:
This is an unverified app/project. Google will show you a trust warning on OAuth flow, approve at your discretion!
