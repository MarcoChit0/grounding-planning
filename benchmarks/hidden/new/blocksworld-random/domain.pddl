

(define (domain kyrtqawo0s0tejr2)

(:requirements :strips)

(:predicates (h9kzr3a33di9r53f ?x)
             (ot48xwrzpi0wcmm1 ?x)
             (kbz6u9989gjo77m5)
             (mrz9lj3txpbq71m9 ?x)
             (njfesrwvhrbvx7zy ?x ?y))

(:action r2vtydnwmn9g40hf
  :parameters (?ob)
  :precondition (and (h9kzr3a33di9r53f ?ob) (ot48xwrzpi0wcmm1 ?ob) (kbz6u9989gjo77m5))
  :effect (and (mrz9lj3txpbq71m9 ?ob) (not (h9kzr3a33di9r53f ?ob)) (not (ot48xwrzpi0wcmm1 ?ob)) 
               (not (kbz6u9989gjo77m5))))

(:action gt60s8k4vhzpo8tz
  :parameters  (?ob)
  :precondition (mrz9lj3txpbq71m9 ?ob)
  :effect (and (h9kzr3a33di9r53f ?ob) (kbz6u9989gjo77m5) (ot48xwrzpi0wcmm1 ?ob) 
               (not (mrz9lj3txpbq71m9 ?ob))))

(:action wmarsm3hjiujmszw
  :parameters  (?ob ?underob)
  :precondition (and (h9kzr3a33di9r53f ?underob) (mrz9lj3txpbq71m9 ?ob))
  :effect (and (kbz6u9989gjo77m5) (h9kzr3a33di9r53f ?ob) (njfesrwvhrbvx7zy ?ob ?underob)
               (not (h9kzr3a33di9r53f ?underob)) (not (mrz9lj3txpbq71m9 ?ob))))

(:action ak03qedve17wrpxv
  :parameters  (?ob ?underob)
  :precondition (and (njfesrwvhrbvx7zy ?ob ?underob) (h9kzr3a33di9r53f ?ob) (kbz6u9989gjo77m5))
  :effect (and (mrz9lj3txpbq71m9 ?ob) (h9kzr3a33di9r53f ?underob)
               (not (njfesrwvhrbvx7zy ?ob ?underob)) (not (h9kzr3a33di9r53f ?ob)) (not (kbz6u9989gjo77m5)))))
