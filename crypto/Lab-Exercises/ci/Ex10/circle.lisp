(defun area-circle (r)
  (* pi r r))

(defun circumference (r)
  (* 2 pi r))

(defun perimeter-rectangle (l w)
  (* 2 (+ l w)))

(defun main ()
  ;; Circle calculations
  (format t "Enter radius of circle: ")
  (finish-output)
  (let ((r (read)))

    (format t "~%Area of circle: ~f~%" (area-circle r))
    (format t "Circumference of circle: ~f~%" (circumference r)))

  ;; Rectangle calculations
  (format t "~%Enter length of rectangle: ")
  (finish-output)
  (let ((l (read)))

    (format t "Enter width of rectangle: ")
    (finish-output)
    (let ((w (read)))

      (format t "~%Perimeter of rectangle: ~a~%"
              (perimeter-rectangle l w)))))

(main)
