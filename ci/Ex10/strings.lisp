(defun string-operations ()
  (format t "~%Enter first string: ")
  (let ((str1 (read-line)))
    
    (format t "~%Enter second string: ")
    (let ((str2 (read-line)))

      (format t "~%Length of first string: ~a~%" (length str1))

      (format t "Reversed first string: ~a~%"
              (coerce (reverse (coerce str1 'list)) 'string))

      (format t "Concatenation: ~a~%"
              (concatenate 'string str1 " " str2))

      (if (string= str1 str2)
          (format t "Strings are equal~%")
          (format t "Strings are NOT equal~%"))
    )))

(string-operations)
