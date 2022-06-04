import enum
from multiprocessing.sharedctypes import Value
from pydantic import BaseModel

class BalancePaymentReply:
    def __init__(self, json):
        if json["PaymentReply"].get("status") != None:
            json = json["PaymentReply"]
            self.TransactionID = json["TransactionID"]
            self.Message = json["Message"]
            self.Balance = json["Balance"]
        else:
            raise ("Invaild pincode! " + json)
class BalanceReplyModel(BaseModel):
    TransactionID:str
    Message:str
    Balance:float
class TransactionTypes(enum.Enum):
    Transfer = "Transfer"
    Bill = "Bill payment"
    VCN = "VCN"
    TopUp = "Top up"
    Utils = "Request to pay"
    SelfTopUp = "Self-Top up"
class Transaction:
    def __init__(
        self,
        TransactionID,
        TransactionName,
        TransactionDate,
        TransactionTime,
        CurrencyCode,
        Amount,
        BNumber,
        Username=None,
        TransactionType=None,
    ):
        self.TransactionID = TransactionID
        self.TransactionType = TransactionTypes(TransactionName)
        self.TransactionDate = TransactionDate
        self.CurrencyCode = CurrencyCode
        self.Amount = Amount
        self.BNumber = BNumber
        if TransactionTypes(TransactionName) == TransactionTypes.Transfer:
            self.Username = Username

    def __repr__(self):
        return f"Transaction(TransactionID = {self.TransactionID},TransactionType={self.TransactionType})"


class TransferPaymentReply:
    """
        {
      "PaymentReply": {
        "status": "true",
        "TransactionID": "203389946",
        "Result": "0",
        "Message": "Transfer successful",
        "Balance": "5.77",
        "ClientID": "1234",
        "Fees": "0.0",
        "clientID": "1234",
        "fees": "0.0"
      }
    }"""

    def __init__(
        self,
        status,
        TransactionID,
        Result,
        Message,
        Balance,
        ClientID,
        Fees,
        clientID=None,
        fees=None,
    ):
        self.status = status
        self.TransactionID = TransactionID
        self.Result = Result
        self.Message = Message
        self.Balance = Balance
        self.ClientID = ClientID
        self.Fees = Fees

    def __repr__(self):
        return f"TransferPaymentReply(status = {self.status},TransactionID = {self.TransactionID},Balance ={self.Balance})"
