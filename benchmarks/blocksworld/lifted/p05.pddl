
(define (problem BW-rand-2)
(:domain blocksworld)
(:objects b1 b2 )
(:init
(holding b2)
(on-table b1)
(clear b1)
)
(:goal
(and
(on b1 b2))
)
)