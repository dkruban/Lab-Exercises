(defun gcd-custom (a b)
  (if (= b 0)
      a
      (gcd-custom b (mod a b))))

(defun lcm-custom (a b)
  (/ (* a b) (gcd-custom a b)))

(defun main ()
  (format t "Enter first number: ")
  (finish-output)
  (let ((a (read)))
    
    (format t "Enter second number: ")
    (finish-output)
    (let ((b (read)))

      (format t "~%GCD: ~a~%" (gcd-custom a b))
      (format t "LCM: ~a~%" (lcm-custom a b)))))

(main)
