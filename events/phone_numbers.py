airtel_prefixes = ['+26097', '097', '077', '+26077']
mtn_prefixes = ['+26096', '+26076', '096', '076']
zamtel_prefixes = ['+26095', '095']
all_prefixes = airtel_prefixes + mtn_prefixes + zamtel_prefixes

def get_network(phone_number: str):
    if phone_number.startswith('+26097') or phone_number.startswith('097') or phone_number.startswith('077') or phone_number.startswith('+26077'):
        return 'airtel'
    elif phone_number.startswith('+26096') or phone_number.startswith('+26076') or phone_number.startswith('096') or phone_number.startswith('076'):
        return 'mtn'
    elif phone_number.startswith('+26095') or phone_number.startswith('095'):
        return 'zamtel'
    else:
        return 'unknown network'

