

(define (problem pr4)
 (:domain d1)
 (:objects o1 o112 o223 o334 o434 o445 o456 - object)
 (:init 
    (p1)
    (p2 o334)
    (p4 o334 o223)
    (p4 o223 o456)
    (p4 o456 o1)
    (p4 o1 o112)
    (p4 o112 o434)
    (p4 o434 o445)
    (p5 o445))
 (:goal  (and 
    (p2 o334)
    (p4 o334 o1)
    (p4 o1 o112)
    (p4 o112 o223)
    (p4 o223 o434)
    (p4 o434 o445)
    (p4 o445 o456)
    (p5 o456))))
