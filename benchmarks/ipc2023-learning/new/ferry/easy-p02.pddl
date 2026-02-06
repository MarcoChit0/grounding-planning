;; cars=3, locations=5, out_folder=new/easy, instance_id=2, seed=43

(define (problem ferry-02)
 (:domain ferry)
 (:objects 
    car1 car2 car3 - car
    loc1 loc2 loc3 loc4 loc5 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc1)
    (at car1 loc3)
    (at car2 loc2)
    (at car3 loc4)
)
 (:goal  (and (at car1 loc4)
   (at car2 loc1)
   (at car3 loc5))))
