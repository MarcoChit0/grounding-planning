;; rows=3, columns=13, robots=12, out_folder=testing/new, instance_id=23, seed=1939

(define (problem floortile-23)
 (:domain floortile)
 (:objects 
    tile_0_1
    tile_0_2
    tile_0_3
    tile_0_4
    tile_0_5
    tile_0_6
    tile_0_7
    tile_0_8
    tile_0_9
    tile_0_10
    tile_0_11
    tile_0_12
    tile_0_13
    tile_1_1
    tile_1_2
    tile_1_3
    tile_1_4
    tile_1_5
    tile_1_6
    tile_1_7
    tile_1_8
    tile_1_9
    tile_1_10
    tile_1_11
    tile_1_12
    tile_1_13
    tile_2_1
    tile_2_2
    tile_2_3
    tile_2_4
    tile_2_5
    tile_2_6
    tile_2_7
    tile_2_8
    tile_2_9
    tile_2_10
    tile_2_11
    tile_2_12
    tile_2_13
    tile_3_1
    tile_3_2
    tile_3_3
    tile_3_4
    tile_3_5
    tile_3_6
    tile_3_7
    tile_3_8
    tile_3_9
    tile_3_10
    tile_3_11
    tile_3_12
    tile_3_13 - tile
    robot1
    robot2
    robot3
    robot4
    robot5
    robot6
    robot7
    robot8
    robot9
    robot10
    robot11
    robot12 - robot
    white black - color
)
 (:init 
    (robot-at robot1 tile_1_12)
    (robot-has robot1 black)
    (robot-at robot2 tile_1_11)
    (robot-has robot2 white)
    (robot-at robot3 tile_2_7)
    (robot-has robot3 white)
    (robot-at robot4 tile_0_3)
    (robot-has robot4 black)
    (robot-at robot5 tile_0_13)
    (robot-has robot5 black)
    (robot-at robot6 tile_2_2)
    (robot-has robot6 white)
    (robot-at robot7 tile_3_8)
    (robot-has robot7 white)
    (robot-at robot8 tile_3_1)
    (robot-has robot8 white)
    (robot-at robot9 tile_2_9)
    (robot-has robot9 white)
    (robot-at robot10 tile_2_6)
    (robot-has robot10 black)
    (robot-at robot11 tile_1_5)
    (robot-has robot11 white)
    (robot-at robot12 tile_3_4)
    (robot-has robot12 white)
    (available-color white)
    (available-color black)
    (clear tile_0_1)
    (clear tile_0_2)
    (clear tile_0_4)
    (clear tile_0_5)
    (clear tile_0_6)
    (clear tile_0_7)
    (clear tile_0_8)
    (clear tile_0_9)
    (clear tile_0_10)
    (clear tile_0_11)
    (clear tile_0_12)
    (clear tile_1_1)
    (clear tile_1_2)
    (clear tile_1_3)
    (clear tile_1_4)
    (clear tile_1_6)
    (clear tile_1_7)
    (clear tile_1_8)
    (clear tile_1_9)
    (clear tile_1_10)
    (clear tile_1_13)
    (clear tile_2_1)
    (clear tile_2_3)
    (clear tile_2_4)
    (clear tile_2_5)
    (clear tile_2_8)
    (clear tile_2_10)
    (clear tile_2_11)
    (clear tile_2_12)
    (clear tile_2_13)
    (clear tile_3_2)
    (clear tile_3_3)
    (clear tile_3_5)
    (clear tile_3_6)
    (clear tile_3_7)
    (clear tile_3_9)
    (clear tile_3_10)
    (clear tile_3_11)
    (clear tile_3_12)
    (clear tile_3_13)
    (up tile_1_1 tile_0_1 )
    (up tile_1_2 tile_0_2 )
    (up tile_1_3 tile_0_3 )
    (up tile_1_4 tile_0_4 )
    (up tile_1_5 tile_0_5 )
    (up tile_1_6 tile_0_6 )
    (up tile_1_7 tile_0_7 )
    (up tile_1_8 tile_0_8 )
    (up tile_1_9 tile_0_9 )
    (up tile_1_10 tile_0_10 )
    (up tile_1_11 tile_0_11 )
    (up tile_1_12 tile_0_12 )
    (up tile_1_13 tile_0_13 )
    (up tile_2_1 tile_1_1 )
    (up tile_2_2 tile_1_2 )
    (up tile_2_3 tile_1_3 )
    (up tile_2_4 tile_1_4 )
    (up tile_2_5 tile_1_5 )
    (up tile_2_6 tile_1_6 )
    (up tile_2_7 tile_1_7 )
    (up tile_2_8 tile_1_8 )
    (up tile_2_9 tile_1_9 )
    (up tile_2_10 tile_1_10 )
    (up tile_2_11 tile_1_11 )
    (up tile_2_12 tile_1_12 )
    (up tile_2_13 tile_1_13 )
    (up tile_3_1 tile_2_1 )
    (up tile_3_2 tile_2_2 )
    (up tile_3_3 tile_2_3 )
    (up tile_3_4 tile_2_4 )
    (up tile_3_5 tile_2_5 )
    (up tile_3_6 tile_2_6 )
    (up tile_3_7 tile_2_7 )
    (up tile_3_8 tile_2_8 )
    (up tile_3_9 tile_2_9 )
    (up tile_3_10 tile_2_10 )
    (up tile_3_11 tile_2_11 )
    (up tile_3_12 tile_2_12 )
    (up tile_3_13 tile_2_13 )
    (down tile_0_1 tile_1_1 )
    (down tile_0_2 tile_1_2 )
    (down tile_0_3 tile_1_3 )
    (down tile_0_4 tile_1_4 )
    (down tile_0_5 tile_1_5 )
    (down tile_0_6 tile_1_6 )
    (down tile_0_7 tile_1_7 )
    (down tile_0_8 tile_1_8 )
    (down tile_0_9 tile_1_9 )
    (down tile_0_10 tile_1_10 )
    (down tile_0_11 tile_1_11 )
    (down tile_0_12 tile_1_12 )
    (down tile_0_13 tile_1_13 )
    (down tile_1_1 tile_2_1 )
    (down tile_1_2 tile_2_2 )
    (down tile_1_3 tile_2_3 )
    (down tile_1_4 tile_2_4 )
    (down tile_1_5 tile_2_5 )
    (down tile_1_6 tile_2_6 )
    (down tile_1_7 tile_2_7 )
    (down tile_1_8 tile_2_8 )
    (down tile_1_9 tile_2_9 )
    (down tile_1_10 tile_2_10 )
    (down tile_1_11 tile_2_11 )
    (down tile_1_12 tile_2_12 )
    (down tile_1_13 tile_2_13 )
    (down tile_2_1 tile_3_1 )
    (down tile_2_2 tile_3_2 )
    (down tile_2_3 tile_3_3 )
    (down tile_2_4 tile_3_4 )
    (down tile_2_5 tile_3_5 )
    (down tile_2_6 tile_3_6 )
    (down tile_2_7 tile_3_7 )
    (down tile_2_8 tile_3_8 )
    (down tile_2_9 tile_3_9 )
    (down tile_2_10 tile_3_10 )
    (down tile_2_11 tile_3_11 )
    (down tile_2_12 tile_3_12 )
    (down tile_2_13 tile_3_13 )
    (left tile_0_1 tile_0_2 )
    (left tile_0_2 tile_0_3 )
    (left tile_0_3 tile_0_4 )
    (left tile_0_4 tile_0_5 )
    (left tile_0_5 tile_0_6 )
    (left tile_0_6 tile_0_7 )
    (left tile_0_7 tile_0_8 )
    (left tile_0_8 tile_0_9 )
    (left tile_0_9 tile_0_10 )
    (left tile_0_10 tile_0_11 )
    (left tile_0_11 tile_0_12 )
    (left tile_0_12 tile_0_13 )
    (left tile_1_1 tile_1_2 )
    (left tile_1_2 tile_1_3 )
    (left tile_1_3 tile_1_4 )
    (left tile_1_4 tile_1_5 )
    (left tile_1_5 tile_1_6 )
    (left tile_1_6 tile_1_7 )
    (left tile_1_7 tile_1_8 )
    (left tile_1_8 tile_1_9 )
    (left tile_1_9 tile_1_10 )
    (left tile_1_10 tile_1_11 )
    (left tile_1_11 tile_1_12 )
    (left tile_1_12 tile_1_13 )
    (left tile_2_1 tile_2_2 )
    (left tile_2_2 tile_2_3 )
    (left tile_2_3 tile_2_4 )
    (left tile_2_4 tile_2_5 )
    (left tile_2_5 tile_2_6 )
    (left tile_2_6 tile_2_7 )
    (left tile_2_7 tile_2_8 )
    (left tile_2_8 tile_2_9 )
    (left tile_2_9 tile_2_10 )
    (left tile_2_10 tile_2_11 )
    (left tile_2_11 tile_2_12 )
    (left tile_2_12 tile_2_13 )
    (left tile_3_1 tile_3_2 )
    (left tile_3_2 tile_3_3 )
    (left tile_3_3 tile_3_4 )
    (left tile_3_4 tile_3_5 )
    (left tile_3_5 tile_3_6 )
    (left tile_3_6 tile_3_7 )
    (left tile_3_7 tile_3_8 )
    (left tile_3_8 tile_3_9 )
    (left tile_3_9 tile_3_10 )
    (left tile_3_10 tile_3_11 )
    (left tile_3_11 tile_3_12 )
    (left tile_3_12 tile_3_13 )
    (right tile_0_2 tile_0_1 )
    (right tile_0_3 tile_0_2 )
    (right tile_0_4 tile_0_3 )
    (right tile_0_5 tile_0_4 )
    (right tile_0_6 tile_0_5 )
    (right tile_0_7 tile_0_6 )
    (right tile_0_8 tile_0_7 )
    (right tile_0_9 tile_0_8 )
    (right tile_0_10 tile_0_9 )
    (right tile_0_11 tile_0_10 )
    (right tile_0_12 tile_0_11 )
    (right tile_0_13 tile_0_12 )
    (right tile_1_2 tile_1_1 )
    (right tile_1_3 tile_1_2 )
    (right tile_1_4 tile_1_3 )
    (right tile_1_5 tile_1_4 )
    (right tile_1_6 tile_1_5 )
    (right tile_1_7 tile_1_6 )
    (right tile_1_8 tile_1_7 )
    (right tile_1_9 tile_1_8 )
    (right tile_1_10 tile_1_9 )
    (right tile_1_11 tile_1_10 )
    (right tile_1_12 tile_1_11 )
    (right tile_1_13 tile_1_12 )
    (right tile_2_2 tile_2_1 )
    (right tile_2_3 tile_2_2 )
    (right tile_2_4 tile_2_3 )
    (right tile_2_5 tile_2_4 )
    (right tile_2_6 tile_2_5 )
    (right tile_2_7 tile_2_6 )
    (right tile_2_8 tile_2_7 )
    (right tile_2_9 tile_2_8 )
    (right tile_2_10 tile_2_9 )
    (right tile_2_11 tile_2_10 )
    (right tile_2_12 tile_2_11 )
    (right tile_2_13 tile_2_12 )
    (right tile_3_2 tile_3_1 )
    (right tile_3_3 tile_3_2 )
    (right tile_3_4 tile_3_3 )
    (right tile_3_5 tile_3_4 )
    (right tile_3_6 tile_3_5 )
    (right tile_3_7 tile_3_6 )
    (right tile_3_8 tile_3_7 )
    (right tile_3_9 tile_3_8 )
    (right tile_3_10 tile_3_9 )
    (right tile_3_11 tile_3_10 )
    (right tile_3_12 tile_3_11 )
    (right tile_3_13 tile_3_12 ))
 (:goal  (and 
    (painted tile_1_1 white)
    (painted tile_1_2 black)
    (painted tile_1_3 white)
    (painted tile_1_4 black)
    (painted tile_1_5 white)
    (painted tile_1_6 black)
    (painted tile_1_7 white)
    (painted tile_1_8 black)
    (painted tile_1_9 white)
    (painted tile_1_10 black)
    (painted tile_1_11 white)
    (painted tile_1_12 black)
    (painted tile_1_13 white)
    (painted tile_2_1 black)
    (painted tile_2_2 white)
    (painted tile_2_3 black)
    (painted tile_2_4 white)
    (painted tile_2_5 black)
    (painted tile_2_6 white)
    (painted tile_2_7 black)
    (painted tile_2_8 white)
    (painted tile_2_9 black)
    (painted tile_2_10 white)
    (painted tile_2_11 black)
    (painted tile_2_12 white)
    (painted tile_2_13 black)
    (painted tile_3_1 white)
    (painted tile_3_2 black)
    (painted tile_3_3 white)
    (painted tile_3_4 black)
    (painted tile_3_5 white)
    (painted tile_3_6 black)
    (painted tile_3_7 white)
    (painted tile_3_8 black)
    (painted tile_3_9 white)
    (painted tile_3_10 black)
    (painted tile_3_11 white)
    (painted tile_3_12 black)
    (painted tile_3_13 white))))
