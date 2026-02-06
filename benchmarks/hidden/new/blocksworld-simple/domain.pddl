

(define (domain d1)

(:requirements :strips)

(:predicates (p2 ?v3)
             (p5 ?v3)
             (p1)
             (p3 ?v3)
             (p4 ?v3 ?v4))

(:action a1
  :parameters (?v1)
  :precondition (and (p2 ?v1) (p5 ?v1) (p1))
  :effect (and (p3 ?v1) (not (p2 ?v1)) (not (p5 ?v1)) 
               (not (p1))))

(:action a2
  :parameters  (?v1)
  :precondition (p3 ?v1)
  :effect (and (p2 ?v1) (p1) (p5 ?v1) 
               (not (p3 ?v1))))

(:action a3
  :parameters  (?v1 ?v2)
  :precondition (and (p2 ?v2) (p3 ?v1))
  :effect (and (p1) (p2 ?v1) (p4 ?v1 ?v2)
               (not (p2 ?v2)) (not (p3 ?v1))))

(:action a4
  :parameters  (?v1 ?v2)
  :precondition (and (p4 ?v1 ?v2) (p2 ?v1) (p1))
  :effect (and (p3 ?v1) (p2 ?v2)
               (not (p4 ?v1 ?v2)) (not (p2 ?v1)) (not (p1)))))
