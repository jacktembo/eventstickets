# from django.test import TestCase
#
# def split(a, n):
#     k, m = divmod(len(a), n)
#
#     return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))
#
# gen =split([i for i in range(1, 80)], 3)
# for item in gen:
#     print(len(item))
#
my_list = ['geeks', 'for', 'geeks', 'like',
           'geeky', 'nerdy', 'geek', 'love',
           'questions', 'words', 'life']


# Yield successive n-sized
# chunks from l.
def divide_chunks(l, n):
    if len(l) % 2 != 0 or len(l) % 2 == 0:

        # looping till length l
        for i in range(0, len(l), n):
            yield l[i:i + n]


# How many elements each
# list should have
number_of_seats = 22
n = ((number_of_seats - 1) // 2) - 1
x = list(divide_chunks([i for i in range(1, number_of_seats + 1)], n))
for item in x:
    print(len(item))
