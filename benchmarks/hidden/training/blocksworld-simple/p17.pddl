

(define (problem pr17)
 (:domain d1)
 (:objects o1 o12 o23 o24 o25 - object)
 (:init 
    (p1)
    (p2 o23)
    (p4 o23 o12)
    (p4 o12 o25)
    (p5 o25)
    (p2 o1)
    (p4 o1 o24)
    (p5 o24))
 (:goal  (and 
    (p2 o12)
    (p4 o12 o23)
    (p4 o23 o24)
    (p4 o24 o25)
    (p4 o25 o1)
    (p5 o1))))
