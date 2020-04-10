// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.


// initialize
    @counter
    M=0
    @out
    M=0

(LOOP)
    @counter
    D=M
    @R1
    D=D-M
    @OUT
    D;JEQ
    @counter
    M=M+1
    @R0
    D=M
    @out
    M=M+D
    @LOOP
    0;JMP 

(OUT)
    @out
    D=M
    @R2
    M=D

(END) // infinite loop
    @END
    0,JMP
