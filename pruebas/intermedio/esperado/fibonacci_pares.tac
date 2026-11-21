    pares = 10
    encontrados = 0
    anterior = 0
    actual = 1
L1:
    t1 = encontrados < pares
    ifFalse t1 goto L2
    t2 = anterior div 2
    t3 = t2 * 2
    t4 = anterior - t3
    t5 = t4 == 0
    ifFalse t5 goto L3
    print anterior
    t6 = encontrados + 1
    encontrados = t6
L3:
    t7 = anterior + actual
    siguiente = t7
    anterior = actual
    actual = siguiente
    goto L1
L2:
