

(define (problem pr5)
 (:domain d1)
 (:objects  o1 o12 o23 - object)
 (:init 
    (p1)
    (p2 o23)
    (p4 o23 o12)
    (p4 o12 o1)
    (p5 o1)
)
 (:goal (and 
    (p2 o23)
    (p5 o23)
    (p2 o12)
    (p5 o12)
    (p2 o1)
    (p5 o1)
)))
