

(define (problem pr20)
 (:domain d1)
 (:objects o1 o12 o23 o24 o25 o26 - object)
 (:init 
    (p1)
    (p2 o25)
    (p4 o25 o12)
    (p4 o12 o26)
    (p4 o26 o24)
    (p4 o24 o1)
    (p4 o1 o23)
    (p5 o23))
 (:goal  (and 
    (p2 o23)
    (p4 o23 o26)
    (p5 o26)
    (p2 o12)
    (p4 o12 o1)
    (p4 o1 o25)
    (p4 o25 o24)
    (p5 o24))))
