
(define (domain d1)
(:requirements :typing :strips)
(:types
	t2 t1 - object
	t3 t4 d1 - t1
)

(:predicates
	(p1 ?v5 - t1 ?v2 - t2)
	(p2 ?v5 - t3 ?v7 - d1)
	(p6 ?v7 - d1)
	(p3 ?v3 - t2 ?v4 - t2)
	(p5 ?v6 - t4)
	(p4 ?v6 - t4))

(:action a3
        :parameters (?v8 - t2 ?v1 - t2 ?v5 - t3)
        :precondition (and (p1 ?v5 ?v8)
                           (p3 ?v8 ?v1))
        :effect (and (not (p1 ?v5 ?v8)) (p1 ?v5 ?v1)))

(:action a1
        :parameters (?v2 - t2 ?v7 - d1 ?v5 - t3)
        :precondition (and (p1 ?v5 ?v2)
                           (p1 ?v7 ?v2))
        :effect (and (not (p1 ?v7 ?v2))
                     (p2 ?v5 ?v7)))

(:action a2
        :parameters (?v2 - t2 ?v7 - d1 ?v5 - t3 ?v6 - t4)
        :precondition (and (p1 ?v5 ?v2)
		      	   (p1 ?v6 ?v2)
			   (p2 ?v5 ?v7)
			   (p6 ?v7)
			   (p4 ?v6))
        :effect (and (not (p4 ?v6))(not (p6 ?v7)) (p5 ?v6)))
)