

(define (problem pr3)
 (:domain d1)
 (:objects o1 o112 o223 o334 o434 o445 - object)
 (:init 
    (p1)
    (p2 o223)
    (p4 o223 o445)
    (p4 o445 o434)
    (p4 o434 o334)
    (p4 o334 o1)
    (p4 o1 o112)
    (p5 o112))
 (:goal  (and 
    (p2 o334)
    (p4 o334 o223)
    (p4 o223 o434)
    (p4 o434 o112)
    (p4 o112 o445)
    (p4 o445 o1)
    (p5 o1))))
