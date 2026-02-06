;; cars=10, locations=10, out_folder=new/easy, instance_id=8, seed=49

(define (problem ferry-08)
 (:domain ferry)
 (:objects 
    car1 car2 car3 car4 car5 car6 car7 car8 car9 car10 - car
    loc1 loc2 loc3 loc4 loc5 loc6 loc7 loc8 loc9 loc10 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc2)
    (at car1 loc6)
    (at car2 loc7)
    (at car3 loc2)
    (at car4 loc6)
    (at car5 loc9)
    (at car6 loc9)
    (at car7 loc1)
    (at car8 loc1)
    (at car9 loc5)
    (at car10 loc3)
)
 (:goal  (and (at car1 loc9)
   (at car2 loc1)
   (at car3 loc10)
   (at car4 loc10)
   (at car5 loc4)
   (at car6 loc5)
   (at car7 loc7)
   (at car8 loc8)
   (at car9 loc1)
   (at car10 loc5))))
