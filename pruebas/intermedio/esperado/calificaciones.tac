    nota1 = 85.5
    nota2 = 70
    nota3 = 92.0
    t1 = nota1 + nota2
    t2 = t1 + nota3
    t3 = t2 / 3.0
    promedio = t3
    mayor = nota1
    t4 = nota2 > mayor
    ifFalse t4 goto L1
    mayor = nota2
L1:
    t5 = nota3 > mayor
    ifFalse t5 goto L2
    mayor = nota3
L2:
    aprobado = 0
    t6 = promedio >= 70
    ifFalse t6 goto L3
    aprobado = 1
L3:
    print nota1
    print nota2
    print nota3
    print promedio
    print mayor
    print aprobado
