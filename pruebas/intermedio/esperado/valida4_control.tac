    n = 5
    fact = 1
    i = 1
L1:
    t1 = i <= n
    ifFalse t1 goto L2
    t2 = fact * i
    fact = t2
    t3 = i + 1
    i = t3
    goto L1
L2:
    print fact
    cuenta = 3
L3:
    t4 = cuenta > 0
    ifFalse t4 goto L4
    print cuenta
    t5 = cuenta - 1
    cuenta = t5
    goto L3
L4:
    k = 1
L5:
    t6 = k <= 6
    ifFalse t6 goto L6
    t7 = k div 2
    mitad = t7
    t8 = mitad * 2
    t9 = k - t8
    resto = t9
    t10 = resto == 0
    ifFalse t10 goto L7
    print k
    goto L8
L7:
    t11 = k == 5
    ifFalse t11 goto L9
    print 100
L9:
L8:
    t12 = k + 1
    k = t12
    goto L5
L6:
