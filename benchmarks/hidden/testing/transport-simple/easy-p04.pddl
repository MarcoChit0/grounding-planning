

(define (problem pr4)
 (:domain d1)
 (:objects 
    o305 o316 o327 - t5
    o111 o217 - t3
    o12 o23 o34 o45 o56 o67 - t2
    o1 o2 o4 - t4
    )
 (:init (p2 o305 o2)
    (p2 o316 o2)
    (p2 o327 o4)
    (p3 o1 o2)
    (p3 o2 o4)
    (p1 o111 o45)
    (p1 o217 o45)
    (p1 o305 o23)
    (p1 o316 o23)
    (p1 o327 o45)
    (p5 o67 o23)
    (p5 o12 o23)
    (p5 o34 o45)
    (p5 o23 o12)
    (p5 o12 o56)
    (p5 o45 o34)
    (p5 o56 o45)
    (p5 o56 o12)
    (p5 o45 o56)
    (p5 o23 o67)
    (p5 o56 o67)
    (p5 o67 o56)
    (p5 o34 o67)
    (p5 o67 o34)
    (p5 o23 o34)
    (p5 o34 o23)
    (p5 o12 o67)
    (p5 o67 o12)
    (p5 o23 o56)
    (p5 o56 o23)
    )
 (:goal  (and 
    (p1 o111 o23)
    (p1 o217 o56))))
