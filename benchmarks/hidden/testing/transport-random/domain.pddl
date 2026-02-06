




(define (domain hbrpoig8f1cbfno6)
  (:requirements :typing)
  (:types
        b9m80o2rak1vrjnv gfygwwqc38hyf9sx mecosfogyr3xkxwn - object
        rek8pk3yr9oudocu zrenun5z3jqip98q - mecosfogyr3xkxwn
  )

  (:predicates
     (hxtpdpff5e8ii49k ?l1 ?l2 - gfygwwqc38hyf9sx)
     (dgdzvgpmm82i1lr3 ?x - mecosfogyr3xkxwn ?v - gfygwwqc38hyf9sx)
     (zhpcf07uqnupqzit ?x - zrenun5z3jqip98q ?v - rek8pk3yr9oudocu)
     (sk28t7a9tgiqhg9j ?v - rek8pk3yr9oudocu ?s1 - b9m80o2rak1vrjnv)
     (iqk2919ahej8cx9j ?s1 ?s2 - b9m80o2rak1vrjnv)
  )

  (:action wtoobmzvrerw6z8v
    :parameters (?v - rek8pk3yr9oudocu ?l1 ?l2 - gfygwwqc38hyf9sx)
    :precondition (and
        (dgdzvgpmm82i1lr3 ?v ?l1)
        (hxtpdpff5e8ii49k ?l1 ?l2)
      )
    :effect (and
        (not (dgdzvgpmm82i1lr3 ?v ?l1))
        (dgdzvgpmm82i1lr3 ?v ?l2)
      )
  )

 (:action bhqlqcg1wu16hymq
    :parameters (?v - rek8pk3yr9oudocu ?l - gfygwwqc38hyf9sx ?p - zrenun5z3jqip98q ?s1 ?s2 - b9m80o2rak1vrjnv)
    :precondition (and
        (dgdzvgpmm82i1lr3 ?v ?l)
        (dgdzvgpmm82i1lr3 ?p ?l)
        (iqk2919ahej8cx9j ?s1 ?s2)
        (sk28t7a9tgiqhg9j ?v ?s2)
      )
    :effect (and
        (not (dgdzvgpmm82i1lr3 ?p ?l))
        (zhpcf07uqnupqzit ?p ?v)
        (sk28t7a9tgiqhg9j ?v ?s1)
        (not (sk28t7a9tgiqhg9j ?v ?s2))
      )
  )

  (:action omjbcp4e30my5zpj
    :parameters (?v - rek8pk3yr9oudocu ?l - gfygwwqc38hyf9sx ?p - zrenun5z3jqip98q ?s1 ?s2 - b9m80o2rak1vrjnv)
    :precondition (and
        (dgdzvgpmm82i1lr3 ?v ?l)
        (zhpcf07uqnupqzit ?p ?v)
        (iqk2919ahej8cx9j ?s1 ?s2)
        (sk28t7a9tgiqhg9j ?v ?s1)
      )
    :effect (and
        (not (zhpcf07uqnupqzit ?p ?v))
        (dgdzvgpmm82i1lr3 ?p ?l)
        (sk28t7a9tgiqhg9j ?v ?s2)
        (not (sk28t7a9tgiqhg9j ?v ?s1))
      )
  )

)