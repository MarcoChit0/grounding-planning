

(define (problem pr2)
 (:domain d1)
 (:objects 
    o1 - t3
    o338 - d1
    o100 - t4
    o337 o3 o14 o25 o36 o2 - t2
 )
 (:init 
    (p1 o1 o337)
    (p1 o338 o3)
    (p6 o338)
    (p1 o100 o2)
    (p4 o100)
    (p3 o337 o3)
    (p3 o36 o2)
    (p3 o3 o14)
     (p3 o14 o25)
     (p3 o25 o36)
 )
 (:goal  (and (p5 o100))))
