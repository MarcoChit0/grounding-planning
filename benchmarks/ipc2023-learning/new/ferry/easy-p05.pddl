;; cars=7, locations=7, out_folder=new/easy, instance_id=5, seed=46

(define (problem ferry-05)
 (:domain ferry)
 (:objects 
    car1 car2 car3 car4 car5 car6 car7 - car
    loc1 loc2 loc3 loc4 loc5 loc6 loc7 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc1)
    (at car1 loc4)
    (at car2 loc1)
    (at car3 loc5)
    (at car4 loc5)
    (at car5 loc7)
    (at car6 loc2)
    (at car7 loc6)
)
 (:goal  (and (at car1 loc6)
   (at car2 loc3)
   (at car3 loc6)
   (at car4 loc6)
   (at car5 loc1)
   (at car6 loc1)
   (at car7 loc1))))
