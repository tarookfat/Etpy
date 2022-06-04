from pydoc import cli
from app import Etisalat
import json

client = Etisalat("01159823703")
status = client.send_verification_code()
print(status)
print(status.status)
client.login_with_code(input("User Verification Code : "))
print(client.save_session)
print(client.user)
print(client.claimtodaygift())