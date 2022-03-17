import secrets
import string
alphabet = string.digits
import itertools
ticket_number = ''.join(secrets.choice(alphabet) for i in range(8))
ticket_number = 'FM'+ ticket_number
print(ticket_number)
