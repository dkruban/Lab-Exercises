CODE:
:- dynamic item/3.     % item(Name, Price, StockQty)
:- dynamic order/2.    % order(Name, OrderedQty)

% -------- Add Item to Store --------
add_item(Name, Price, Qty) :-
    assertz(item(Name, Price, Qty)),
    write('Item added to store'), nl.

% -------- Delete Item from Store --------
delete_item(Name) :-
    retractall(item(Name, _, _)),
    write('Item deleted from store'), nl.

% -------- Increase Stock --------
increase_stock(Name, Inc) :-
    retract(item(Name, Price, Qty)),
    NewQty is Qty + Inc,
    assertz(item(Name, Price, NewQty)),
    write('Stock increased'), nl.

% -------- Decrease Stock --------
decrease_stock(Name, Dec) :-
    retract(item(Name, Price, Qty)),
    NewQty is Qty - Dec,
    ( NewQty >= 0 ->
        assertz(item(Name, Price, NewQty)),
        write('Stock decreased'), nl
    ;
        write('Not enough stock'), nl,
        assertz(item(Name, Price, Qty))
    ).

% -------- Place Order --------
place_order(Name, Qty) :-
    item(Name, Price, Stock),
    Qty =< Stock,   % check stock availability
    NewStock is Stock - Qty,

    % update stock
    retract(item(Name, Price, Stock)),
    assertz(item(Name, Price, NewStock)),

    % add/update order
    ( retract(order(Name, OldQty)) ->
        NewQty is OldQty + Qty
    ;
        NewQty is Qty
    ),
    assertz(order(Name, NewQty)),

    write('Order placed'), nl.

place_order(Name, _) :-
    write('Item not available or insufficient stock'), nl.

% -------- Delete Order --------
delete_order(Name) :-
    retractall(order(Name, _)),
    write('Order removed'), nl.

% -------- Display Bill --------
display_bill :-
    write('------- CUSTOMER BILL -------'), nl,
    write('Item\tPrice\tQty\tSubtotal'), nl,
    show_orders,
    grand_total(Total),
    write('-----------------------------'), nl,
    write('Grand Total = '), write(Total), nl.

% -------- Show Ordered Items --------
show_orders :-
    order(Name, Qty),
    item(Name, Price, _),
    Subtotal is Price * Qty,
    write(Name), write('\t'),
    write(Price), write('\t'),
    write(Qty), write('\t'),
    write(Subtotal), nl,
    fail.
show_orders.

% -------- Grand Total --------
grand_total(Total) :-
    findall(Sub,
        (order(Name, Qty), item(Name, Price, _), Sub is Price*Qty),
        List),
    sum_list(List, Total).

OUTPUT:
?- add_item(rice, 50, 2).
Item added to store
true.

?- add_item(milk, 30, 3).
Item added to store
true.

?- place_order(rice, 2).
Order placed
true .

?- display_bill.
------- CUSTOMER BILL -------
Item    Price   Qty     Subtotal
rice    50      2       100
-----------------------------
Grand Total = 100
true.

?- place_order(milk, 3).
Order placed
true .

?- display_bill.
------- CUSTOMER BILL -------
Item    Price   Qty     Subtotal
rice    50      2       100
milk    30      3       90
-----------------------------
Grand Total = 190
true.

?- place_order(rice, 2).
Item not available or insufficient stock
true.

?-  add_item(rice, 50, 5).
Item added to store
true.

?- place_order(rice, 2).
Order placed
true .

?- display_bill.
------- CUSTOMER BILL -------
Item    Price   Qty     Subtotal
milk    30      3       90
rice    50      4       200
rice    50      4       200
-----------------------------
Grand Total = 490
true.
