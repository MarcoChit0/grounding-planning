;; blocks=6, out_folder=new/easy, instance_id=2, seed=43

(define (problem blocksworld-02)
 (:domain blocksworld)
 (:objects b1 b2 b3 b4 b5 b6 - object)
 (:init 
    (arm-empty)
    (clear b6)
    (on b6 b5)
    (on b5 b4)
    (on b4 b2)
    (on b2 b3)
    (on b3 b1)
    (on-table b1))
 (:goal  (and 
    (clear b6)
    (on b6 b2)
    (on b2 b3)
    (on b3 b4)
    (on b4 b5)
    (on b5 b1)
    (on-table b1))))
