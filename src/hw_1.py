def p1():
    r1 = 300 + 200
    r2 = 1 / ((1 / r1) + (1 / 450))
    r3 = 75 + r2
    r4 = 1 / ((1 / 250) + (1 / r3))
    Rab = 50 + r4
    print("Resistance Rab: {:.2f} Ω".format(Rab))