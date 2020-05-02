import string
import math
import copy


def mat_mul(A, B):
    # print (A, B)
    dot_sum = 0
    for ii in range((len(A))):
        dot_sum = dot_sum + (A[ii] * B[ii])
    # print(dot_sum)
    return dot_sum


def vec_row(mat, r):
    vec = mat[r]
    return vec


def vec_col(mat, c):
    vec = [elem[c] for elem in mat]
    return


def minor_ij(minor_mat):
    to_be_returned = 0
    if len(minor_mat) == 1:
        to_be_returned = float(minor_mat[0][0])
    elif len(minor_mat) == 2:
        to_be_returned = float(minor_mat[0][0] * minor_mat[1][1]) \
                         - float(minor_mat[0][1] * minor_mat[1][0])
    else:  # more than 2x2
        for col in range(len(minor_mat[0])):
            reduced_mat = []
            for row in range(1, len(minor_mat)):
                single_reduced = minor_mat[row].copy()
                del single_reduced[col]  # delete the col-th item
                reduced_mat.append(single_reduced)

            to_be_returned = to_be_returned + (-1) ** col * minor_mat[0][col] \
                             * minor_ij(reduced_mat)

    return to_be_returned


def trp_mat(mat_inp):
    row = len(mat_inp)
    mat_out = []
    for nn in range(row):
        elem =[]
        for kk in range(col):
            single_elem = mat_inp[kk][nn]
            if math.floor(single_elem) == single_elem:
                single_elem = int(single_elem)
            else:
                single_elem = round(single_elem, 4)
            elem.append(single_elem)

        mat_out.append(elem)

    return mat_out


run_prog = True
while run_prog:
    print("1. Add matrices")
    print("2. Multiply matrix by a constant")
    print("3. Multiply matrices")
    print("4. Transpose matrix")
    print("5. Calculate determinant")
    print("6. Inverse matrix")
    print("0. Exit")
    print("Your choice: ")
    mata = []
    matb = []
    single_elem = 0
    action = input()
    if action == '1':  # add
        read = input('Enter size of first matrix: ')
        row = int(read.split()[0])
        col = int(read.split()[1])
        print('Enter first matrix:')
        for mm in range(row):
            read = input()
            v = [float(read.split()[_]) for _ in range(col)]
            mata.append(v)

        read = input('Enter size of second matrix: ')
        rowb = int(read.split()[0])
        colb = int(read.split()[1])
        print('Enter second matrix:')
        for mm in range(rowb):
            read = input()
            v = [float(read.split()[_]) for _ in range(colb)]
            matb.append(v)

        if (row != rowb) or (col != colb):
            print('The operation cannot be performed.')
        else:
            print('The result is:')
            for mm in range(row):
                for nn in range(col):
                    elem = float(mata[mm][nn] + matb[mm][nn])
                    if math.floor(elem) == elem:
                        elem = int(elem)
                    print(f'{elem} ', end=' ')
                print()

    if action == '2':  # multiply by a constant
        read = input('Enter size of matrix: ')
        row = int(read.split()[0])
        col = int(read.split()[1])
        print('Enter matrix:')
        for mm in range(row):
            read = input()
            v = [float(read.split()[_]) for _ in range(col)]
            mata.append(v)
        const_factor = float(input('Enter constant:'))
        print('The result is:')
        for nn in range(row):
            for kk in range(col):
                single_elem = const_factor * mata[nn][kk]
                if math.floor(single_elem) == single_elem:
                    single_elem = int(single_elem)
                else:
                    single_elem = round(single_elem, 4)

                print(f'{single_elem} ', end=' ')
            print()

    if action == '3':  # matrices multiplication
        read = input('Enter size of first matrix: ')
        row = int(read.split()[0])
        col = int(read.split()[1])
        print('Enter first matrix:')
        for mm in range(row):
            read = input()
            v = [float(read.split()[_]) for _ in range(col)]
            mata.append(v)

        read = input('Enter size of second matrix: ')
        rowb = int(read.split()[0])
        colb = int(read.split()[1])
        print('Enter second matrix:')
        for mm in range(rowb):
            read = input()
            v = [float(read.split()[_]) for _ in range(colb)]
            matb.append(v)
        # print(row, colb)
        if rowb != col:
            print('The operation cannot be performed.')
        else:
            print('The result is:')
            for mm in range(row):
                for nn in range(colb):
                    single_elem = \
                        float(mat_mul(mata[mm], [elem[nn] for elem in matb]))
                    if math.floor(single_elem) == single_elem:
                        single_elem = int(single_elem)
                    else:
                        single_elem = round(single_elem, 4)

                    print(f'{single_elem} ', end=' ')
                print()

    if action == '4':  # Transpose
        print()
        print("1. Main diagonal")
        print("2. Side diagonal")
        print("3. Vertical line")
        print("4. Horizontal line")
        print("Your choice: ")
        mirror_line = input()

        read = input('Enter size of matrix: ')
        row = int(read.split()[0])
        col = int(read.split()[1])
        print('Enter matrix:')
        for mm in range(row):
            read = input()
            v = [float(read.split()[_]) for _ in range(col)]
            mata.append(v)
        print('The result is:')
        for nn in range(row):
            for kk in range(col):
                if mirror_line == '1':  # Main
                    single_elem = mata[kk][nn]
                if mirror_line == '2':  # side
                    single_elem = mata[col - 1 - kk][row - 1 - nn]
                if mirror_line == '3':  # Vert
                    single_elem = mata[nn][col - 1 - kk]
                if mirror_line == '4':  # Hori
                    single_elem = mata[row - 1 - nn][kk]
                if math.floor(single_elem) == single_elem:
                    single_elem = int(single_elem)
                else:
                    single_elem = round(single_elem, 4)
                print(f'{single_elem} ', end=' ')
            print()

    if action == '5':  # determinant
        read = input('Enter size of matrix: ')
        row = int(read.split()[0])
        col = int(read.split()[1])
        print('Enter matrix:')
        for mm in range(row):
            read = input()
            v = [float(read.split()[_]) for _ in range(col)]
            mata.append(v)
        mat_det = minor_ij(mata)
        print('The result is:')
        if math.floor(mat_det) == mat_det:
            mat_det = int(mat_det)
        else:
            mat_det = round(mat_det, 4)
        print(mat_det)

    if action == '6':  # inversion
        read = input('Enter size of matrix: ')
        row = int(read.split()[0])
        col = int(read.split()[1])
        print('Enter matrix:')
        for mm in range(row):
            read = input()
            v = [float(read.split()[_]) for _ in range(col)]
            mata.append(v)
        mat_det = minor_ij(mata)
        if mat_det == 0:
            print("This matrix doesn't have an inverse.")
        else:  # Inversion exists
            mat_tmp = []
            if row == 1:  #  a single number
                mat_tmp = (1 / mat_det) * mata
            else:  # more than a single element
                matb = []
                for ii in range(row):
                    elem = []
                    for jj in range(col):
                        mat_tmp = copy.deepcopy(mata)
                        # print(f'{ii}, {jj} mat_tmp {mat_tmp}, {mata}')
                        for kk in range(col):
                            del mat_tmp[kk][jj]
                        # print(f'mat_tmp reduce jj: {mat_tmp}, {mata}')
                        del mat_tmp[ii]
                        # print(f'mat_tmp reduce ii: {mat_tmp}, {mata}')
                        single_elem = (-1)**(ii + jj) * minor_ij(mat_tmp)
                        # print(f'single_element: {single_elem}, {mata}')
                        elem.append(single_elem)
                    # print(elem)
                    matb.append(elem)

                matb = trp_mat(matb)
                for nn in range(row):
                    for kk in range(col):
                        single_elem = (1 / mat_det) * matb[nn][kk]
                        single_elem = round(single_elem, 3)
                        print(f'{single_elem} ', end=' ')
                    print()
                print()

    if action == '0':
        exit(0)

    print()
