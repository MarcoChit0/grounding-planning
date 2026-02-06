

(define (problem pr3)
 (:domain d1)
 (:objects  o1 o12 - object)
 (:init 
    (p1)
    (p2 o1)
    (p4 o1 o12)
    (p5 o12)
)
 (:goal (and
    (p2 o12)
    (p5 o12)
    (p2 o1)
    (p5 o1)
)))