

(define (problem pr5)
 (:domain d1)
 (:objects 
    o1 o112 o223 o334 o445 o556 o667 - t1
    o948 o1059 o1170 o1281 o1367 o1378 o1389 - t2
 )
 (:init 
    (p3)
    (p2 o948)
    (p1 o1 o1281)
    (p1 o112 o948)
    (p1 o223 o1367)
    (p1 o334 o1367)
    (p1 o445 o1389)
    (p1 o556 o1059)
    (p1 o667 o1378)
)
 (:goal  (and (p1 o1 o1378)
   (p1 o112 o1170)
   (p1 o223 o1378)
   (p1 o334 o1378)
   (p1 o445 o948)
   (p1 o556 o948)
   (p1 o667 o948))))
