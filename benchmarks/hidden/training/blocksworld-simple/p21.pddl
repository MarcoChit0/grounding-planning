

(define (problem pr21)
 (:domain d1)
 (:objects o1 o12 o23 o24 o25 o26 - object)
 (:init 
    (p1)
    (p2 o1)
    (p4 o1 o24)
    (p4 o24 o26)
    (p4 o26 o12)
    (p4 o12 o23)
    (p4 o23 o25)
    (p5 o25))
 (:goal  (and 
    (p2 o12)
    (p4 o12 o25)
    (p4 o25 o23)
    (p4 o23 o24)
    (p4 o24 o1)
    (p4 o1 o26)
    (p5 o26))))
