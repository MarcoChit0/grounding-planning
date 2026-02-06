

(define (domain d1)
  (:requirements :strips :typing)
  (:types t2 - object
          t1 - object
         )

(:predicates 
(p5 ?v8 - t2 ?v4 - t1)



(p3 ?v8 - t2 ?v4 - t1)



(p1 ?v5 - t1  ?v6 - t1)


(p2 ?v8 - t2)


(p6 ?v8 - t2)


(p4 ?v4 - t1)

)




(:action a1
  :parameters (?v1 - t1 ?v7 - t2)
  :precondition (and (p4 ?v1) (p5 ?v7 ?v1))
  :effect (and (p2 ?v7) (not (p5 ?v7 ?v1))))

(:action a2
  :parameters (?v1 - t1 ?v7 - t2)
  :precondition (and (p4 ?v1) (p3 ?v7 ?v1)
		     (p2 ?v7))
  :effect (and (not (p2 ?v7))
	       (p6 ?v7)))


(:action a4
  :parameters (?v2 - t1 ?v3 - t1)
  :precondition (and (p4 ?v2) (p1 ?v2 ?v3))
  :effect (and (p4 ?v3) (not (p4 ?v2))))




(:action a3
  :parameters (?v2 - t1 ?v3 - t1)
  :precondition (and (p4 ?v2) (p1 ?v3 ?v2))
  :effect (and (p4 ?v3) (not (p4 ?v2))))
)



