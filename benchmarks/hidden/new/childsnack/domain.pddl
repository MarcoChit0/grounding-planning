



















(define (domain d1)
(:requirements :typing :equality)
(:types t2 t1 t3 t5 t6 t4)
(:constants o853 - t4)

(:predicates (p3 ?v1 - t1)
	     (p4 ?v2 - t3)
     	     (p5 ?v6 - t5)
     	     (p6 ?v1 - t1)
       	     (p7 ?v2 - t3)
      	     (p11 ?v6 - t5 ?v7 - t6)
       	     (p8 ?v6 - t5)
	     (p1 ?v2 - t2)
     	     (p9 ?v2 - t2)
	     (p12 ?v2 - t2)
	     (p13 ?v2 - t2 ?v3 - t4)
             (p2 ?v7 - t6 ?v3 - t4)
	     (p10 ?v6 - t5)
  )

(:action a2
	 :parameters (?v6 - t5 ?v1 - t1 ?v2 - t3)
	 :precondition (and (p3 ?v1)
			    (p4 ?v2)
			    (p6 ?v1)
			    (p7 ?v2)
			    (p10 ?v6))
	 :effect (and
		   (not (p3 ?v1))
		   (not (p4 ?v2))
		   (p5 ?v6)
		   (p8 ?v6)
                   (not (p10 ?v6))
		   ))


(:action a1
	 :parameters (?v6 - t5 ?v1 - t1 ?v2 - t3)
	 :precondition (and (p3 ?v1)
			    (p4 ?v2)
                            (p10 ?v6)
			    )
	 :effect (and
		   (not (p3 ?v1))
		   (not (p4 ?v2))
		   (p5 ?v6)
                   (not (p10 ?v6))
		   ))


(:action a4
	 :parameters (?v6 - t5 ?v7 - t6)
	 :precondition (and  (p5 ?v6)
			     (p2 ?v7 o853))
	 :effect (and
		   (not (p5 ?v6))
		   (p11 ?v6 ?v7)))


(:action a6
 	:parameters (?v6 - t5 ?v2 - t2 ?v7 - t6 ?v3 - t4)
	:precondition (and
		       (p1 ?v2)
		       (p11 ?v6 ?v7)
		       (p13 ?v2 ?v3)
		       (p8 ?v6)
                       (p2 ?v7 ?v3)
		       )
	:effect (and (not (p11 ?v6 ?v7))
		     (p12 ?v2)))

(:action a5
	:parameters (?v6 - t5 ?v2 - t2 ?v7 - t6 ?v3 - t4)
	:precondition (and (p9 ?v2)
	                   (p13 ?v2 ?v3)
			   (p11 ?v6 ?v7)
			   (p2 ?v7 ?v3))
	:effect (and (not (p11 ?v6 ?v7))
		     (p12 ?v2)))

(:action a3
	 :parameters (?v7 - t6 ?v4 ?v5 - t4)
	 :precondition (and (p2 ?v7 ?v4))
	 :effect (and (not (p2 ?v7 ?v4))
		      (p2 ?v7 ?v5)))


)