segment data
    ;
    ; initialized data
    ;
segment bss
    ;
    ; uninitialized data
    ;
segment text
    global _func

_func:
    enter n,0
    push        ; save registers
        ;
        ; body of the function
        ;
    pop         ; restore registers
    mov eax, 0  ; return value
    leave
    ret
