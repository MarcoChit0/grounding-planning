;; vehicles=3, packages=3, locations=6, max_capacity=2, out_folder=new/easy, instance_id=3, seed=44

(define (problem transport-03)
 (:domain transport)
 (:objects 
    v1 v2 v3 - vehicle
    p1 p2 p3 - package
    l1 l2 l3 l4 l5 l6 - location
    c0 c1 c2 - size
    )
 (:init (capacity v1 c2)
    (capacity v2 c1)
    (capacity v3 c1)
    (capacity-predecessor c0 c1)
    (capacity-predecessor c1 c2)
    (at p1 l4)
    (at p2 l2)
    (at p3 l3)
    (at v1 l1)
    (at v2 l2)
    (at v3 l1)
    (road l2 l4)
    (road l5 l4)
    (road l4 l6)
    (road l6 l4)
    (road l4 l2)
    (road l1 l4)
    (road l2 l3)
    (road l4 l5)
    (road l3 l2)
    (road l4 l1)
    (road l1 l6)
    (road l6 l1)
    )
 (:goal  (and 
    (at p1 l1)
    (at p2 l6)
    (at p3 l1))))
