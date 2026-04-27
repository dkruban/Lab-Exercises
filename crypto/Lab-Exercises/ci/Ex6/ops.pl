% --- Arithmetic Operations ---
% Usage: calculate(Operation, A, B, Result).

add(A, B, X)      :- X is A + B.
subtract(A, B, X) :- X is A - B.
divide(A, B, X)   :- X is A / B.
power(A, B, X)    :- X is A ** B.
modulo(A, B, X)   :- X is A mod B.

% --- Set Operation: Intersection ---
% intersection(List1, List2, Result).

% 1. Base case: intersection with an empty list is empty.
intersection([], _, []).

% 2. If Head (H) is in List2, include it in the result and recurse.
intersection([H|T], L2, [H|Res]) :-
    member(H, L2),
    !,
    intersection(T, L2, Res).

% 3. If Head is NOT in List2, skip it and recurse.
intersection([_|T], L2, Res) :-
    intersection(T, L2, Res).

