// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

    @SCREEN
    D=A
    @POS
    M=D-1

(LOOP)
    @KBD
    D=M
    @FILL
    D;JGT
    @UNFILL
    0;JMP

(FILL)
    @POS
    D=M
    @KBD
    D=D-A
    @LOOP
    D;JEQ
    @POS
    A=M
    M=-1
    @POS
    M=M+1
    @LOOP
    0;JMP

(UNFILL)
    @POS
    D=M
    @SCREEN
    D=D-A
    D=D+1
    @LOOP
    D;JEQ
    @POS
    A=M
    M=0
    @POS
    M=M-1
    @LOOP
    0;JMP
    
