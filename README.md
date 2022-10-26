# Etpy | MyEtisalat Reverse Engineering
Etpy is a Reverse Engineering of MyEtisalat Masr android application
with this package you can control your etisalat number including cash wallet with python
```python
from etpy import Client
client = Client("011xxxxxxxx") # here you must put your etisalat phone number
client.send_verification_code() # We are using this function to send verification code to procced the login request
client.login_with_code(input("Code ?  : ")) # here you must enter the verification code recevied on your phone
print(client.getbalance()) # Printing User Balance
```
### Saving Session 
```python
print(client.access_token) # printing current user session
```
### Login with Saved Session
```python
client.session_login("xxxxxxxxxxxxxxxxxxxxxxxxxx....")
```
### Using Etisalat Cash Functions 
```python
client.cash_login("your cash wallet pincode") 
client.generate_online_shopping_card(1)  # Generating Online Card with x limit
client.cash_card_online_deposit(amount,"pan","expire-month","expire-year(2 digits only)","cvv") # Deposit Wallet With Credit Card (Still Developing)
client.cash_transfer("phone-number","amount-to-transfer") # transfer cash to any meeza wallet in egypt
client.wait_for_cash() # Wait for x amount and once amount is received the function will releasd
```

## Installing Etpy
```console
$ python -m pip install etpy
```
## Supported Features
- OTP Login
- Session Login 
- Getting User Balance
- Rechage User Balance ``using scrach card``
- Getting Daily Gifts
- Redeeming Daily Gifts
- Getting Call Log 
- Getting Calling Numbers
- Getting ``011`` Offers
- Redeeming ``011`` Offers
- Cash Features
 - Getting Balance
 - Money Transfer
 - Waiting For Cash Payment
 - Getting Transcation History
### To do list
- Getting User usage and subscriptions
- Out of credit Service
    - Sallefny 3la nota 
    - Megabytes 3al nota
- Cash
    - ~~Balance Rechrage~~ (done)
    - ~~Generating Online Payments Cards~~ (done)
    - ~~Cash Out~~ (done)
    - Purchase 
    - Bank to Wallet
 





