% Menu-Driven Arithmetic Operations in Prolog

% Arithmetic Operations
add(X, Y, R) :- R is X + Y.
subtract(X, Y, R) :- R is X - Y.
multiply(X, Y, R) :- R is X * Y.
divide(X, Y, R) :-
    Y =\= 0,
    R is X / Y.
modulus(X, Y, R) :-
    Y =\= 0,
    R is X mod Y.
power(X, Y, R) :- R is X ** Y.

% Menu Display
show_menu :-
    nl, write('********** ARITHMETIC MENU **********'), nl,
    write('1. Addition'), nl,
    write('2. Subtraction'), nl,
    write('3. Multiplication'), nl,
    write('4. Division'), nl,
    write('5. Modulus'), nl,
    write('6. Power'), nl,
    write('7. Exit'), nl,
    write('Enter your choice (1-7): ').

% Start Program
start :-
    repeat,
    show_menu,
    read(Choice),
    ( Choice == 7 ->
        write('Exiting program...'), nl, !
    ; Choice >= 1, Choice =< 6 ->
        write('Enter first number: '), read(X),
        write('Enter second number: '), read(Y),
        perform_operation(Choice, X, Y),
        fail
    ; write('Invalid choice! Please enter a number from 1 to 7.'), nl,
      fail).

% Perform Operation Based on Choice
perform_operation(1, X, Y) :- add(X, Y, R), format('Result: ~w + ~w = ~w~n', [X, Y, R]).
perform_operation(2, X, Y) :- subtract(X, Y, R), format('Result: ~w - ~w = ~w~n', [X, Y, R]).
perform_operation(3, X, Y) :- multiply(X, Y, R), format('Result: ~w * ~w = ~w~n', [X, Y, R]).
perform_operation(4, X, Y) :-
    (Y =:= 0 -> write('Error: Division by zero not allowed!'), nl ;
     divide(X, Y, R), format('Result: ~w / ~w = ~w~n', [X, Y, R])).
perform_operation(5, X, Y) :-
    (Y =:= 0 -> write('Error: Modulus by zero not allowed!'), nl ;
     modulus(X, Y, R), format('Result: ~w mod ~w = ~w~n', [X, Y, R])).
perform_operation(6, X, Y) :- power(X, Y, R), format('Result: ~w ^ ~w = ~w~n', [X, Y, R]).
