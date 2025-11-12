poly START 0

    LDX #0 .stevec
    LDL #0 .zamik
    LDB #1 .potenca
    LDA k0 .koeficient
    LDS #0 .rezultat

    RMO A, S

loop TIX #5
    JEQ done

    .povecanje potence
    LDT x
    MULR T, B

    .povecanje zamika, load koeficent, zmanjsanje zamika
    LDT #3
    MULR T, X
    LDA k0, X
    DIVR T, X

    .racunanje
    MULR B, A
    ADDR A, S

    J loop

done STS result
halt J halt

x WORD 2
k0 WORD 5
k1 WORD 4
k2 WORD 3
k3 WORD 2
k4 WORD 1
result RESW 1
