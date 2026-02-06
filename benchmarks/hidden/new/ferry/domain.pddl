

(define (domain d1)
   (:requirements :typing :strips :negative-preconditions)
   (:types
        t1 - object
        t2 - object )

   (:predicates
		(p2 ?v4 - t2)
		(p1 ?v1 - t1 ?v4 - t2)
		(p3)
		(p4 ?v1 - t1))

   (:action a3
       :parameters  (?v3 - t2 ?v6 - t2)
       :precondition (and (p2 ?v3) (not (p2 ?v6)))
       :effect (and  (p2 ?v6) (not (p2 ?v3))))


   (:action a1
       :parameters (?v2 - t1 ?v5 - t2)
       :precondition  (and  (p1 ?v2 ?v5) (p2 ?v5) (p3))
       :effect (and
            (p4 ?v2)
		    (not (p1 ?v2 ?v5)) 
		    (not (p3))))

   (:action a2
       :parameters  (?v2 - t1  ?v5 - t2)
       :precondition  (and (p4 ?v2) (p2 ?v5))
       :effect (and
            (p1 ?v2 ?v5)
		    (p3)
		    (not (p4 ?v2)))))
