




(define (domain d1)
  (:requirements :typing)
  (:types
        t4 t2 t1 - object
        t5 t3 - t1
  )

  (:predicates
     (p5 ?v2 ?v3 - t2)
     (p1 ?v8 - t1 ?v7 - t2)
     (p4 ?v8 - t3 ?v7 - t5)
     (p2 ?v7 - t5 ?v5 - t4)
     (p3 ?v5 ?v6 - t4)
  )

  (:action a1
    :parameters (?v7 - t5 ?v2 ?v3 - t2)
    :precondition (and
        (p1 ?v7 ?v2)
        (p5 ?v2 ?v3)
      )
    :effect (and
        (not (p1 ?v7 ?v2))
        (p1 ?v7 ?v3)
      )
  )

 (:action a3
    :parameters (?v7 - t5 ?v1 - t2 ?v4 - t3 ?v5 ?v6 - t4)
    :precondition (and
        (p1 ?v7 ?v1)
        (p1 ?v4 ?v1)
        (p3 ?v5 ?v6)
        (p2 ?v7 ?v6)
      )
    :effect (and
        (not (p1 ?v4 ?v1))
        (p4 ?v4 ?v7)
        (p2 ?v7 ?v5)
        (not (p2 ?v7 ?v6))
      )
  )

  (:action a2
    :parameters (?v7 - t5 ?v1 - t2 ?v4 - t3 ?v5 ?v6 - t4)
    :precondition (and
        (p1 ?v7 ?v1)
        (p4 ?v4 ?v7)
        (p3 ?v5 ?v6)
        (p2 ?v7 ?v5)
      )
    :effect (and
        (not (p4 ?v4 ?v7))
        (p1 ?v4 ?v1)
        (p2 ?v7 ?v6)
        (not (p2 ?v7 ?v5))
      )
  )

)