    i = 1
    pares = 0
    impares = 0
L1:
    t1 = i <= 6
    ifFalse t1 goto L2
    t2 = i div 2
    t3 = t2 * 2
    t4 = i - t3
    t5 = t4 == 0
    ifFalse t5 goto L3
    t6 = pares + 1
    pares = t6
    goto L4
L3:
    t7 = impares + 1
    impares = t7
L4:
    t8 = i + 1
    i = t8
    goto L1
L2:
    print pares
    print impares
    nota = 85
    t9 = nota >= 90
    ifFalse t9 goto L5
    print 1
    goto L6
L5:
    t10 = nota >= 70
    ifFalse t10 goto L7
    print 2
    goto L8
L7:
    print 3
L8:
L6:
