print START 0

loop LDCH txt, X
    WD #0x01
    TIX #len
    JLT loop

halt J halt

txt BYTE C'HELLO WORLD'
    BYTE 10
    .BYTE 0

end EQU *
len EQU end-txt