import requests,uuid,xmltodict,json,base64,urllib.parse
from requests.sessions import Session
class RechargeResponse():
    def __init__(self,data):
        if data.get('rechargeResponse') != None:
            if data["rechargeResponse"]["status"] == "true":
                self.status = True
            else:
                self.status = False
            self.requestId = data["rechargeResponse"]["requestId"]
        else:
            raise("An expected error in server response : " + data)
class SubmitResponse():
    def __init__(self,data):
        if data.get("submitResponse") != None:
            if data["submitResponse"]["status"] =="true":
                self.status = True
            else : 
                self.status = False
            self.orderId = data["submitResponse"]["orderId"]
        else:
            raise("An expected error in server response : " + data)
class Gift:
    def __init__(self,gift_units,gift_number,is_redeemed,is_today_gift):
        self.value = gift_units
        self.day  = gift_number
        self.today_gift = is_today_gift
        if is_redeemed == "FALSE":
            self.redeemed = False
        else :
            self.redeemed = True
        if is_today_gift == "FALSE":
            self.today_gift = False
        else :
            self.today_gift = True
    def __str__(self):
        return self.value + ";"+self.day + ";"+str(self.redeemed)+";"+str(self.today_gift)     
class Constants:
    application_password="ZFZyqUpqeO9TMhXg4R/9qs0Igwg="
    build_number="502"
    app_version="22.10.0"
    device_name="Iphone 13 pro"
    API_ENDPOINT="https://mab.etisalat.com.eg:11003"
class Etisalat(object):
    headers = {
    "applicationVersion":"2",
    "Content-Type":"text/xml;charset=UTF-8",
    "applicationName":"MAB",
    "Accept":"text/xml",
    "applicationPassword":Constants.application_password,
    "APP-BuildNumber":Constants.build_number,
    "APP-Version":"22.10.0",
    "OS-Type":"Android",
    "OS-Version":"7.0",
    "APP-STORE":"GOOGLE",
    "Is-Corporate":"false",
    "Host":"mab.etisalat.com.eg:11003",
    "Connection":"Keep-Alive",
    "Accept-Encoding":"gzip",
    "User-Agent":"okhttp/3.12.8",
    "ADRUM_1":"isMobile:true",
    "ADRUM":"isAjax:true"
    }
    access_token = ""
    def __init__(self, phone,device_id = None,device_name = Constants.device_name,platform = "IOS",os_version="15"):
        self.phone = phone[1:]
        self.device_id = device_id
        self.device_name = device_name 
        self.platform = platform
        self.os_version = os_version
        self.device_id = "tarookissexyguy699"
        self.gifts = []
    def xmltojson(self,xml):
        return json.loads(json.dumps(xmltodict.parse(xml,encoding='utf-8'),ensure_ascii=False).encode('utf-8')) 
    def sendverificationcode(self):
        return self.xmltojson(requests.get(Constants.API_ENDPOINT+f"/Saytar/rest/quickAccess/sendVerCodeQuickAccessV2?sendVerCodeQuickAccessRequest=<sendVerCodeQuickAccessRequest><udid>{self.device_id}</udid><dial>{self.phone}</dial></sendVerCodeQuickAccessRequest>",headers=self.headers).text)
    def session_login(self,session):
        self.headers["Authorization"] = "Basic " +  session
        self.access_token = session
        response = requests.post(Constants.API_ENDPOINT + "/Saytar/rest/quickAccess/loginQuickAccessWithPlan",data=f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><loginWlQuickAccessRequest><firstLoginAttempt>true</firstLoginAttempt><modelType>{self.device_name}</modelType><osVersion>{self.os_version}</osVersion><platform>{self.platform}</platform><wlUdid>{self.device_id}</wlUdid></loginWlQuickAccessRequest>",headers=self.headers)
        self.session = response.cookies["JSESSIONID"]
        self.headers["cookie"] = "JSESSIONID=" + self.session +";"
        data = self.xmltojson(response.text)["loginResponseWithPlan"]
        self.user_info = data
        self.account_number = data["accountNumber"]
        self.account_id     = data["accountId"]
        self.plan_name = data["planName"]
        data = self.__get(f"/Saytar/rest/account/profile?req=<getCustomerProfileV4Request><nativeToken/><firstLoginAttempt>true</firstLoginAttempt><serviceClass>2094</serviceClass><thirdPartyType>firebase</thirdPartyType><versionNum>22.10.1</versionNum><billingProfileId>1-31DW-1861</billingProfileId><language>2</language><accountNumber>{self.account_number}</accountNumber><deviceId>{self.device_id}</deviceId><platform>{self.platform}</platform><versionCode>507</versionCode><deviceModelType>{self.device_name}</deviceModelType><osVersion>{self.os_version}</osVersion><notificationToken>cEcfpO9cSTCgZU-ibNyJMJ:APA91bGuTW23IvvPGzQ2CaS1tBSDdQAWDezZDLje6rJTQy4uh2R_KT-2_YyeLzmoGj0vubIZKwnMSpDBOsQDP2XdE4dzLL2FRFbpbMUTiCpzeAFB9ngfeiNucd0YhtMxGQVdVfFMa8NH</notificationToken></getCustomerProfileV4Request>")["getAccountProfileResponse"]["contracts"]["contract"]
        self.first_name = data["firstName"]
        self.last_name = data["fname"]
        self.last_name = data["lastName"]
        self.address = data["address"]
        self.plan = data["ratePlan"]
        return True
    def loginwithcode(self,user_code):
        data = self.__post('/Saytar/rest/quickAccess/verifyCodeQuickAccess',f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><verifyCodeQuickAccessRequest><dial>{self.phone}</dial><udid>{self.device_id}</udid><verCode>{user_code}</verCode></verifyCodeQuickAccessRequest>")
        if data.get("verifyCodeQuickAccessResponse",{}).get('pass') != None:
            self.account_password = data["verifyCodeQuickAccessResponse"]["pass"]
            session = self.phone+ ","+ str(self.device_id)+":"+self.account_password
            self.basic_auth  =  base64.b64encode(session.encode('utf-8')).decode('ascii')
            self.headers["Authorization"] = "Basic " +  self.basic_auth
            print(self.basic_auth)
            for x in range(10):
                response = requests.post(Constants.API_ENDPOINT + "/Saytar/rest/quickAccess/loginQuickAccessWithPlan",data=f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><loginWlQuickAccessRequest><firstLoginAttempt>true</firstLoginAttempt><modelType>{self.device_name}</modelType><osVersion>{self.os_version}</osVersion><platform>{self.platform}</platform><wlUdid>{self.device_id}</wlUdid></loginWlQuickAccessRequest>",headers=self.headers)
                if "JSESSIONID" in response.cookies:
                    self.session = response.cookies["JSESSIONID"]
                    self.headers["cookie"] = "JSESSIONID=" + self.session +";"
                    data = self.xmltojson(response.text)["loginResponseWithPlan"]
                    self.user_info = data
                    self.account_number = data["accountNumber"]
                    self.account_id     = data["accountId"]
                    self.plan_name = data["planName"]
                    data = self.__get(f"/Saytar/rest/account/profile?req=<getCustomerProfileV4Request><nativeToken/><firstLoginAttempt>true</firstLoginAttempt><serviceClass>2094</serviceClass><thirdPartyType>firebase</thirdPartyType><versionNum>22.10.1</versionNum><billingProfileId>1-31DW-1861</billingProfileId><language>2</language><accountNumber>{self.account_number}</accountNumber><deviceId>{self.device_id}</deviceId><platform>{self.platform}</platform><versionCode>507</versionCode><deviceModelType>{self.device_name}</deviceModelType><osVersion>{self.os_version}</osVersion><notificationToken>cEcfpO9cSTCgZU-ibNyJMJ:APA91bGuTW23IvvPGzQ2CaS1tBSDdQAWDezZDLje6rJTQy4uh2R_KT-2_YyeLzmoGj0vubIZKwnMSpDBOsQDP2XdE4dzLL2FRFbpbMUTiCpzeAFB9ngfeiNucd0YhtMxGQVdVfFMa8NH</notificationToken></getCustomerProfileV4Request>")["getAccountProfileResponse"]["contracts"]["contract"]
                    self.first_name = data["firstName"]
                    self.last_name = data["fname"]
                    self.last_name = data["lastName"]
                    self.address = data["address"]
                    self.plan = data["ratePlan"]
                    return True
                else:
                    raise("Error Key JSESSIONID is not found")
        return False
    def zero11_get(self):
        return self.__get(f"/Saytar/rest/zero11/offers?req=<dialAndLanguageRequest><subscriberNumber>{self.phone}</subscriberNumber><language>2</language></dialAndLanguageRequest>")["mabCategorizedProductsResponse"]["mabCategoryList"]
    def zero11_order(self,offer_id):
        return SubmitResponse(self.__post("/Saytar/rest/zero11/submitOrder",f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><submitOrderRequest><mabOperation></mabOperation><msisdn>{self.phone}</msisdn><operation>ACTIVATE</operation><parameters><parameter><name>GIFT_FULLFILMENT_PARAMETERS</name><value>Offer_ID:{offer_id};isRTIM:Y</value></parameter></parameters><productName>DYNAMIC_OFFERING_PAY_AND_GET_MI</productName></submitOrderRequest>"))
    def __post(self,path,data):
        return self.xmltojson(requests.post(Constants.API_ENDPOINT + path,data=data,headers=self.headers).text)
    def __get(self,path):
        return self.xmltojson(requests.get(Constants.API_ENDPOINT + path,headers=self.headers).text)
    def gettodaydailygift(self):
        gifts = []
        if self.gifts:
            gifts = self.gifts
        else : gifts = self.getdailygifts()
        for gift in gifts:
            if gift.today_gift == True:
                return gift
    def getdailygifts(self): 
        gifts  =  [] 
        for gift in self.__get(f"/Saytar/rest/dailyTipsWS/dailyTipGiftV3?req=%3CdailyTipRequest%3E%3CsubscriberNumber%3E{self.phone}%3C%2FsubscriberNumber%3E%3Clanguage%3E2%3C%2Flanguage%3E%3C%2FdailyTipRequest%3E")["dailyTipNewResponse"]["dailyLists"]["dailyList"]:
            gifts.append(Gift(gift["dailyTips"]["dailyTip"]["params"]["param"][2]["value"],gift["dayNum"],str(gift["dailyTips"]["dailyTip"]["redeemed"]),gift["dailyTips"]["dailyTip"]["todayGift"]))
        self.gifts = gifts
        return gifts
    def claimtodaygift(self):
        return SubmitResponse(self.__post(f"/Saytar/rest/dailyTipsWS/submitOrder",f"<dailyTipsSubmitRequest><operationId>REDEEM</operationId><params><param><name>GIFT_ID</name><value>{self.gettodaydailygift().day}</value></param><param><name>CATEGORY</name><value>DAILY_TIPS_NEW</value></param></params><productId>DAILY_TIPS_GIFT</productId><subscriberNumber>{self.phone}</subscriberNumber></dailyTipsSubmitRequest>"))
    def getbalance(self):
        return self.__get(f"/Saytar/rest/servicemanagement/getGenericConsumptions?requestParam=<dialAndLanguageRequest><subscriberNumber>{self.phone}</subscriberNumber><language>2</language></dialAndLanguageRequest>")["getConsumptionResponse"]["balance"]
    def scratchcard(self,voucher):
        return RechargeResponse(self.__post(f"/Saytar/rest/digitalIncentive/recharge",data=f"<?xml version='1.0' encoding='UTF-8' standalone='yes' ?><rechargeRequest><damagedFlag>false</damagedFlag><serialNumber></serialNumber><subscriberNumber>{self.phone}</subscriberNumber><voucherNumber>{voucher}</voucherNumber></rechargeRequest>"))

