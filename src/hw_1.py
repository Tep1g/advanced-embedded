def p1():
    r1 = 300 + 200
    r2 = 1 / ((1 / r1) + (1 / 450))
    r3 = 75 + r2
    r4 = 1 / ((1 / 250) + (1 / r3))
    Rab = 50 + r4
    print("Resistance Rab: {:.2f} Ω".format(Rab))

def _p2_p3_res():
    r1 = 400 + 125
    r2 = 1 / ((1 / 300) + (1 / r1))
    r3 = 75 + r2

    return (r1, r2, r3)

def p2():
    (r1, r2, r3) = _p2_p3_res()

    i_total = 10
    i1 = i_total * (r3 / (r3 + 200))            #5.7
    i2 = (i_total - i1) * (r1 / (r1 + 300))     #2.7
    i3 = i_total - i1 - i2                      #1.5

    print("I1: {}A".format(i1))
    print("I2: {}A".format(i2))
    print("I3: {}A".format(i3))
