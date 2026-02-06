

(define (problem pr4)
 (:domain d1)
 (:objects 
    o1 o112 o223 o334 o445 - t1
    o948 o1059 o1170 o1281 o1367 o1378 o1389 - t2
 )
 (:init 
    (p3)
    (p2 o1170)
    (p1 o1 o1281)
    (p1 o112 o1281)
    (p1 o223 o1170)
    (p1 o334 o948)
    (p1 o445 o1170)
)
 (:goal  (and (p1 o1 o1170)
   (p1 o112 o948)
   (p1 o223 o948)
   (p1 o334 o1367)
   (p1 o445 o948))))
