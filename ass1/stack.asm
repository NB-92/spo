stack START 0
    JSUB sinit
    JSUB beri
done JSUB pisi
pdone LDA #0xA
    WD #1
halt J halt

.RUTINE ZA SKLAD
.inicializacija
sinit STA temp
    LDA #stk
    STA stkp
    LDA temp
    RSUB

.A > sklad, poveca stkp za 3
spush STA temp
    STA @stkp
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
    LDA @stkp
    RSUB

.RUTINA ZA BRANJE/PISANJE
beri RD #0
    .WD #1
    JSUB spush
    LDX #0xA
    COMPR X, A
    JEQ done
    J beri

pisi LDX stkp
    LDB #stk
    COMPR X, B
    JEQ pdone
    JSUB spop
    WD #1
    J pisi

.podatki za sklad
stkp WORD 0 .stack pointer
temp RESW 1 .temp za odlaganje vrednosti registrov
stk RESW 1000

    END stack