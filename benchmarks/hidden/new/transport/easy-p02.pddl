

(define (problem pr2)
 (:domain d1)
 (:objects 
    o297 o308 o319 - t5
    o109 o209 - t3
    o12 o23 o34 o45 o56 - t2
    o1 o2 o4 - t4
    )
 (:init (p2 o297 o2)
    (p2 o308 o4)
    (p2 o319 o2)
    (p3 o1 o2)
    (p3 o2 o4)
    (p1 o109 o45)
    (p1 o209 o34)
    (p1 o297 o12)
    (p1 o308 o45)
    (p1 o319 o56)
    (p5 o23 o45)
    (p5 o12 o23)
    (p5 o23 o12)
    (p5 o45 o23)
    (p5 o23 o34)
    (p5 o34 o23)
    (p5 o23 o56)
    (p5 o56 o23)
    )
 (:goal  (and 
    (p1 o109 o23)
    (p1 o209 o56))))
