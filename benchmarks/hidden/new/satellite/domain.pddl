




(define (domain d1)
  (:requirements :strips :typing :negative-preconditions)
  (:types d1 t1 t2 t3)
  (:predicates
	(p4 ?v4 - t2 ?v6 - d1)
	(p8 ?v4 - t2 ?v5 - t3)
	(p5 ?v6 - d1 ?v1 - t1)
	(p6 ?v6 - d1)
	(p7 ?v4 - t2)
	(p1 ?v4 - t2)
	(p3 ?v1 - t1 ?v5 - t3)
	(p2 ?v4 - t2 ?v1 - t1))

  (:action a5
   :parameters (?v6 - d1 ?v2 - t1 ?v3 - t1)
   :precondition (and
        (p5 ?v6 ?v3)
        (not (p5 ?v6 ?v2)))
   :effect (and
        (p5 ?v6 ?v2)
        (not (p5 ?v6 ?v3))))

  (:action a3
   :parameters (?v4 - t2 ?v6 - d1)
   :precondition (and
        (p4 ?v4 ?v6)
        (p6 ?v6))
   :effect (and
        (p7 ?v4)
        (not (p1 ?v4))
        (not (p6 ?v6))))

  (:action a2
   :parameters (?v4 - t2 ?v6 - d1)
   :precondition (and (p4 ?v4 ?v6)
                      (p7 ?v4))
   :effect (and (not (p7 ?v4))
                (p6 ?v6)))

  (:action a1
   :parameters (?v6 - d1 ?v4 - t2 ?v1 - t1)
   :precondition (and (p4 ?v4 ?v6)
		      (p2 ?v4 ?v1)
                      (p5 ?v6 ?v1)
                      (p7 ?v4))
   :effect (p1 ?v4))

  (:action a4
   :parameters (?v6 - d1 ?v1 - t1 ?v4 - t2 ?v5 - t3)
   :precondition (and (p1 ?v4)
                      (p4 ?v4 ?v6)
                      (p8 ?v4 ?v5)
                      (p7 ?v4)
                      (p5 ?v6 ?v1))
   :effect (p3 ?v1 ?v5)))
