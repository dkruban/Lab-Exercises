% A collection of predicates for set operations on lists.

% Membership: Checks if an element is a member of a set (list).
% Usage: is_member(Element, Set)

is_member(X, [X|_]).
is_member(X, [_|Tail]) :-
    is_member(X, Tail).
% Subset: Checks if the first set is a subset of the second.
% All elements of Set1 must be members of Set2.
% Usage: is_subset(Set1, Set2)

is_subset([], _).
is_subset([Head|Tail], Set2) :-
    is_member(Head, Set2),
    is_subset(Tail, Set2).

% Union: The third argument is the union of the first two sets.
% The resulting set contains all unique elements from both sets.
% Usage: union_of(Set1, Set2, Union)

union_of([], Set, Set).
union_of([Head|Tail], Set2, Union) :-
    is_member(Head, Set2),
    !,
    union_of(Tail, Set2, Union).
union_of([Head|Tail], Set2, [Head|Union]) :-
    union_of(Tail, Set2, Union).

% Intersection: The third argument is the intersection of the first two.
% The resulting set contains elements that are in both sets.
% Usage: intersection_of(Set1, Set2, Intersection)

intersection_of([], _, []).
intersection_of([Head|Tail], Set2, [Head|Intersection]) :-
    is_member(Head, Set2),
    !,
    intersection_of(Tail, Set2, Intersection).
intersection_of([_|Tail], Set2, Intersection) :-
    intersection_of(Tail, Set2, Intersection).

% Difference: The third argument is the difference of Set1 and Set2.
% The resulting set contains elements of Set1 that are not in Set2.
% Usage: difference_of(Set1, Set2, Difference)

difference_of([], _, []).
difference_of([Head|Tail], Set2, Difference) :-
    is_member(Head, Set2),
    !,
    difference_of(Tail, Set2, Difference).
difference_of([Head|Tail], Set2, [Head|Difference]) :-
    difference_of(Tail, Set2, Difference).

% Symmetric Difference: The third argument is the symmetric difference
% of the first two sets (elements in one, but not both).
% Usage: symmetric_difference_of(Set1, Set2, SymDifference)

symmetric_difference_of(Set1, Set2, Result) :-
    union_of(Set1, Set2, Union),
    intersection_of(Set1, Set2, Intersection),
    difference_of(Union, Intersection, Result).
% Equality: Checks if two sets are equal.
% Two sets are equal if they are subsets of each other.
% Usage: equal_sets(Set1, Set2)

equal_sets(Set1, Set2) :-
    is_subset(Set1, Set2),
    is_subset(Set2, Set1).
