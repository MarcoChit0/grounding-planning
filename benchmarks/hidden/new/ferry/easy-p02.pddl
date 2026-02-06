

(define (problem pr2)
 (:domain d1)
 (:objects 
    o1 o112 o223 - t1
    o948 o1059 o1170 o1281 o1367 - t2
 )
 (:init 
    (p3)
    (p2 o948)
    (p1 o1 o1170)
    (p1 o112 o1059)
    (p1 o223 o1281)
)
 (:goal  (and (p1 o1 o1281)
   (p1 o112 o948)
   (p1 o223 o1367))))
