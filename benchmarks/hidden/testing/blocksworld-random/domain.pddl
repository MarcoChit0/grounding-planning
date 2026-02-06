

(define (domain swmivibhgrceuh3n)

(:requirements :strips :typing)

(:predicates (jyl8ny94brpqqzdx ?x)
             (wf0ooz14rzkewsma ?x)
             (ni2znqqdangh4jl5)
             (l29rs36ubgq6gqzr ?x)
             (rwpi4bggss3phkx8 ?x ?y))

(:action p8lsi1lqtlye888i
  :parameters (?ob)
  :precondition (and (jyl8ny94brpqqzdx ?ob) (wf0ooz14rzkewsma ?ob) (ni2znqqdangh4jl5))
  :effect (and (l29rs36ubgq6gqzr ?ob) (not (jyl8ny94brpqqzdx ?ob)) (not (wf0ooz14rzkewsma ?ob))
               (not (ni2znqqdangh4jl5))))

(:action m59d3113vlll922s
  :parameters  (?ob)
  :precondition (l29rs36ubgq6gqzr ?ob)
  :effect (and (jyl8ny94brpqqzdx ?ob) (ni2znqqdangh4jl5) (wf0ooz14rzkewsma ?ob)
               (not (l29rs36ubgq6gqzr ?ob))))

(:action y2cy4vvz5leki7vy
  :parameters  (?ob ?underob)
  :precondition (and (jyl8ny94brpqqzdx ?underob) (l29rs36ubgq6gqzr ?ob))
  :effect (and (ni2znqqdangh4jl5) (jyl8ny94brpqqzdx ?ob) (rwpi4bggss3phkx8 ?ob ?underob)
               (not (jyl8ny94brpqqzdx ?underob)) (not (l29rs36ubgq6gqzr ?ob))))

(:action l559hose8ab7a122
  :parameters  (?ob ?underob)
  :precondition (and (rwpi4bggss3phkx8 ?ob ?underob) (jyl8ny94brpqqzdx ?ob) (ni2znqqdangh4jl5))
  :effect (and (l29rs36ubgq6gqzr ?ob) (jyl8ny94brpqqzdx ?underob)
               (not (rwpi4bggss3phkx8 ?ob ?underob)) (not (jyl8ny94brpqqzdx ?ob)) (not (ni2znqqdangh4jl5)))))
