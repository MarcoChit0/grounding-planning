





(define (domain d1)
(:requirements :strips :typing)
(:types d1 t7 t6 t1 t3 t2 t4)

(:predicates
    (p1 ?v11 - d1 ?v12 - t7)
    (p2 ?v11 - t2 ?v12 - t7)
    (p7 ?v7 - d1 ?v11 - t7 ?v12 - t7)
	(p14 ?v7 - d1)
    (p13 ?v7 - d1)
    (p12 ?v7 - d1)
    (p11 ?v8 - t6)
    (p17 ?v7 - d1 ?v10 - t7)
    (p18 ?v7 - d1 ?v10 - t7)
    (p15 ?v8 - t6)
	(p5 ?v1 - t1 ?v7 - d1)
	(p21 ?v1 - t1 ?v4 - t3)
    (p22 ?v10 - t7 ?v6 - t7)
    (p16 ?v7 - d1 ?v5 - t4 ?v4 - t3)
    (p10 ?v10 - t7)
    (p9 ?v10 - t7)
    (p8 ?v5 - t4 ?v4 - t3)
	(p4 ?v10 - t7)
	(p3 ?v10 - t7)
    (p23 ?v5 - t4 ?v10 - t7)
	(p20 ?v8 - t6 ?v7 - d1)
	(p6 ?v2 - t1 ?v5 - t4)
	(p19 ?v2 - t1 ?v7 - d1)
)

(:action a6
:parameters (?v11 - d1 ?v12 - t7 ?v13 - t7)
:precondition (and
    (p7 ?v11 ?v12 ?v13)
    (p1 ?v11 ?v12)
    (p22 ?v12 ?v13))
:effect (and
    (not (p1 ?v11 ?v12))
    (p1 ?v11 ?v13))
)

(:action a8
:parameters (?v11 - d1 ?v8 - t6 ?v6 - t7)
:precondition (and
    (p1 ?v11 ?v6)
    (p4 ?v6)
	(p14 ?v11)
	(p20 ?v8 ?v11)
	(p11 ?v8))
:effect (and
    (not (p11 ?v8))
    (p15 ?v8)
    (p18 ?v11 ?v6)
    (not (p4 ?v6)))
)

(:action a7
:parameters (?v11 - d1 ?v8 - t6 ?v6 - t7)
:precondition (and
    (p1 ?v11 ?v6)
    (p3 ?v6)
	(p13 ?v11)
	(p20 ?v8 ?v11)
	(p11 ?v8))
:effect (and
    (not (p11 ?v8))
    (p15 ?v8)
    (p17 ?v11 ?v6)
	(not (p3 ?v6)))
)

(:action a5
:parameters (?v11 - d1 ?v12 - t6)
:precondition (and
    (p20 ?v12 ?v11)
    (p15 ?v12))
:effect (and
    (not (p15 ?v12))
    (p11 ?v12))
)

(:action a1
 :parameters (?v7 - d1 ?v2 - t1 ?v9 - t4 ?v10 - t7)
 :precondition (and
    (p12 ?v7)
    (p6 ?v2 ?v9)
    (p1 ?v7 ?v10)
    (p23 ?v9 ?v10)
    (p19 ?v2 ?v7))
 :effect (and
    (p5 ?v2 ?v7))
)

(:action a9
 :parameters (?v7 - d1 ?v6 - t7 ?v5 - t4 ?v2 - t1 ?v4 - t3)
 :precondition (and
    (p5 ?v2 ?v7)
    (p19 ?v2 ?v7)
    (p12 ?v7)
    (p21 ?v2 ?v4)
    (p23 ?v5 ?v6)
    (p1 ?v7 ?v6))
 :effect (and
    (p16 ?v7 ?v5 ?v4)
    (not (p5 ?v2 ?v7)))
)

(:action a4
 :parameters (?v7 - d1 ?v3 - t2 ?v6 - t7 ?v11 - t7 ?v12 - t7)
 :precondition (and
    (p1 ?v7 ?v11)
    (p2 ?v3 ?v12)
    (p18 ?v7 ?v6)
    (p22 ?v11 ?v12))
 :effect (and
    (p10 ?v6))
)

(:action a3
 :parameters (?v7 - d1 ?v3 - t2 ?v6 - t7 ?v11 - t7 ?v12 - t7)
 :precondition (and
    (p1 ?v7 ?v11)
    (p2 ?v3 ?v12)
    (p17 ?v7 ?v6)
    (p22 ?v11 ?v12))
 :effect (and
    (p9 ?v6))
)

(:action a2
 :parameters (?v7 - d1 ?v3 - t2 ?v5 - t4 ?v4 - t3
	      ?v11 - t7 ?v12 - t7)
 :precondition (and
    (p1 ?v7 ?v11)
    (p2 ?v3 ?v12)
    (p16 ?v7 ?v5 ?v4)
    (p22 ?v11 ?v12))
 :effect (and
    (p8 ?v5 ?v4)))
)