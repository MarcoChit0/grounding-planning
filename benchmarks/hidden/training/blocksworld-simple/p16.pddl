

(define (problem pr16)
 (:domain d1)
 (:objects o1 o12 o23 o24 o25 - object)
 (:init 
    (p1)
    (p2 o12)
    (p4 o12 o25)
    (p4 o25 o24)
    (p4 o24 o23)
    (p4 o23 o1)
    (p5 o1))
 (:goal  (and 
    (p2 o12)
    (p4 o12 o1)
    (p4 o1 o23)
    (p4 o23 o24)
    (p4 o24 o25)
    (p5 o25))))
