    a = 48
    b = 18
L1:
    t1 = a != b
    ifFalse t1 goto L2
    t2 = a > b
    ifFalse t2 goto L3
    t3 = a - b
    a = t3
    goto L4
L3:
    t4 = b - a
    b = t4
L4:
    goto L1
L2:
    print a
    numero = 4821
    suma = 0
L5:
    t5 = numero > 0
    ifFalse t5 goto L6
    t6 = numero div 10
    t7 = t6 * 10
    t8 = numero - t7
    digito = t8
    t9 = suma + digito
    suma = t9
    t10 = numero div 10
    numero = t10
    goto L5
L6:
    print suma
    n = 6
    pasos = 0
L7:
    t11 = n != 1
    ifFalse t11 goto L8
    t12 = n div 2
    mitad = t12
    t13 = mitad * 2
    t14 = n - t13
    t15 = t14 == 0
    ifFalse t15 goto L9
    n = mitad
    goto L10
L9:
    t16 = 3 * n
    t17 = t16 + 1
    n = t17
L10:
    t18 = pasos + 1
    pasos = t18
    goto L7
L8:
    print pasos
