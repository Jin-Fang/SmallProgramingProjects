side = 3
# [A,B]
# [C,D,E]
# [F,G,H,I]
# [J,K,L]

hori_lst = [['A', 'B'], ['C', 'D', 'E'], ['F', 'G', 'H', 'I'], ['J', 'K', 'L']]
hori_result = ["@", "@", "@", "@"]

left_lst = [['A', 'C', 'F'], ['B', 'D', 'G', 'I'], ['E', 'H', 'K'], ['I', 'L']]
left_result = ["@", "@", "@", "@"]

right_lst = [['F', 'J'], ['C', 'G', 'K'], ['A', 'D', 'H', 'L'], ['B', 'E', 'I']]
right_result = ["@", "@", "@", "@"]

line = ''
lineindex = 0

for i in range(2 * side + 5):

    # empty the line string
    line = ''

    if i % 2 == 0:
        lineindex = int(i / 2)
        if lineindex <= side:
            # get the first 2 left result
            if lineindex == 0:
                # print('first line')
                for ia in range(2 * side):
                    line += '  '
                line += left_result[0]
                line += '   '
                line += left_result[1]

            # general case of combing the results and list together
            else:
                if lineindex == side:
                    line += ' '
                for ib in range(side - lineindex):
                    line += '   '
                line += hori_result[lineindex - 1]
                for ic in range(len(hori_lst[lineindex - 1])):
                    line += ' - '
                    line += hori_lst[lineindex - 1][ic]
                if lineindex != side:
                    line += '   '
                    line += hori_result[lineindex + 1]
        else:
            if lineindex == side + 1:
                # for id in range():
                line += '   '
                line += hori_result[side]
                for ie in range(side):
                    line += ' - '
                    line += hori_lst[side][ie]
                line += '   '
                line += right_result[side]
            else:
                # print the last row for all other right resutls
                # print('right resutls')
                for ig in range(side + 6):
                    line += ' '
                for ih in range(side):
                    line += right_result[ih]
                    line += '   '
        print(line)
    else:
        # print stuff for the '/'
        # print()
        ssss = []
        lineindex2 = int(i / 2)
        if lineindex2 == 0:
            for iA in range(2 * side - 1):
                line += '  '
            line += ' / '
            line += ' '
            line += " / "
        elif lineindex2 < side:
            for iA in range(3 * (1 + side - lineindex2)):
                line += ' '
                # print('lineindex2: '+str(lineindex2)+' '+str(3*(1+side-lineindex2)))
            for iB in range(lineindex2 + 1):
                line += '/ \\ '
            line += '/'
        elif lineindex2 == side:
            for iC in range(3 * (side - 1)):
                line += ' '
            for iD in range(side):
                line += '\\ / '
            line += '\\'
        elif lineindex2 == side + 1:
            for iE in range(5 + side):
                line += ' '
            for iG in range(side):
                line += '\\   '

        print(line)

