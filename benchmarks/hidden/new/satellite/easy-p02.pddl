

(define (problem pr2)
 (:domain d1)
 (:objects 
    o297 o308 o319 - d1
    o97 o199 o210 o221 - t2
    o287 - t3
    o1 o12 o23 o34 - t1
    )
 (:init 
    (p5 o297 o1)
    (p5 o308 o23)
    (p5 o319 o12)
    (p6 o297)
    (p6 o308)
    (p6 o319)
    (p2 o97 o34)
    (p2 o199 o23)
    (p2 o210 o1)
    (p2 o221 o34)
    (p4 o97 o297)
    (p4 o199 o308)
    (p4 o210 o319)
    (p4 o221 o319)
    (p8 o221 o287)
    (p8 o199 o287)
    (p8 o210 o287)
    (p8 o97 o287))
 (:goal  (and 
   (p3 o34 o287))))
