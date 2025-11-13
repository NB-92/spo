vsota START 0

    JSUB sinit
    LDA #10
    JSUB rsum
    STA result

halt J halt

.REKURZIVNA VSOTA 1..N
rsum STL @stkp .daj L in B na sklad
    JSUB spush
    STB @stkp
    JSUB spush

    COMP #2
    JLT rsumEx .če je A < 2 return
    RMO A, B
    SUB #1
    JSUB rsum . A = A - 1
    ADDR B, A

rsumEx JSUB spop
    LDB @stkp
    JSUB spop
    LDL @stkp
    RSUB

.RUTINE ZA SKLAD
.inicializacija
sinit STA temp
    LDA #stk
    STA stkp
    LDA temp
    RSUB

.A > sklad, poveca stkp za 3
spush STA temp
    LDA stkp
    ADD #3
    STA stkp
    LDA temp
    RSUB

.A < sklad, zmanjsa stkp za 3
spop STA temp
    LDA stkp
    SUB #3
    STA stkp
    LDA temp
    RSUB

result RESW 1

.podatki za sklad
stkp WORD 0 .stack pointer
temp RESW 1 .temp za odlaganje vrednosti registrov
stk RESW 1000

    END vsota