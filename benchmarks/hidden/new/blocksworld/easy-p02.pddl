

(define (problem pr2)
 (:domain d1)
 (:objects o1 o112 o223 o334 o423 o434 - object)
 (:init 
    (p1)
    (p2 o434)
    (p4 o434 o423)
    (p4 o423 o334)
    (p4 o334 o112)
    (p4 o112 o223)
    (p4 o223 o1)
    (p5 o1))
 (:goal  (and 
    (p2 o434)
    (p4 o434 o112)
    (p4 o112 o223)
    (p4 o223 o334)
    (p4 o334 o423)
    (p4 o423 o1)
    (p5 o1))))
