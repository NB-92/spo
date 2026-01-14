arith START 0

.seštevanje
    LDA x
    LDB y
    ADDR A, B
    STA sum

.odštevanje
    LDA x
    LDB y
    SUBR A, B
    STA diff

.množenje
    LDA x
    LDB y
    MULR A, B
    STA prod

.deljenje
    LDA x
    LDB y
    DIVR A, B
    STA quot

.modul
    LDA y
    LDB quot
    MULR A, B
    STA temp
    LDA x
    LDB temp
    SUBR A, B
    STA mod

halt J halt

x WORD 5
y WORD 42

sum RESW 1
diff RESW 1
prod RESW 1
quot RESW 1
mod RESW 1
temp RESW 1