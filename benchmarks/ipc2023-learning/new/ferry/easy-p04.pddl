;; cars=5, locations=7, out_folder=new/easy, instance_id=4, seed=45

(define (problem ferry-04)
 (:domain ferry)
 (:objects 
    car1 car2 car3 car4 car5 - car
    loc1 loc2 loc3 loc4 loc5 loc6 loc7 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc3)
    (at car1 loc4)
    (at car2 loc4)
    (at car3 loc3)
    (at car4 loc1)
    (at car5 loc3)
)
 (:goal  (and (at car1 loc3)
   (at car2 loc1)
   (at car3 loc1)
   (at car4 loc5)
   (at car5 loc1))))
