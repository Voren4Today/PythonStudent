import math
import sys


class LoanClass:
    def __init__(self):
        self.prin = 0
        self.amt = 0
        self.n_mon = 0
        self.interest = 0
        self.type = ''
        self.total_paid = 0

    def year_month_needed(self, num_month):
        yr = num_month // 12
        mo = num_month % 12
        month_phrase = ''  # zero month
        if mo == 1:
            month_phrase = '1 month'
        if mo > 1:  # more than one month
            month_phrase = str(mo) + ' months'
        year_phrase = ''
        if yr == 1:
            year_phrase = '1 year'
        if yr > 1:
            year_phrase = str(yr) + ' years'

        if (yr != 0) and (mo != 0):  # add 'and' only when both exist
            and_phrase = ' and '
        else:
            and_phrase = ''

        return year_phrase + and_phrase + month_phrase


def verify_args(loan, arg_inp):
    loan_para = {'--principal', '--periods', '--payment', '--interest'}

    if len(arg_inp) != 5:
        print('Incorrect parameters')
        return 'Incorrect'

    if arg_inp[1] == '--type=diff':
        loan.type = 'diff'
    elif arg_inp[1] == '--type=annuity':
        loan.type = 'annuity'
    else:
        print('Incorrect parameters')
        return 'Incorrect'
    for cntr in range(2, 5):
        inp_front = arg_inp[cntr].split('=')[0]
        inp_back = arg_inp[cntr].split('=')[1]
        if inp_front in loan_para:
            if inp_front == '--principal':
                loan.prin = int(inp_back)
                loan_para.discard(inp_front)
            elif inp_front == '--periods':
                loan.n_mon = int(inp_back)
                loan_para.discard(inp_front)
            elif inp_front == '--interest':
                loan.interest = float(inp_back)
                loan_para.discard(inp_front)
            elif inp_front == '--payment':
                loan_para.discard(inp_front)
                loan.amt = int(inp_back)

    if (len(loan_para) != 1):
        print('Incorrect parameters')  # the args not match
        return 'Incorrect'

    for para in loan_para:
        pass
    return para  # remaining parameter (to be solved)


loan_x = LoanClass()

to_be_solved = verify_args(loan_x, sys.argv)
# print(to_be_solved)
if to_be_solved == 'Incorrect':
    exit(1)

if loan_x.type == 'annuity':
    if to_be_solved == '--periods':
        i_numerical = loan_x.interest / (12 * 100)
        n = math.log(float(loan_x.amt / (loan_x.amt
                  - i_numerical * loan_x.prin)), 1 + i_numerical)
        loan_x.n_mon = math.ceil(n)
        loan_x.total_paid = loan_x.amt * loan_x.n_mon
        print(f'You need {loan_x.year_month_needed(loan_x.n_mon)} '
              f'to repay this credit!')

    if to_be_solved == '--payment':
        i_numerical = loan_x.interest / (12 * 100)
        loan_x.amt = math.ceil(loan_x.prin * i_numerical \
                               * (1 + i_numerical) ** loan_x.n_mon \
                               / ((1 + i_numerical) ** loan_x.n_mon - 1))
        loan_x.total_paid = loan_x.amt * loan_x.n_mon
        print(f'Your annuity payment = {loan_x.amt}')

    if to_be_solved == '--principal':
        i_numerical = loan_x.interest / (12 * 100)
        loan_x.prin = int(loan_x.amt / (i_numerical \
                           * (1 + i_numerical) ** loan_x.n_mon \
                           / ((1 + i_numerical) ** loan_x.n_mon - 1)))
        loan_x.total_paid = loan_x.amt * loan_x.n_mon
        print(f'Your credit principal = {loan_x.prin}!')

    print(f'Overpayment = {loan_x.total_paid - loan_x.prin}')

if loan_x.type == 'diff':
    if to_be_solved == '--payment':
        i_numerical = loan_x.interest / (12 * 100)
        for cntr in range(0, loan_x.n_mon):
            loan_x.amt = math.ceil(loan_x.prin / loan_x.n_mon + i_numerical \
                    * (loan_x.prin -(loan_x.prin * cntr) / loan_x.n_mon))
            print(f'Month {cntr + 1 }: paid out {loan_x.amt}')
            loan_x.total_paid += loan_x.amt

        print()
        print(f'Overpayment = {loan_x.total_paid - loan_x.prin}')
    else:  # can only solve payment. Others give error message
        print('Incorrect parameters')  # the args not match

exit(0)
