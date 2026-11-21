    cantidad = 10
    anterior = 0
    actual = 1
    contador = 1
L1:
    t1 = contador <= cantidad
    ifFalse t1 goto L2
    print anterior
    t2 = anterior + actual
    siguiente = t2
    anterior = actual
    actual = siguiente
    t3 = contador + 1
    contador = t3
    goto L1
L2:
