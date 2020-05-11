import copy
import string
from collections import deque


class InputToken:
    cont = True
    pm = {'+', '-'}
    md = {'*', '/'}
    brkt = {'(', ')'}
    allowed_op = {'+', '-', '*', '/', '^'}
    allowed_in_eq = {'+', '-', '*', '/', '^', '(', ')'}
    dict = dict()

    def __init__(self):
        self.help = 'Helpful comments here!'
        self.unk_cmd = 'Unknown command'
        self.back_to_input = False
        self.res = 0
        self.left = ''
        self.right = ''
        self.print = 'False'
        self.exit = False
        self.error = ''

    def to_preset(self):
        self.res = 0
        self.left = ''
        self.right = ''
        self.print = False
        self.back_to_input = False
        self.error = ''

def remove_space(tmp_str):
    op_str = ''
    for ii in range(len(tmp_str)):
        if tmp_str[ii] == ' ':
            op_str += ''
        else:
            op_str += tmp_str[ii]
    return op_str


def has_eq_sign(inp, tmp_inp):
    if '=' in tmp_inp:
        # print('= here')
        for ii in range(len(tmp_inp)):
            # print(tmp_inp[ii])
            if tmp_inp[ii] == '=':
                inp.left = tmp_inp[:ii]
                inp.right = tmp_inp[ii + 1:]
                break
        for one_char in inp.right:
            # print(inp.right)
            if one_char != ' ':
                return True
        inp.right = ''  # all right side has are spaces
        return True
    else:
        inp.left = tmp_inp
        return False


def empty_input(tmp_inp):
    for one_char in tmp_inp:
        if one_char != ' ':
            return False
    return True


def var_valid(tmp_var):
    if tmp_var == '':
        return False
    for one_char in tmp_var:
        if one_char not in string.ascii_letters:
            return False
    return True


def assign_valid(one_inp, side_str):
    tmp_str = getattr(one_inp, side_str)
    global current_q
    while current_q:
        current_q.popleft()
    iden = ''
    bracket_stack = deque()
    for ii in range(len(tmp_str)):
        # First pick out the characters there are not illegible
        if ii == len(tmp_str) - 1:  # reaching the end of the string
            if tmp_str[ii] in InputToken.allowed_in_eq:
                if tmp_str[ii] == ')':  # ends with a right-bracket
                    try:
                        ignored = bracket_stack.pop()
                        current_q.append(iden)
                        current_q.append(')')
                    except IndexError:
                        one_inp.back_to_input = True
                        print('Invalid expression')
                        return False
                else:  # ends with an operator other than right-bracket
                    print('Invalid expression')
                    return False
            else:  # ends with a number or a letter
                iden += tmp_str[ii]
                current_q.append(iden)
            if not bracket_stack:  # matching brackets
                return True
            else:  # non-matching bracket
                print('Invalid expression')
                one_inp.back_to_input = True
                return False
        else:  # Not the end of string
            if not (tmp_str[ii] in InputToken.allowed_in_eq
                    or tmp_str[ii] in string.ascii_letters
                    or tmp_str[ii] in string.digits):
                print('Invalid expression')
                one_inp.back_to_input = True
                return False  # Back if any character is illegible
            #  Continue if this character is legit (variables or operator)
            if tmp_str[ii] in InputToken.allowed_in_eq:  # iden ends with previous char
                if tmp_str[ii] == '(':
                    bracket_stack.append('bracket_left')
                    if iden:
                        current_q.append(iden)
                    current_q.append(tmp_str[ii])
                    iden = ''  # reset identity if nothing wrong here
                elif tmp_str[ii] == ')':
                    try:
                        bracket_stack.pop()
                        if iden:
                            current_q.append(iden)
                        current_q.append(tmp_str[ii])
                        iden = ''  # reset identity if nothing wrong here
                    except IndexError:
                        print('Invalid syntax -- )')
                        one_inp.back_to_input = True
                        return False
                elif iden != '':  # no bracket involved here
                    try:  # first see if this is an integer
                        int(iden)
                    except ValueError:  # otherwise check to see if it exists
                        if not var_valid(iden):
                            print('Unknown variable')
                            one_inp.back_to_input = True
                            return False
                    current_q.append(iden)
                    current_q.append(tmp_str[ii])
                    iden = ''  # reset identity if nothing wrong here
                else:  # iden == '' operator follows operator
                    current_q.append(tmp_str[ii])
            else:  # not an operator
                iden = iden + tmp_str[ii]  # Not a complete identity yet.
    return False if bracket_stack else True


def assign_avail(tmp_str):
    #  The validity of the variables, and the bracket-matching should have
    # been checked. The inputs have been stored in the queue: current_q
    global current_q
    copied_q = deque()
    while current_q:
        copied_q.append(current_q.popleft())  # transfer the queue to a copy
    previous_popped = ''
    # print(f'copied_q size = {copied_q.qsize()}')
    while copied_q:
        popped = copied_q.popleft()
        if popped not in InputToken.brkt:  # ignoring brackets
            if popped in InputToken.md:
                if previous_popped == '' or previous_popped in InputToken.allowed_op:
                    print('Invalid expression -- assign_avail()')
                    return False
            elif popped in InputToken.pm:
                if previous_popped in InputToken.pm:
                    combo = previous_popped + popped
                    if combo == '--' or combo == '++':
                        current_q.pop()
                        popped = '+'
                    elif combo == '-+' or combo == '+-':
                        current_q.pop()
                        popped = '-'
                    else:  # previous_pop == '' case
                        pass
            else:  # integer or variable
                try:  # integer?
                    popped = int(popped)
                except ValueError:
                    if not var_valid(popped):
                        if tmp_str == 'left':
                            print('Invalid identifier')
                        else:
                            print('Invalid assignment')
                        return False
                    elif popped not in InputToken.dict.keys():
                        if tmp_str =='right':
                            print('Unknown variable')
                            return False
        current_q.append(popped)
        previous_popped = copy.copy(popped)
    return True


def precedence_one(str_1, str_2):
    if str_1 == '^':
        return True
    elif str_1 in InputToken.md and str_2 in InputToken.pm:
        return True
    else:
        return False


def assign_eval(one_inp):
    # Take the queue and start to fill the computation stack. Everything should already
    # be checked by assign_avail function.
    # print('Evauluating')
    global current_q
    value_in_one_inp = float(0)
    eval_stack = deque()
    oper_stack = deque()
    result_stack = deque()
    while current_q:
        from_FIFO = current_q.popleft()
        # print(from_FIFO)
        if from_FIFO not in InputToken.allowed_in_eq:  # number or variable
            eval_stack.append(from_FIFO)
        elif from_FIFO == ')':
            popped = oper_stack.pop()
            while popped != '(':
                eval_stack.append(popped)
                popped = oper_stack.pop()
        elif from_FIFO == '(':
            oper_stack.append('(')
        elif oper_stack:  # Non-empty oper_stack
            if oper_stack[-1] == '(':
                oper_stack.append(from_FIFO)
            else:  # precedence tests
                if precedence_one(from_FIFO, oper_stack[-1]):
                    oper_stack.append(from_FIFO)
                else:
                    eval_stack.append(oper_stack.pop())
                    while (oper_stack and precedence_one(from_FIFO,
                             oper_stack[-1]) and oper_stack[-1] != '('):
                        eval_stack.append(oper_stack.pop())
                    oper_stack.append(from_FIFO)
        else:  # Empty oper_stack
            oper_stack.append(from_FIFO)
    while oper_stack:
        eval_stack.append(oper_stack.pop())
    # for ii in range(len(eval_stack)):
    #     print(f'{eval_stack[ii]}', end=' ')
    # print('eval_stack listed above!')
    result_stack.append(0)  # guarding against leading +-
    while eval_stack:
        popped = eval_stack.popleft()
        if popped in InputToken.allowed_op:
            operand_1 = result_stack.pop()
            operand_2 = result_stack.pop()
            # print(popped)
            # print(operand_2, operand_1)
            if popped == '+':
                value_in_one_inp = operand_2 + operand_1
            elif popped == '-':
                value_in_one_inp = operand_2 - operand_1
            elif popped == '*':
                value_in_one_inp = operand_2 * operand_1
            elif popped == '/':
                value_in_one_inp = operand_2 / operand_1
            else:  # '^' case
                value_in_one_inp = operand_2 ^ operand_1
            result_stack.append(value_in_one_inp)
        else:
            try:
                int(popped)
                result_stack.append(popped)
            except ValueError:
                result_stack.append(InputToken.dict[popped])
        # for ii in range(len(result_stack)):
        #     print(f'{result_stack[ii]}', end=' ')
        # print()
    value_in_one_inp = result_stack.pop()
    return value_in_one_inp


##  InputToken.dict starts empty. New key:value pairs would be added into it.
#  It will not be cleared until the end of the program.
#
#  current_q stores the validated variables and operators.
# With the order they are entered. This should be cleared after
# the contents are converted into a RPN stack.
#
#  inp is an instance. May contain one or two sides (separated by '=')

current_q = deque()
inp = InputToken()
while not inp.exit:
    tmp_inp = input()
    while current_q:
        current_q.popleft()  # clear the queue for each input
    tmp_inp = remove_space(tmp_inp)
    if tmp_inp == '':
        pass  # ignore if input were nothing more than spaces
    else:  # non-empty input
        if has_eq_sign(inp, tmp_inp):
            if assign_valid(inp, 'left'):
                if assign_valid(inp, 'right'):
                    if assign_avail('right'):
                        InputToken.dict.update \
                            ({inp.left: assign_eval(inp.right)})
                    else:  # right side NOT valid
                        inp.back_to_input = True
                else:
                    print('Invalid assignment')
                    inp.back_to_input = True
            else:  # left side invalid
                print('Invalid identifier')
                inp.back_to_input = True
        else:  # no '=' sign. One-sided entry
            if inp.left[0] == '/':
                if inp.left == '/exit':
                    print('Bye!')
                    inp.exit = True
                elif inp.left == '/help':
                    print(inp.help)
                else:
                    print('Unknown command')
                    inp.back_to_input = True
            elif assign_valid(inp, 'left'):  # begins with something other than '/'
                if assign_avail('right'):
                    final = assign_eval(inp)
                    if int(final) == final:
                        print(int(final))
                    else:
                        print(final)
    if inp.exit:
        exit(0)
    inp.to_preset()
