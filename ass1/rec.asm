.FIBONACCI
rec START 0
    .inicializacija stackov
    JSUB sinit
    JSUB ninit

    .beremo dokler ne dobimo 0
loop LDA #0
    JSUB beri .v A
    
brdone RMO B, A
    COMP #0 .preskočimo dvojne \n
    JEQ loop 
    JSUB fib .fib(A)
    STA result .fib(A) -> result

    JSUB resset .result damo stevko po stevko na sklad
done LDA #0xA
    WD #1 .\n
    J loop

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
    .shranimo memo[A-1] v S in memo[A-2] v T in sestejemo
    SUB #1
    MUL #3
    RMO A, X
    LDS memo, X
    SUB #3
    RMO A, X
    LDT memo, X
    ADDR S, T .F(A) = T

    .T shranimo v memo[A]
    RMO B, A
    MUL #3
    RMO A, X
    STT memo, X


fibEx JSUB spop
    LDB @stkp
    JSUB spop
    LDL @stkp

    .ce je memo[A] > 0, smo ga ze zapisali in ga nocemo overwritad z 1
    .sicer je A == 0 ali A == 1 in je fib(A) == 1
    LDA memo, X
    COMP #0
    JGT skip3

    LDA #1
    STA memo, X
skip3 RSUB

.RUTINA ZA BRANJE
beri TD #0xAA
    RD #0xAA
    COMP #0xA .koncamo ce je \n
    JEQ brdone
    COMP #0xD .koncamo ce je carriage return
    JEQ brdone
    COMP #0 . koncam, ce je 1. znak 0
    JEQ halt

    SUB #48 .odstejemo, da dobimo iz znaka stevilko
    RMO A, B

brloop TD #0xAA
    RD #0xAA
    COMP #0xA .koncamo ce je \n
    JEQ brdone
    COMP #0xD .koncamo, ce je carriage return
    JEQ brdone
    SUB #48 
    RMO A, S
    RMO B, A
    MUL #10
    ADDR S, A
    RMO A, B
    J brloop


.RUTINA ZA PISANJE
.prebere stevilo iz result in jo da po stevkah na sklad
resset LDA result
    COMP #0
    JEQ pisi
    DIV #10
    MUL #10
    RMO A, B
    LDA result
    SUBR B, A
    STA @nump
    JSUB npush
    LDA result
    DIV #10
    STA result
    J resset

.iz sklada nums po vrsti izpisujemo cifre na stand. izhod
pisi JSUB npop
    LDA @nump
    ADD #48
    WD #1
    LDA nump
    COMP #nums
    JEQ done
    J pisi

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

.RUTINE ZA SKLAD STEVK
.inicializacija
ninit STA temp
    LDA #nums
    STA nump
    LDA temp
    RSUB

.poveca nump za 3
npush STA temp
    LDA nump
    ADD #3
    STA nump
    LDA temp
    RSUB

.zmanjsa nump za 3
npop STA temp
    LDA nump
    SUB #3
    STA nump
    LDA temp
    RSUB

.PODATKI ZA SKLAD
stkp WORD 0 .stack pointer
temp RESW 1 .temp za odlaganje vrednosti registrov
stk RESW 500

.PODATKI ZA SKLAD STEVK
nump WORD 0
nums RESW 20

.OSTALI PODATKI
x1 RESW 1
result RESW 1
memop RESW 1
memo RESW 50

    END rec