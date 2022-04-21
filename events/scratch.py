ticket_price = 2
percentage_commission = 8
deposit = ticket_price - (ticket_price * (8 / 100))
from decimal import Decimal
print(float(deposit) + 23)