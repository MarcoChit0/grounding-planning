

(define (problem pr3)
 (:domain d1)
 (:objects 
    o1 o112 o223 o334 - t1
    o948 o1059 o1170 o1281 o1367 o1378 - t2
 )
 (:init 
    (p3)
    (p2 o1281)
    (p1 o1 o1367)
    (p1 o112 o1367)
    (p1 o223 o1378)
    (p1 o334 o948)
)
 (:goal  (and (p1 o1 o1059)
   (p1 o112 o1281)
   (p1 o223 o1059)
   (p1 o334 o1281))))
