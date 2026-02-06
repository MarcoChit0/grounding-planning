;; cars=4, locations=6, out_folder=new/easy, instance_id=3, seed=44

(define (problem ferry-03)
 (:domain ferry)
 (:objects 
    car1 car2 car3 car4 - car
    loc1 loc2 loc3 loc4 loc5 loc6 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc4)
    (at car1 loc5)
    (at car2 loc5)
    (at car3 loc6)
    (at car4 loc1)
)
 (:goal  (and (at car1 loc2)
   (at car2 loc4)
   (at car3 loc2)
   (at car4 loc4))))
