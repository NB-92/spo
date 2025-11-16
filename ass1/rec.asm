.FIBONACCI
rec START 0
    .inicializacija stacka
    JSUB sinit
    .JSUB minit

    LDA #42

    JSUB fib
    STA result

halt J halt

.FIBONACCI
fib STL @stkp
    JSUB spush
    STB @stkp
    JSUB spush

    COMP #2
    JLT fibEx
    RMO A, B

    .F(A-1)
    SUB #1
    .preverimo, ce je v memo, in ce je preskocimo
    MUL #3
    RMO A, X
    LDA memo, X
    COMP #0
    JGT skip1

    RMO B, A
    SUB #1
    JSUB fib

    .F(A-2)
skip1 RMO B, A
    SUB #2
    MUL #3
    RMO A, X
    LDA memo, X
    COMP #0
    JGT skip2

    RMO B, A
    SUB #2
    JSUB fib

skip2 RMO B, A
    SUB #1
    MUL #3
    RMO A, X
    LDS memo, X
    SUB #3
    RMO A, X
    LDT memo, X
    ADDR S, T .F(A) = T

    RMO B, A
    MUL #3
    RMO A, X
    STT memo, X


fibEx JSUB spop
    LDB @stkp
    JSUB spop
    LDL @stkp

    LDA memo, X
    COMP #0
    JGT skip3

    LDA #1
    STA memo, X
skip3 RSUB

.RUTINE ZA SKLAD
.inicializacija
sinit STA temp
    LDA #stk
    STA stkp
    LDA temp
    RSUB

.poveca stkp za 3
spush STA temp
    LDA stkp
    ADD #3
    STA stkp
    LDA temp
    RSUB

.zmanjsa stkp za 3
spop STA temp
    LDA stkp
    SUB #3
    STA stkp
    LDA temp
    RSUB

.RUTINE ZA MEMOIZACIJO
.minit STA temp
    .LDA #memo
    .STA memop
    .LDA temp
    .RSUB

.PODATKI ZA SKLAD
stkp WORD 0 .stack pointer
temp RESW 1 .temp za odlaganje vrednosti registrov
stk RESW 1000

.OSTALI PODATKI
x1 RESW 1
result RESW 1
memop RESW 1
memo RESW 50

    END rec