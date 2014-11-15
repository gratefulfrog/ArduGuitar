;;; parse.lisp
;;; parsing coil-node expressions
;;; let's say that the connections data structure is a list of lists:
;;; (list-out+ list-out- list-of-lists-of-internal-connections)
;;; ((out+) (out-) ((internal connection) (internal connection) ...))
;;; then we need to get the pair-wise connections of the form:
;;; ((A+  out+) (a-  b+) (... etc)
;;; thus we need some high level functions to define the circuit
;;; and a function to get all the necessary connections

;;; Define a Parallel connection
;;; (pp coil1 &optional coil2 coil3 coil4)
;;; paralllel connection of all the coils given

;;; Define a Series connection
;;; (ss coil1 coil2 &optional coil3 coil4)
;;; series connection of all the coils given

;;; both the above functions return a connection list which is the argument
;;; needed to get the pair-wise list of connected terminals

;;; Get the pair-wise connected terminals
;;; (connection-list (ss 'c1 'c2 (pp 'c3 'c4)))
;;; -> (("C1+" "out+") ("C3-" "out-") ("C4-" "out-") ("C3+" "C4+") ("C2-" "C3+")
;;;     ("C2-" "C4+") ("C1-" "C2+"))

;;; all the others are helper functions

(defun pp (n1 &optional n2 n3 n4)
  "top level PARALLEL connection call, dispatches as needed."
   (p n1 (p n2 (p n3 (p n4)))))
    
(defun ss (n1 n2 &optional n3 n4)
  "top level SERIES connection call, dispatches as needed."
  (let ((res (s n1 n2)))
    (if n3
	(let ((ress (s res n3)))
	  (if n4
	      (let ((resss (s ress n4)))
		resss)
	    ress))
      res)))

(defun p (n1 &optional n2)
  "parallel connect nd1 nd2 means:
   out+ = the out+ of nd1 and nd2 connected together
   out- = the out- of nd1 and nd2 connected together
   whatever previous internal connections there were are maintained"
  (list (connect (n+ n1) 
		 (n+ n2))
	(connect (n- n1) 
		 (n- n2))
	(append (n* n1) 
		(n* n2))))

(defun s (n1 n2)
  "series connect nd1 nd2 means:
   out+ = the out+ of nd1 
   out- = the out- of nd2 
   internals = add a connection from out- of nd1 to out+ of nd2 to
   whatever previous internal connections there were."
  (list (n+ n1)
	(n- n2)
	(cons (connect (n- n1) 
		       (n+ n2))
	      (append (n* n1) 
		      (n* n2)))))

(defun connect (a b)
  "just syntactic sugar ;-)"
  (append a b))

(defun n (nd ind)
  "this little helper function takes a node and an index and returns the 
   element then is required:
   0: out+
   1: out-
   2: internals"
  (and (not (null nd))
       
  (let ((rep (if (atom nd)
		 ;; if we have an atom, then we have a base coil:
		 ;; we  need the name with a + or - concatenanted to it.
		 ;; coils have no internals.
		 (list (list (concatenate 'string 
					  (symbol-name nd) "+"))
		       (list (concatenate 'string 
					  (symbol-name nd) "-"))
		       ())
	       ;; otherwise we use the nd provided in argument.
	       nd)))
    ;; return the nth car of the rep variable as determined above.
    (nth ind rep))))

(defun n+ (nd)
  "return the out+ of the node"
  (n nd 0))

(defun n- (nd)
  "return the out- of the node"
  (n nd 1))

(defun n* (nd)
  "return the internals of the node"
  (n nd 2))

(defun connection-list (c-lis)
  (append (mapcar #'(lambda(elt) 
		      (list elt "out+"))
		  (car c-lis))
	  (mapcar #'(lambda(elt) 
		      (list elt "out-"))
		  (cadr c-lis))
	  (mapcan #'map-connect
		  (caddr c-lis))))

(defun map-connect (lis)
  (map-connect-helper lis ()))

(defun map-connect-helper (lis res)
  (cond
   ((null (cdr lis)) res)
   (t (map-connect-helper (cdr lis)
			  (append (mapcar #'(lambda (elt)
					      (list (car lis)
						    elt))
					  (cdr lis))
				  res)))))

#|
some **GOOD** results:

* (load "parse.lisp")

T
* (p 'a 'b)

(("A+" "B+") ("A-" "B-") NIL)
* (s 'a 'b)

(("A+") ("B-") (("A-" "B+")))
* (s (p 'a 'b)(p 'c 'd))

(("A+" "B+") ("C-" "D-") (("A-" "B-" "C+" "D+")))
* (s 'a (p (s 'b 'c) 'd))

(("A+") ("C-" "D-") (("A-" "B+" "D+") ("B-" "C+")))
* (p (s 'a (p 'b 'c)) 'd)

(("A+" "D+") ("B-" "C-" "D-") (("A-" "B+" "C+")))
* (dribble)

* (load "parse.lisp")

T
* (connection-list (p 'a 'b))

(("A+" "out+") ("B+" "out+") ("A-" "out-") ("B-" "out-"))
* (connection-list (s 'a 'b))

(("A+" "out+") ("B-" "out-") ("A-" "B+"))
* (connection-list (s (p 'a 'b)(p 'c 'd)))

(("A+" "out+") ("B+" "out+") ("C-" "out-") ("D-" "out-") ("C+" "D+")
 ("B-" "C+") ("B-" "D+") ("A-" "B-") ("A-" "C+") ("A-" "D+"))
* (connection-list  (s 'a (p (s 'b 'c) 'd)))

(("A+" "out+") ("C-" "out-") ("D-" "out-") ("B+" "D+") ("A-" "B+") ("A-" "D+")
 ("B-" "C+"))
* (connection-list  (p (s 'a (p 'b 'c)) 'd))

(("A+" "out+") ("D+" "out+") ("B-" "out-") ("C-" "out-") ("D-" "out-")
 ("B+" "C+") ("A-" "B+") ("A-" "C+"))
* (dribble)

* (load "parse.lisp")

T
* (ss 'a 'b 'c)

(("A+") ("C-") (("B-" "C+") ("A-" "B+")))
* (pp 'a)

(("A+") ("A-") NIL)
* (pp 'a 'b 'c 'd)

(("A+" "B+" "C+" "D+") ("A-" "B-" "C-" "D-") NIL)
* (ss 'a 'b (pp 'c 'd))

(("A+") ("C-" "D-") (("B-" "C+" "D+") ("A-" "B+")))
* (connection-list (ss 'a 'b (pp 'c 'd)))

(("A+" "out+") ("C-" "out-") ("D-" "out-") ("C+" "D+") ("B-" "C+") ("B-" "D+")
 ("A-" "B+"))
* (connection-list  (pp (ss 'a (p 'b 'c)) 'd))

(("A+" "out+") ("D+" "out+") ("B-" "out-") ("C-" "out-") ("D-" "out-")
 ("B+" "C+") ("A-" "B+") ("A-" "C+"))
* (dribble)


|#
