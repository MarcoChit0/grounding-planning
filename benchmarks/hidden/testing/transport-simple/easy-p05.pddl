

(define (problem pr5)
 (:domain d1)
 (:objects 
    o305 o316 o327 - t5
    o111 o217 o228 - t3
    o12 o23 o34 o45 o56 o67 - t2
    o1 o2 o4 - t4
    )
 (:init (p2 o305 o4)
    (p2 o316 o4)
    (p2 o327 o2)
    (p3 o1 o2)
    (p3 o2 o4)
    (p1 o111 o45)
    (p1 o217 o23)
    (p1 o228 o67)
    (p1 o305 o45)
    (p1 o316 o45)
    (p1 o327 o67)
    (p5 o67 o23)
    (p5 o34 o12)
    (p5 o67 o12)
    (p5 o56 o45)
    (p5 o45 o56)
    (p5 o23 o67)
    (p5 o56 o34)
    (p5 o12 o67)
    (p5 o12 o34)
    (p5 o34 o56)
    (p5 o56 o67)
    (p5 o67 o56)
    )
 (:goal  (and 
    (p1 o111 o23)
    (p1 o217 o56)
    (p1 o228 o12))))
