




(define (domain k1fkkmrn89p4pepm)
  (:requirements :typing)
  (:types
        s4xjfwlpq4q1xy41 n5bxf8vi67eqt22b znywa791ukahjfs9 - object
        liipnyfanb3z4u2w pwp8z5l0cwl7b4mn - znywa791ukahjfs9
  )

  (:predicates
     (bom2kp8l8rvrbkzs ?l1 ?l2 - n5bxf8vi67eqt22b)
     (qhmiyva3rfsh9osg ?x - znywa791ukahjfs9 ?v - n5bxf8vi67eqt22b)
     (oldstwtdsk4mg7p3 ?x - pwp8z5l0cwl7b4mn ?v - liipnyfanb3z4u2w)
     (v73d7s4mfxfxwa3v ?v - liipnyfanb3z4u2w ?s1 - s4xjfwlpq4q1xy41)
     (ptnnxw5u6yxezc4k ?s1 ?s2 - s4xjfwlpq4q1xy41)
  )

  (:action fxd0oxzpgyyudg05
    :parameters (?v - liipnyfanb3z4u2w ?l1 ?l2 - n5bxf8vi67eqt22b)
    :precondition (and
        (qhmiyva3rfsh9osg ?v ?l1)
        (bom2kp8l8rvrbkzs ?l1 ?l2)
      )
    :effect (and
        (not (qhmiyva3rfsh9osg ?v ?l1))
        (qhmiyva3rfsh9osg ?v ?l2)
      )
  )

 (:action r08ak0m6dkj3w0p3
    :parameters (?v - liipnyfanb3z4u2w ?l - n5bxf8vi67eqt22b ?p - pwp8z5l0cwl7b4mn ?s1 ?s2 - s4xjfwlpq4q1xy41)
    :precondition (and
        (qhmiyva3rfsh9osg ?v ?l)
        (qhmiyva3rfsh9osg ?p ?l)
        (ptnnxw5u6yxezc4k ?s1 ?s2)
        (v73d7s4mfxfxwa3v ?v ?s2)
      )
    :effect (and
        (not (qhmiyva3rfsh9osg ?p ?l))
        (oldstwtdsk4mg7p3 ?p ?v)
        (v73d7s4mfxfxwa3v ?v ?s1)
        (not (v73d7s4mfxfxwa3v ?v ?s2))
      )
  )

  (:action lzpf0ob1jjgbq170
    :parameters (?v - liipnyfanb3z4u2w ?l - n5bxf8vi67eqt22b ?p - pwp8z5l0cwl7b4mn ?s1 ?s2 - s4xjfwlpq4q1xy41)
    :precondition (and
        (qhmiyva3rfsh9osg ?v ?l)
        (oldstwtdsk4mg7p3 ?p ?v)
        (ptnnxw5u6yxezc4k ?s1 ?s2)
        (v73d7s4mfxfxwa3v ?v ?s1)
      )
    :effect (and
        (not (oldstwtdsk4mg7p3 ?p ?v))
        (qhmiyva3rfsh9osg ?p ?l)
        (v73d7s4mfxfxwa3v ?v ?s2)
        (not (v73d7s4mfxfxwa3v ?v ?s1))
      )
  )

)