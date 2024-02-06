def sa(e):
    def bare_expr(s):
        nums = []
        not_nums = []
        not_nums_plus = []
        for k in s:
            if k.isnumeric():
                nums.append(k)
            else:
                if k in ['*', '/', '%']:
                    not_nums_plus.append(k)
                elif k in ['+', '-']:
                    not_nums.append(k)
        return list(nums+not_nums_plus+not_nums)   
    res=[]
    fin_res=[]
    parenthesis = e.count('(')
    if parenthesis>=1:
        for z in range(0, parenthesis):
            for n, k in enumerate(e):
                if k=='(':
                    last_opar = n
                elif k==')':
                    last_cpar = n
                    break
            res = bare_expr(e[last_opar:(last_cpar+1)])
            print(res)
            fin_res.append(res)
            print('-----------------------------------------------')
            e=e[:last_opar]+[]+e[(last_cpar+1):]
            print(e)
            print(fin_res)
    to_return = []
    for _n in fin_res:
        to_return=to_return+_n
    print(to_return+e)
sa(["(",
                           "(",
                           "(",
                           "1",
                           "+",
                           "2",
                           ")",
                           "*",
                           "3",
                           ")",
                           "+",
                           "6",
                           ")",
                           "/",
                           "(",
                           "2",
                           "+",
                           "3",
                           ")"])