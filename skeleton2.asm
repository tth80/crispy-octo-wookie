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
    push ebp
    mov ebp,esp
    sub esp,n
    push            ; save registers
        ;
        ; body of the function
        ;
    pop         ; restore registers
    mov eax, 0  ; return value
    mov esp, ebp
    pop ebp
    ret
