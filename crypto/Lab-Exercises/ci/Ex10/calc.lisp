(defun calculator ()
  (format t "Enter first number: ")
  (finish-output)
  (let ((a (read)))

    (format t "Enter second number: ")
    (finish-output)
    (let ((b (read)))

      (format t "Enter operator (+, -, *, /): ")
      (finish-output)
      (let ((op (read)))

        (cond
          ((eq op '+) (format t "~%Result: ~a~%" (+ a b)))
          ((eq op '-) (format t "~%Result: ~a~%" (- a b)))
          ((eq op '*) (format t "~%Result: ~a~%" (* a b)))
          ((eq op '/)
           (if (= b 0)
               (format t "~%Error: Division by zero!~%")
               (format t "~%Result: ~a~%" (/ a b))))
          (t (format t "~%Invalid operator!~%")))))))

;; Run the calculator
(calculator)
