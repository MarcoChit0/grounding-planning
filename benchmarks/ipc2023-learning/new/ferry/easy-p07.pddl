;; cars=9, locations=9, out_folder=new/easy, instance_id=7, seed=48

(define (problem ferry-07)
 (:domain ferry)
 (:objects 
    car1 car2 car3 car4 car5 car6 car7 car8 car9 - car
    loc1 loc2 loc3 loc4 loc5 loc6 loc7 loc8 loc9 - location
 )
 (:init 
    (empty-ferry)
    (at-ferry loc9)
    (at car1 loc6)
    (at car2 loc3)
    (at car3 loc9)
    (at car4 loc9)
    (at car5 loc5)
    (at car6 loc9)
    (at car7 loc4)
    (at car8 loc7)
    (at car9 loc3)
)
 (:goal  (and (at car1 loc3)
   (at car2 loc2)
   (at car3 loc8)
   (at car4 loc4)
   (at car5 loc4)
   (at car6 loc3)
   (at car7 loc9)
   (at car8 loc4)
   (at car9 loc1))))
