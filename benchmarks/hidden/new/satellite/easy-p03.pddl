

(define (problem pr3)
 (:domain d1)
 (:objects 
    o297 o308 o319 o330 - d1
    o97 o199 o210 o221 o232 - t2
    o287 - t3
    o1 o12 o23 o34 - t1
    )
 (:init 
    (p5 o297 o34)
    (p5 o308 o1)
    (p5 o319 o12)
    (p5 o330 o34)
    (p6 o297)
    (p6 o308)
    (p6 o319)
    (p6 o330)
    (p2 o97 o12)
    (p2 o199 o23)
    (p2 o210 o1)
    (p2 o221 o12)
    (p2 o232 o1)
    (p4 o97 o308)
    (p4 o199 o319)
    (p4 o210 o330)
    (p4 o221 o297)
    (p4 o232 o319)
    (p8 o97 o287)
    (p8 o199 o287)
    (p8 o210 o287)
    (p8 o232 o287)
    (p8 o221 o287))
 (:goal  (and (p5 o308 o23)
   (p5 o330 o1)
   (p3 o12 o287)
   (p3 o34 o287)
   (p3 o23 o287))))
