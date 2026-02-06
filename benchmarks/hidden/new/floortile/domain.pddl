





(define (domain d1)
(:requirements :typing)
(:types t2 t3 t1 - object)

(:predicates
    (p8 ?v3 - t2 ?v4 - t3)
    (p10 ?v4 - t3 ?v5 - t3)
    (p3 ?v4 - t3 ?v5 - t3)
    (p7 ?v4 - t3 ?v5 - t3)
    (p5 ?v4 - t3 ?v5 - t3)
    (p2 ?v4 - t3)
    (p6 ?v4 - t3 ?v1 - t1)
    (p9 ?v3 - t2 ?v1 - t1)
    (p1 ?v1 - t1)
    (p4 ?v3 - t2))

(:action a1
  :parameters (?v3 - t2 ?v1 - t1 ?v2 - t1)
  :precondition (and (p9 ?v3 ?v1) (p1 ?v2))
  :effect (and (not (p9 ?v3 ?v1)) (p9 ?v3 ?v2))
)

(:action a7
  :parameters (?v3 - t2 ?v5 - t3 ?v4 - t3 ?v1 - t1)
  :precondition (and (p9 ?v3 ?v1) (p8 ?v3 ?v4) (p10 ?v5 ?v4) (p2 ?v5))
  :effect (and (not (p2 ?v5)) (p6 ?v5 ?v1))
)

(:action a6
  :parameters (?v3 - t2 ?v5 - t3 ?v4 - t3 ?v1 - t1)
  :precondition (and (p9 ?v3 ?v1) (p8 ?v3 ?v4) (p3 ?v5 ?v4) (p2 ?v5))
  :effect (and (not (p2 ?v5)) (p6 ?v5 ?v1))
)


(:action a5
  :parameters (?v3 - t2 ?v4 - t3 ?v5 - t3)
  :precondition (and (p8 ?v3 ?v4) (p10 ?v5 ?v4) (p2 ?v5))
  :effect (and (p8 ?v3 ?v5) (not (p8 ?v3 ?v4))
               (p2 ?v4) (not (p2 ?v5)))
)

(:action a2
  :parameters (?v3 - t2 ?v4 - t3 ?v5 - t3)
  :precondition (and (p8 ?v3 ?v4) (p3 ?v5 ?v4) (p2 ?v5))
  :effect (and (p8 ?v3 ?v5) (not (p8 ?v3 ?v4))
               (p2 ?v4) (not (p2 ?v5)))
)

(:action a4
  :parameters (?v3 - t2 ?v4 - t3 ?v5 - t3)
  :precondition (and (p8 ?v3 ?v4) (p7 ?v5 ?v4) (p2 ?v5))
  :effect (and (p8 ?v3 ?v5) (not (p8 ?v3 ?v4))
               (p2 ?v4) (not (p2 ?v5)))
)

(:action a3
  :parameters (?v3 - t2 ?v4 - t3 ?v5 - t3)
  :precondition (and (p8 ?v3 ?v4) (p5 ?v5 ?v4) (p2 ?v5))
  :effect (and (p8 ?v3 ?v5) (not (p8 ?v3 ?v4))
               (p2 ?v4) (not (p2 ?v5)))
)

)