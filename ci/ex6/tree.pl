% =====================================================
% TRAVANCORE ROYAL FAMILY TREE
% =====================================================
% ========================
% FACTS: parent/gender
% ========================
% ---------- Generation 1 ----------


parent(attingal_elaya_thampuran, sethu_lakshmi_bayi).
parent(attingal_elaya_thampuran, sethu_parvathi_bayi).
parent(attingal_elaya_thampuran, other_sister_1).

gender(attingal_elaya_thampuran, female).
gender(sethu_lakshmi_bayi, female).
gender(sethu_parvathi_bayi, female).
gender(other_sister_1, female).

% ---------- Generation 2 ----------
parent(sethu_parvathi_bayi, chithira_thirunal).
parent(sethu_parvathi_bayi, uthradom_thirunal).
parent(sethu_parvathi_bayi, karthika_thirunal).

gender(chithira_thirunal, male).
gender(uthradom_thirunal, male).
gender(karthika_thirunal, female).

% ---------- Generation 3 ----------
parent(karthika_thirunal, pooyam_thirunal).
parent(karthika_thirunal, aswathi_thirunal).

parent(pooyam_thirunal, moolam_thirunal).
parent(pooyam_thirunal, revathi_thirunal).

gender(pooyam_thirunal, female).
gender(aswathi_thirunal, female).
gender(moolam_thirunal, male).
gender(revathi_thirunal, male).

% ---------- Generation 4 ----------
parent(moolam_thirunal, prince_kerala_varma).
parent(moolam_thirunal, princess_lakshmi_bayi).

parent(aswathi_thirunal, shreekumar_varma).
parent(aswathi_thirunal, princess_rukmini).

gender(prince_kerala_varma, male).
gender(princess_lakshmi_bayi, female).
gender(shreekumar_varma, male).
gender(princess_rukmini, female).

% ---------- Generation 5 ----------
parent(princess_lakshmi_bayi, princess_arya_varma).
parent(princess_lakshmi_bayi, prince_aditya_varma).

parent(princess_rukmini, princess_maya_lakshmi).
parent(shreekumar_varma, princess_gowri_parvathi).

gender(princess_arya_varma, female).
gender(prince_aditya_varma, male).
gender(princess_maya_lakshmi, female).
gender(princess_gowri_parvathi, female).

% ---------- Generation 6 ----------
parent(princess_arya_varma, princess_lakshmi_devi).
parent(princess_arya_varma, prince_rama_varma_iii).

parent(princess_maya_lakshmi, princess_kamala_devi).
parent(princess_maya_lakshmi, prince_balarama_thirunal_ii).

parent(princess_gowri_parvathi, princess_rukmini_thirunal).
parent(princess_gowri_parvathi, prince_vikrama_varma).

gender(princess_lakshmi_devi, female).
gender(prince_rama_varma_iii, male).
gender(princess_kamala_devi, female).
gender(prince_balarama_thirunal_ii, male).
gender(princess_rukmini_thirunal, female).
gender(prince_vikrama_varma, male).

% ---------- Generation 7 ----------
parent(princess_lakshmi_devi, princess_saraswati_lakshmi).
parent(princess_lakshmi_devi, prince_jayanta_thirunal_iii).

parent(princess_kamala_devi, princess_parvathi_devi).
parent(princess_kamala_devi, prince_narayana_varma_iii).

gender(princess_saraswati_lakshmi, female).
gender(prince_jayanta_thirunal_iii, male).
gender(princess_parvathi_devi, female).
gender(prince_narayana_varma_iii, male).


% =====================================================
% RELATIONSHIPS
% =====================================================

% Mother
mother(Mother, Child) :-
    parent(Mother, Child),
    gender(Mother, female).

% Father
father(Father, Child) :-
    parent(Father, Child),
    gender(Father, male).

% Siblings
sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

% Brother
brother(Brother, Person) :-
    sibling(Brother, Person),
    gender(Brother, male).

% Sister
sister(Sister, Person) :-
    sibling(Sister, Person),
    gender(Sister, female).

% Grandparent
grandparent(GP, GC) :-
    parent(GP, P),
    parent(P, GC).

% Grandmother
grandmother(GM, GC) :-
    grandparent(GM, GC),
    gender(GM, female).

% Grandfather
grandfather(GF, GC) :-
    grandparent(GF, GC),
    gender(GF, male).

% Aunt
aunt(Aunt, Person) :-
    parent(P, Person),
    sister(Aunt, P).

% Uncle
uncle(Uncle, Person) :-
    parent(P, Person),
    brother(Uncle, P).

% Nephew
nephew(Nephew, Person) :-
    sibling(Parent, Person),
    parent(Parent, Nephew),
    gender(Nephew, male).

% Niece
niece(Niece, Person) :-
    sibling(Parent, Person),
    parent(Parent, Niece),
    gender(Niece, female).

% Cousin
cousin(X, Y) :-
    parent(P1, X),
    parent(P2, Y),
    sibling(P1, P2),
    X \= Y.

% Ancestor
ancestor(A, D) :- parent(A, D).
ancestor(A, D) :-
    parent(A, X),
    ancestor(X, D).

% Descendant
descendant(D, A) :- ancestor(A, D).

% Generation
generation(attingal_elaya_thampuran, 0).

generation(Person, N) :-
    parent(P, Person),
    generation(P, N1),
    N is N1 + 1.
