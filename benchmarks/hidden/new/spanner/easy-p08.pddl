

(define (problem pr8)
 (:domain d1)
 (:objects 
    o1 - t3
    o338 o449 o560 o671 o757 - d1
    o100 o211 o260 - t4
    o337 o3 o14 o25 o36 o47 o58 o69 o2 - t2
 )
 (:init 
    (p1 o1 o337)
    (p1 o338 o3)
    (p6 o338)
    (p1 o449 o25)
    (p6 o449)
    (p1 o560 o36)
    (p6 o560)
    (p1 o671 o3)
    (p6 o671)
    (p1 o757 o25)
    (p6 o757)
    (p1 o100 o2)
    (p4 o100)
    (p1 o211 o2)
    (p4 o211)
    (p1 o260 o2)
    (p4 o260)
    (p3 o337 o3)
    (p3 o69 o2)
    (p3 o3 o14)
     (p3 o14 o25)
     (p3 o25 o36)
     (p3 o36 o47)
     (p3 o47 o58)
     (p3 o58 o69)
 )
 (:goal  (and (p5 o100)
   (p5 o211)
   (p5 o260))))
