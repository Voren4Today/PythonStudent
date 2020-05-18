import random


def fetch_stronger(inp, n_total):
    idx_to_return = []
    for ii in range(inp + 1, inp + n_total // 2 + 1):
        idx_to_return = idx_to_return + [ii % n_total]
    return idx_to_return


inp = input('Enter your name: ')  # starting of the game
file_rating = open('rating.txt', 'r')
if inp != '!exit':
    print(f'Hello {inp}')
    rating_p = int(0)  # preset rating to zero in case it's not on file
    line_in_file = file_rating.readline()
    while line_in_file:
        name_r, rating_r = line_in_file.split()
        if name_r == inp:  # record found
            rating_p = int(rating_r)
            break
        else:  # read again
            line_in_file = file_rating.readline()
    options = input().split(',')
    if options == ['']:  # using default
        options = ['rock', 'paper', 'scissors']
    num_opt = len(options)
    print("Okay, let's start")
while inp != '!exit':
    inp = input()
    if inp == '!rating':
        print(f'Your rating: {rating_p}')
    elif inp in options:
        inp_index = options.index(inp)
        strong_indexes = fetch_stronger(inp_index, num_opt)
        comp_index = random.randint(0, num_opt-1)
        if comp_index == inp_index:
            rating_p += 50
            print(f'There is a draw ({options[comp_index]})')
        elif comp_index in strong_indexes:
            print(f'Sorry, but computer chose {options[comp_index]}')
        else:
            rating_p += 100
            print(f'Well done. Computer chose {options[comp_index]} and failed')
    elif inp == '!exit':
        break
    else:
        print('Invalid input')
print('Bye!')
