



(define (domain d1)
(:requirements :typing)
(:types t3 t2 t1)

(:constants o79 o9686 o80 o9685 - t2)

(:predicates
             (p3 ?v7 - t3)
             (p2 ?v10 - t1 ?v7 - t3)
             (p1 ?v8 - t3 ?v9 - t3 ?v3 - t2) 
             (p4 ?v7 - t3)
)

(:action a1
:parameters (?v6 - t3 ?v12 - t3 ?v4 - t2)
:precondition (and (p4 ?v12) (p3 ?v6) (p1 ?v6 ?v12 ?v4))
:effect (and (p3 ?v12) (not (p3 ?v6)))
)
             

(:action a2
:parameters  (?v11 - t3 ?v2 - t3 ?v5 - t3 ?v4 - t2 ?v1 - t1)
:precondition (and (p3 ?v11) (p2 ?v1 ?v2) (p4 ?v5)
	           (p1 ?v11 ?v2 ?v4) (p1 ?v2 ?v5 ?v4))

:effect (and (p3 ?v2) (p2 ?v1 ?v5) (p4 ?v2)
             (not (p3 ?v11)) (not (p2 ?v1 ?v2)) (not (p4 ?v5)))
)
)

