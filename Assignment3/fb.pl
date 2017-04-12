%%%%%%%%%%%  PART 1 %%%%%%%%%%%%%%%%%%

%%% SUCCESSOR %%%

%	∀n successor(n) ≠ 0.
%	∀m, n  m ≠ n ⇒ S(m) ≠ S(n).
%	∀m, n successor(m, n) ⇔ m + 1 = n

%Ns successor is Y
successor(N,Y) :-
	var(N) ->
	N is Y - 1;
	Y is N + 1.
	
%%% NATURAL NUMBER %%%
%	NatNum(0).  
%	∀n natNum(n)⇒NatNum(S(n)).	

natNum(0).
natNum(0.0).
natNum(X) :-
	successor(Y, X),
	Y >= 0,
	natNum(Y).

%%% ADDITION %%%
%	∀m natNum(m) ⇒ +(0, m) = 0.
%	∀m, n natNum(m) ∧ natNum(n) ⇔ +(S(m), n) = S(+(m, n)).

plus(X, 0, X).
plus(X, Y, OUT) :-
	successor(X , XX),
	successor(Yy, Y),
	plus(XX, Yy, OUT).

%%% MULTIPLICATION %%%
%	∀m natNum(m) ⇒ *(m, 0) = 0
%	∀m, n natNum(m) ∧ natNum(n) ⇔ *(S(m), n) = +(*(m, n), m).

mult(X, Y, OUT) :-
	multHelper(X, X, Y, OUT).

multHelper(X,_,1,X).
multHelper(X, ConstantX, Y, OUT):-
	plus(X, ConstantX, AddOut),
	successor(Yy, Y),
	multHelper(AddOut, ConstantX, Yy, OUT).

%%% EXPONENTIATION %%%
%	∀m natNum(m) ⇒ ^(m, 0) = 1
%	∀m, n natNum(m) ∧ natNum(n) ⇒ ^(m, S(n)) = *(^(m, n), m).

exp(X, Y, OUT):-
	expHelper(X, X, Y, OUT).

expHelper(X, _, 1, X).
expHelper(X, ConstantX, Y, OUT):-
	mult(X, ConstantX, MultOut),
	successor(Yy, Y),
	expHelper(MultOut, ConstantX, Yy, OUT).



%%%%%%%%%%%  PART 2 %%%%%%%%%%%%%%%%%%

child(william, diana).
child(william, charles).
child(harry, diana).
child(harry, charles).
child(peter, anne).
child(peter, mark).
child(zara, mark).
child(zara, anne).
child(beatrice, andrew).
child(beatrice, sarah).
child(eugine, andrew).
child(eugine, sarah).
child(louise, edward).
child(louise, sophie).
child(james, edward).
child(james, sophie).
child(diana, spencer).
child(diana, kydd).
child(charles, elizabeth).
child(charles, philip).
child(anne, elizabeth).
child(anne, philip).
child(andrew, elizabeth).
child(andrew, philip).
child(edward, elizabeth).
child(edward, philip).
child(elizabeth, george).
child(elizabeth, mum).
child(margaret, mum).
child(margaret, gerorge).

male(charles).
male(william).
male(harry).
male(spencer).
male(peter).
male(mark).
male(george).
male(eugine).
male(james).
male(edward).
male(andrew).
male(philip).

female(mum).
female(elizabeth).
female(diana).
female(zara).
female(anne).
female(kydd).
female(margaret).
female(beatrice).
female(louise).
female(sophie).
female(sarah).

spouse(spencer, kydd).
spouse(diana, charles).
spouse(anne, mark).
spouse(elizabeth, philip).
spouse(george, mum).
spouse(andrew, sarah).
spouse(edward, sophie).

%	FOPL: ∀(x, y) grandchild(x,y) ⇔ E p  child(x, p) ∧ child(p, y)
grandchild(C, G) :-
	child(C, P),
	child(P, G).

%	FOPL: ∀(x, y) greatGrandChild(x, y) ⇔ E g, p child(g, x) ∧ child(p, g) ∧ child(y, p)
greatGrandParent(A, C) :-
	child(G, A),
	child(P, G),
	child(C, P).

%	FOPL: ∀(x, y) ancestor(x,y) ⇔ E c (child(y, x)) ∨ (child(c, x) ∧ ancestor(c, y)) 
ancestor(A, X) :-
	child(X, A).

ancestor(A, X) :-
	child(X, C),
	ancestor(A, C). 

%	FOPL: ∀(x, y) brother(x, y) ⇔ E z male(x) ∧ child(x, z) ∧ child(y, z)
brother(X, Y):-
	male(X),
	child(X, Z),
	child(Y, Z),
	female(Z).

%	FOPL: ∀(x, y) sister(x, y) ⇔ E z female(x) ∧ child(x, z) ∧ child(y, z)
sister(X, Y) :-
	female(X),
	child(X, Z),
	child(Y, Z),
	female(Z).

%	FOPL: ∀(x, y) daughter(x, y) ⇔ female(x) ∧ child(x, y)
daughter(X, Y) :-
	female(X),
	child(X, Y).

%	FOPL: ∀(x, y) son(x, y) ⇔ male(x) ∧ child(x, y)
son(X, Y):-
	male(X),
	child(X, Y).

%	FOPL: ∀(x, y) sibling(x, y) ⇔ E z child(x, z) ∧ child(y, z)
sibling(X, Y):-
	child(X, Z),
	child(Y, Z), 
	Y \= X,
	female(Z).

%	FOPL: ∀(x, y) firstCousin(x, y) ⇔ E p1, p2, g child(x, p1) ∧ child(y, p2) ∧ child(p1, g) ∧ child(p2, g)
firstCousin(X, Y) :-
	child(X, P1),
	child(Y, P2),
	P1 \= P2,
	child(P1, G),
	child(P2, G),
	female(G),
	X \= Y.

%	FOPL: ∀(x, y) brotherinlaw(x, y) ⇔ E s, p male(x) ∧ (spouse(s, x) ∧ child(s, p) ∧ child(y, p)) ∨ (child(x, p) ∧ child(s, p) ∧ spouse(s, y))

brotherinlaw(X, Y) :-
	male(X),
	(
	(spouse(X, S) ; spouse(S, X)),
	child(S, P),
	female(P),
	child(Y, P),
	Y \= S
	);(
	child(X, P),
	female(P),
	child(S, P),
	S \= X,
	(spouse(S, Y) ; spouse(Y, S))
	).

%	FOPL: ∀(x, y) sisterinlaw(x, y) ⇔ E s, p female(x) ∧ (spouse(s, x) ∧ child(s, p) ∧ child(y, p)) ∨ (child(x, p) ∧ child(s, p) ∧ spouse(s, y))

sisterinlaw(X, Y) :-
	female(X),
	(
	(spouse(X, S) ; spouse(S, X)),
	child(S, P),
	female(P),
	child(Y, P),
	Y \= S
	);(
	child(X, P),
	female(P),
	child(S, P),
	S \= X,
	(spouse(S, Y) ; spouse(Y, S))
	).

%	FOPL ∀(x, y) aunt(x, y) ⇔ E p, c female(x) ∧ (child(x, p) ∧ child(c, p) ∧ child(y, c)) ∨ (spouse(x, s) ∧ child(s, p) ∧ child(c, p) ∧ child(y, c))
aunt(X, Y) :-
	female(X),
	(
	child(X, P),
	female(P),
	child(C, P),
	X \= C,
	child(Y, C)
	);(
	(spouse(X, S);spouse(S, X)),
	child(S, P),
	female(P),
	child(C, P),
	S \= C,
	child(Y, C)
	).

%	FOPL ∀(x, y) uncle(x, y) ⇔ E p, c male(x) ∧ (child(x, p) ∧ child(c, p) ∧ child(y, c)) ∨ (spouse(x, s) ∧ child(s, p) ∧ child(c, p) ∧ child(y, c))
uncle(X, Y) :-
	male(X),
	(
	child(X, P),
	female(P),
	child(C, P),
	X \= C,
	child(Y, C)
	);(
	(spouse(X, S);spouse(S, X)),
	child(S, P),
	female(P),
	child(C, P),
	S \= C,
	child(Y, C)
	).