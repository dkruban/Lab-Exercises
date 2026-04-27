% =====================================================
% PIZZAHUT BILLING SYSTEM
% =====================================================

:- dynamic(total/1).
:- dynamic(order/3).   % order(Item, Quantity, Amount)

total(0).

% ---------------- MENU PRICES ----------------
price(margherita, 150).
price(pepperoni, 250).
price(farmhouse, 220).
price(veggie_supreme, 200).
price(chicken_dominator, 300).

% ---------------- MENU ----------------
menu :-
    nl, write('********* PIZZAHUT MENU *********'), nl,
    write('1. Margherita - Rs 150'), nl,
    write('2. Pepperoni - Rs 250'), nl,
    write('3. Farmhouse - Rs 220'), nl,
    write('4. Veggie Supreme - Rs 200'), nl,
    write('5. Chicken Dominator - Rs 300'), nl,
    write('6. Show Total Bill & Exit'), nl,
    write('Enter your choice (1-6): ').

% ---------------- START ----------------
start :-
    retractall(total(_)),
    assert(total(0)),
    retractall(order(_,_,_)),
    billing.

% ---------------- BILLING LOOP ----------------
billing :-
    menu,
    read(Choice),
    process_choice(Choice).

% ---------------- PROCESS CHOICE ----------------
process_choice(6) :-
    nl, write('==============================='), nl,
    write('        PIZZAHUT BILL           '), nl,
    write('==============================='), nl,
    nl,
    write('Item\tQty\tRate\tAmount'), nl,
    write('--------------------------------'), nl,
    show_items,
    write('--------------------------------'), nl,
    total(Total),
    format('Total Bill Amount: Rs ~w~n', [Total]),
    write('==============================='), nl,
    write('Thank you! Visit again!'), nl,
    nl.

process_choice(Choice) :-
    (Choice >= 1, Choice =< 5 ->
        get_item(Choice, Item),
        format('Enter quantity for ~w: ', [Item]),
        read(Qty),
        price(Item, Price),
        Amount is Price * Qty,
        retract(total(T)),
        NewTotal is T + Amount,
        assert(total(NewTotal)),
        assert(order(Item, Qty, Amount)),
        format('Added ~w x ~w for Rs ~w.~n', [Qty, Item, Amount]),
        billing
    ;
        write('Invalid choice! Please enter 1 to 6.'), nl,
        billing
    ).

% ---------------- ITEM MAPPING ----------------
get_item(1, margherita).
get_item(2, pepperoni).
get_item(3, farmhouse).
get_item(4, veggie_supreme).
get_item(5, chicken_dominator).

% ---------------- SHOW ITEMS ----------------
show_items :-
    order(Item, Qty, Amount),
    price(Item, Price),
    format('~w\t~w\t~w\t~w~n', [Item, Qty, Price, Amount]),
    fail.
show_items.
