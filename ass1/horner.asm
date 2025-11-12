horner START 0

    LDA k4
    MUL x
    ADD k3
    MUL x
    ADD k2
    MUL x
    ADD k1
    MUL x
    ADD k0

    STA result

halt J halt

x WORD 2
k4 WORD 1
k3 WORD 2
k2 WORD 3
k1 WORD 4
k0 WORD 5
result RESW 1
