arith START 0

.seštevanje
    LDA x
    ADD y
    STA sum

.odštevanje
    LDA x
    SUB y
    STA diff

.množenje
    LDA x
    MUL y
    STA prod

.deljenje
    LDA x
    DIV y
    STA quot

.modul
    LDA y
    MUL quot
    STA temp
    LDA x
    SUB temp
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