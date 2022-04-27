import requests
import json
from datetime import datetime
from time import sleep
from threading import Thread

now = datetime.now().isoformat()
import string
import secrets

base_url = "https://testapi.kazang.net/apimanager/api_rest/v1/"
test_username = "1000631231"
test_password = "15721977"
channel = "PridePayments"
serial_number = "102.147.160.102"
time_stamp = now
auth_data = {
    "username": test_username, "password": test_password, "channel": channel
}

headers = {
    "Content-Type": "application/json"

}


def auth_client():
    r = requests.post(base_url + "authClient", data=json.dumps(auth_data), headers=headers)
    return r.json()


def get_new_session_uuid():
    session_uuid = auth_client().get('session_uuid', False)
    return session_uuid


def get_balance():
    return auth_client().get('balance', None)


def is_active_session(response):
    if response.json().get('response_code', False) == 7 or response.json().get('response_code',
                                                                               False) == 8 or response.json().get(
        'response_code', False) == 9:
        return False
    elif response.json().get('response_code', False) == 0:
        return True
    else:
        return False


session_uuid = 'dd18a959-c494-4bde-b39e-ae2479e0098d'

data = {
    "session_uuid": session_uuid
}
default_data = {
    'session_uuid': session_uuid
}


def product_list():
    default_data = {
        'session_uuid': session_uuid
    }
    r = requests.post(base_url + 'productList', data=json.dumps(data), headers=headers)
    products = r.json().get('product_list', None)
    return products


def find_product_from_method_name(method: str):
    """
    Get a product dictionary form an API method name
    :param method:
    :return dict:
    """
    products = product_list()
    return next(item for item in products if item["method_name"] == method)


def airtel_pay_payment(phone_number: str, amount):
    data = {
        "session_uuid": session_uuid
    }
    """
    Airtel Pay Payment workflow
    :param phone_number:
    :param amount:
    :return:
    """
    data['product_id'] = '5392'
    data['wallet_msisdn'] = phone_number
    data['amount'] = amount
    r = requests.post(base_url + "airtelPayPayment", data=json.dumps(data), headers=headers)
    # confirmation_number = r.json().get('confirmation_number', False)
    # data['confirmation_number'] = confirmation_number
    # result = requests.post(base_url + "airtelPayPaymentConfirm", data=json.dumps(data), headers=headers)
    # return result.json()
    return r.json()


def airtel_pay_query():
    result = ''
    airtel_reference = result.json().get('airtel_reference', False)
    data['airtel_reference'] = airtel_reference
    data['product_id'] = "5393"
    airtel_pay_query = requests.post(base_url + "airtelPayQuery", data=json.dumps(data), headers=headers)
    data['confirmation_number'] = airtel_pay_query.json().get('confirmation_number', False)
    airtel_pay_query_confirm = requests.post(base_url + "airtelPayQueryConfirm", data=json.dumps(data), headers=headers)

    return airtel_pay_query_confirm.json()


def zamtel_money_pay(phone_number: str, amount):
    data = {
        "session_uuid": session_uuid
    }
    """Zamtel Money Pay workflow"""
    data['request_reference'] = '100402'
    data['msisdn'] = phone_number
    data['amount'] = amount
    data['product_id'] = '1706'
    zamtel_money_pay = requests.post(base_url + 'zamtelMoneyPay', data=json.dumps(data), headers=headers)
    data['request_reference'] = '128001'
    data['confirmation_number'] = zamtel_money_pay.json().get('confirmation_number', None)
    zamtel_pay_confirmation = requests.post(base_url + 'zamtelMoneyPayConfirm', data=json.dumps(data), headers=headers)
    return zamtel_pay_confirmation.json()


def mtn_debit(phone_number: str, amount: float):
    data['wallet_msisdn'] = phone_number
    data['amount'] = amount
    data['product_id'] = '1612'
    r = requests.post(base_url + 'mtnDebit', data=json.dumps(data), headers=headers)
    data['supplier_transaction_id'] = r.json().get('supplier_transaction_id', None)
    data['product_id'] = '1613'
    approval = requests.post(base_url + 'mtnDebitApproval', data=json.dumps(data), headers=headers)
    data['confirmation_number'] = approval.json().get('confirmation_number', None)
    approval_confirm = requests.post(base_url + 'mtnDebitApprovalConfirm', data=json.dumps(data), headers=headers)
    return approval_confirm.json()




def all1zed_pay_for_bus(customer_phone_number, bus_owner_phone_number, customer_amount, bus_owner_amount):
    print(mtn_debit(customer_phone_number, customer_amount))
    print(mtn_cash_in(bus_owner_phone_number, bus_owner_amount))


def nfs_cash_in(phone_number, amount):
    alphabet = string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(6))
    code2 = ''.join(secrets.choice(alphabet) for i in range(6))
    data = {
        "session_uuid": session_uuid
    }
    data['product_id'] = '1648'
    data['request_reference'] = code
    data['reference'] = phone_number
    data['amount'] = amount
    cash_in = requests.post(base_url + 'nfsCashIn', data=json.dumps(data), headers=headers)
    data['confirmation_number'] = cash_in.json().get('confirmation_number', False)
    data['request_reference'] = code2
    del data['amount']
    del data['reference']
    nfs_cash_in_confirm = requests.post(base_url + 'nfsCashInConfirm', data=json.dumps(data), headers=headers)
    return nfs_cash_in_confirm.json()


def nfs_cash_out(phone_number, amount):
    alphabet = string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(6))
    code2 = ''.join(secrets.choice(alphabet) for i in range(6))
    data = {
        "session_uuid": session_uuid
    }
    data['product_id'] = '1649'
    data['request_reference'] = code
    data['reference'] = phone_number
    data['amount'] = amount
    cash_out = requests.post(base_url + 'nfsATMCashOut', data=json.dumps(data), headers=headers)
    data['data'] = '2020'
    data['data_reference_number'] = cash_out.json().get('data_reference_number', False)
    data['request_reference'] = code2
    del data['amount']
    del data['reference']
    cash_out_confirm = requests.post(base_url + 'nfsATMCashOutSubmitData', data=json.dumps(data), headers=headers)
    return cash_out_confirm.json()


def mtn_cash_in(phone_number, amount):
    alphabet = string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(6))
    code2 = ''.join(secrets.choice(alphabet) for i in range(6))
    data = {
        "session_uuid": session_uuid
    }
    data['receiving_msisdn'] = phone_number
    data['amount'] = amount
    data['product_id'] = '1608'
    data['request_reference'] = code
    cash_in = requests.post(base_url + 'mtnCashIn', data=json.dumps(data), headers=headers)
    data['data_reference_number'] = cash_in.json().get('data_reference_number', False)
    data['request_reference'] = code2
    data['data'] = phone_number
    del data['receiving_msisdn']
    del data['amount']
    cash_in_confirm = requests.post(base_url + 'mtnCashInSubmitData', data=json.dumps(data), headers=headers)
    return cash_in_confirm.json()



def zamtel_money_cash_in(phone_number, amount):
    alphabet = string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(6))
    code2 = ''.join(secrets.choice(alphabet) for i in range(6))
    data = {
        "session_uuid": session_uuid
    }
    data['product_id'] = '1665'
    data['request_reference'] = code
    data['msisdn'] = phone_number
    data['amount'] = amount
    cash_in = requests.post(base_url + 'zamtelMoneyCashIn', data=json.dumps(data), headers=headers)
    data['confirmation_number'] = cash_in.json().get('confirmation_number', False)
    data['request_reference'] = code2
    del data['msisdn']
    del data['amount']
    cash_in_confirm = requests.post(base_url + 'zamtelMoneyCashInConfirm', data=json.dumps(data), headers=headers)
    return cash_in_confirm.json()


def buy_voucher():
    alphabet = string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(6))
    code2 = ''.join(secrets.choice(alphabet) for i in range(6))
    data = {
        "session_uuid": session_uuid
    }
    data['product_id'] = find_product_from_method_name('buyVoucher')['product_id']
    data['request_reference'] = code
    voucher = requests.post(base_url + 'buyVoucher', data=json.dumps(data), headers=headers)
    return voucher.json()

def direct_recharge_airtime(phone_number, amount):
    alphabet = string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(6))
    code2 = ''.join(secrets.choice(alphabet) for i in range(6))
    data = {
        "session_uuid": session_uuid
    }
    data['product_id'] = find_product_from_method_name('directRechargeAirtime')['product_id']
    data['request_reference'] = code
    data['msisdn'] = phone_number
    data['amount'] = amount
    direct_recharge = requests.post(base_url + 'directRechargeAirtime', data=json.dumps(data), headers=headers)
    return direct_recharge.json()


def direct_recharge_data(phone_number, amount):
    alphabet = string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(6))
    code2 = ''.join(secrets.choice(alphabet) for i in range(6))
    data = {
        "session_uuid": session_uuid
    }
    # data['request_reference'] = code
    data['msisdn'] = phone_number
    data['amount'] = amount
    data['product_id'] = find_product_from_method_name('directRechargeData')['product_id']
    direct_recharge = requests.post(base_url + 'directRechargeData', data=json.dumps(data), headers=headers)
    data['confirmation_number'] = direct_recharge.json().get('confirmation_number', False)
    # data['request_reference'] = code2
    del data['msisdn']
    del data['amount']
    direct_recharge_confirm = requests.post(base_url + 'confirm', data=json.dumps(data), headers=headers)
    return direct_recharge_confirm.json()


def mtn_cash_out(phone_number, amount):
    alphabet = string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(6))
    code2 = ''.join(secrets.choice(alphabet) for i in range(6))
    code3 = ''.join(secrets.choice(alphabet) for i in range(6))
    data = {
        "session_uuid": session_uuid
    }
    data['product_id'] = '1609'
    data['request_reference'] = code
    data['receiving_msisdn'] = phone_number
    data['amount'] = amount
    cash_out = requests.post(base_url + 'mtnCashOut', data=json.dumps(data), headers=headers)
    data['supplier_transaction_id'] = cash_out.json().get('supplier_transaction_id', False)
    data['request_reference'] = code2
    data['product_id'] = '1610'
    cash_out_approval = requests.post(base_url + 'mtnCashOutApproval', data=json.dumps(data), headers=headers)
    data['confirmation_number'] = cash_out_approval.json().get('confirmation_number', False)
    data['request_reference'] = code3
    cash_out_confirm = requests.post(base_url + 'mtnCashOutApprovalConfirm', data=json.dumps(data), headers=headers)
    return cash_out_confirm.json()


def zamtel_money_cash_out(phone_number, amount):
    alphabet = string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(6))
    code2 = ''.join(secrets.choice(alphabet) for i in range(6))
    code3 = ''.join(secrets.choice(alphabet) for i in range(6))
    data = {
        "session_uuid": session_uuid
    }
    data['product_id'] = '1666'
    data['request_reference'] = code
    data['msisdn'] = phone_number
    data['amount'] = amount
    cash_out = requests.post(base_url + 'zamtelMoneyCashOut', data=json.dumps(data), headers=headers)
    data['confirmation_number'] = cash_out.json().get('confirmation_number', False)
    data['request_reference'] = code2
    del data['msisdn']
    del data['amount']
    cash_out_confirm = requests.post(base_url + 'zamtelMoneyCashOutConfirm', data=json.dumps(data), headers=headers)
    return cash_out_confirm.json()


def buyElectricity(meter_number, amount):
    alphabet = string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(6))
    code2 = ''.join(secrets.choice(alphabet) for i in range(6))
    code3 = ''.join(secrets.choice(alphabet) for i in range(6))
    data = {
        "session_uuid": session_uuid
    }
    data['request_reference'] = code
    data['meter_number'] = meter_number
    data['amount'] = amount
    data['product_id'] = find_product_from_method_name('buyElectricity')['product_id']
    r =requests.post(base_url + 'buyElectricity', data=json.dumps(data), headers=headers)
    data['confirmation_number'] = r.json().get('confirmation_number', False)
    del data['meter_number']
    del data['amount']
    electricity = requests.post(base_url + 'confirm', data=json.dumps(data), headers=headers)
    return electricity.json()


def spenn_deposit(phone_number, amount):
    alphabet = string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(6))
    code2 = ''.join(secrets.choice(alphabet) for i in range(6))
    code3 = ''.join(secrets.choice(alphabet) for i in range(6))
    data = {
        "session_uuid": session_uuid
    }
    data['request_reference'] = code
    data['product_id'] = find_product_from_method_name('spennDeposit')['product_id']
    data['wallet_msisdn'] = phone_number
    data['amount'] = amount
    spenn_deposit = requests.post(base_url + 'spennDeposit', data=json.dumps(data), headers=headers)
    data['confirmation_number'] = spenn_deposit.json().get('confirmation_number', False)
    data['request_reference'] = code2
    del data['wallet_msisdn']
    del data['amount']
    confirm = requests.post(base_url + 'spennDepositConfirm', data=json.dumps(data), headers=headers)
    return confirm.json()


def spenn_cash_out(phone_number, amount):
    alphabet = string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(6))
    code2 = ''.join(secrets.choice(alphabet) for i in range(6))
    code3 = ''.join(secrets.choice(alphabet) for i in range(6))
    code4 = ''.join(secrets.choice(alphabet) for i in range(6))

    data = {
        "session_uuid": session_uuid
    }
    data['request_reference'] = code
    data['wallet_msisdn'] = phone_number
    data['amount'] = amount
    data['product_id'] = find_product_from_method_name('spennCashOut')['product_id']
    data['shortcode'] = code3
    cash_out = requests.post(base_url + 'spennCashOut', data=json.dumps(data), headers=headers)
    data['confirmation_number'] = cash_out.json().get('confirmation_number', False)
    data['request_reference'] = code2
    del data['wallet_msisdn']
    del data['amount']
    confirm = requests.post(base_url + 'spennCashOutConfirm', data=json.dumps(data), headers=headers)
    data['shortcode'] = confirm.json().get('shortcode', False)
    data['request_reference'] = code3
    approval = requests.post(base_url + 'spennCashOutApproval', data=json.dumps(data), headers=headers)
    data['confirmation_number'] = approval.json().get('confirmation_number', False)
    data['request_reference'] = code4
    approval_confirm = requests.post(base_url + 'spennCashOutApprovalConfirm', data=json.dumps(data), headers=headers)
    return cash_out.json()
