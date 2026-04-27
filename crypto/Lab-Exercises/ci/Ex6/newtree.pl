% =====================================================
% TRAVANCORE ROYAL FAMILY TREE
% =====================================================

% ========================
% FACTS: parent
% ========================

% ---------- Generation 1 ----------
parent(attingal_elaya_thampuran, sethu_lakshmi_bayi).
parent(attingal_elaya_thampuran, sethu_parvathi_bayi).
parent(attingal_elaya_thampuran, other_sister_1).

% ---------- Generation 2 ----------
parent(sethu_parvathi_bayi, chithira_thirunal).
parent(sethu_parvathi_bayi, uthradom_thirunal).
parent(sethu_parvathi_bayi, karthika_thirunal).

% ---------- Generation 3 ----------
parent(karthika_thirunal, pooyam_thirunal).
parent(karthika_thirunal, aswathi_thirunal).

parent(pooyam_thirunal, moolam_thirunal).
parent(pooyam_thirunal, revathi_thirunal).

% ---------- Generation 4 ----------
parent(moolam_thirunal, prince_kerala_varma).
parent(moolam_thirunal, princess_lakshmi_bayi).
parent(moolam_thirunal, prince_aditya_varma).
parent(moolam_thirunal, princess_gowri_parvathi).

parent(aswathi_thirunal, shreekumar_varma).
parent(aswathi_thirunal, princess_rukmini).

% ---------- Generation 5 ----------
parent(princess_lakshmi_bayi, princess_saraswati_lakshmi).
parent(princess_lakshmi_bayi, prince_jayanta_thirunal_iii).
parent(princess_lakshmi_bayi, prince_narayana_varma_iii).

parent(princess_rukmini, princess_maya_lakshmi).
parent(shreekumar_varma, princess_gowri_parvathi).


% ========================
% FACTS: gender
% ========================

gender(attingal_elaya_thampuran, female).
gender(sethu_lakshmi_bayi, female).
gender(sethu_parvathi_bayi, female).
gender(other_sister_1, female).

gender(chithira_thirunal, male).
gender(uthradom_thirunal, male).
gender(karthika_thirunal, female).

gender(pooyam_thirunal, female).
gender(aswathi_thirunal, female).
gender(moolam_thirunal, male).
gender(revathi_thirunal, male).

gender(prince_kerala_varma, male).
gender(princess_lakshmi_bayi, female).
gender(princess_gowri_parvathi, female).
gender(prince_aditya_varma, male).
gender(shreekumar_varma, male).
gender(princess_rukmini, female).

gender(princess_saraswati_lakshmi, female).
gender(prince_jayanta_thirunal_iii, male).
gender(prince_narayana_varma_iii, male).
gender(princess_maya_lakshmi, female).
gender(princess_gowri_parvathi, female).


% =====================================================
% RELATIONSHIPS (UNCHANGED)
% =====================================================

mother(Mother, Child) :-
    parent(Mother, Child),
    gender(Mother, female).

father(Father, Child) :-
    parent(Father, Child),
    gender(Father, male).

sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

brother(Brother, Person) :-
    sibling(Brother, Person),
    gender(Brother, male).

sister(Sister, Person) :-
    sibling(Sister, Person),
    gender(Sister, female).

grandparent(GP, GC) :-
    parent(GP, P),
    parent(P, GC).

grandmother(GM, GC) :-
    grandparent(GM, GC),
    gender(GM, female).

grandfather(GF, GC) :-
    grandparent(GF, GC),
    gender(GF, male).

aunt(Aunt, Person) :-
    parent(P, Person),
    sister(Aunt, P).

uncle(Uncle, Person) :-
    parent(P, Person),
    brother(Uncle, P).

nephew(Nephew, Person) :-
    sibling(Parent, Person),
    parent(Parent, Nephew),
    gender(Nephew, male).

niece(Niece, Person) :-
    sibling(Parent, Person),
    parent(Parent, Niece),
    gender(Niece, female).

cousin(X, Y) :-
    parent(P1, X),
    parent(P2, Y),
    sibling(P1, P2),
    X \= Y.

ancestor(A, D) :- parent(A, D).
ancestor(A, D) :-
    parent(A, X),
    ancestor(X, D).

descendant(D, A) :- ancestor(A, D).

generation(attingal_elaya_thampuran, 0).

generation(Person, N) :-
    parent(P, Person),
    generation(P, N1),
    N is N1 + 1.
