(set-param! resolution 20)    ; pixels/µm

(define-param h 0.22)         ; waveguide height
(define-param w 0.5)          ; waveguide width

(define-param a 1.0)          ; Bragg grating periodicity/lattice parameter
(define-param d 0.5)          ; Bragg grating thickness
(define-param N 5)            ; number of grating periods
(set! N (+ N 1))

(define nSi 3.45)
(define Si (make medium (index nSi)))

(define nSiO2 1.45)
(define SiO2 (make medium (index nSiO2)))

(define-param sxy 16)
(define-param sz 4)
(set! geometry-lattice (make lattice (size sxy sxy sz)))

; rings of Bragg grating
(set! geometry (append geometry
       (map (lambda (n)
          (list
	      (make cylinder (material Si) (center 0 0 0) (radius (* n a)) (height h))
	      (make cylinder (material air) (center 0 0 0) (radius (- (* n a) d)) (height h))))
	   (arith-sequence N -1 N))))
(set! geometry (apply append geometry))

; remove left half of Bragg grating rings to form semi circle
(set! geometry (append geometry (list
	 (make block (material air) (center (* -0.5 (* N a)) 0 0) (size (* N a) (* 2 N a) h))
	 (make cylinder (material Si) (center 0 0 0) (radius (- a d)) (height h)))))

; angle sides of Bragg grating

; rotation angle of sides relative to Y axis (degrees)
(define-param rot-theta 0)
(set! rot-theta (deg->rad (- rot-theta)))

(define pvec (vector3 0 (* 0.5 w) 0))
(define cvec (vector3 (* -0.5 N a) (+ (* 0.5 N a) (* 0.5 w)) 0))
(define rvec (vector3- cvec pvec))
(define rrvec (rotate-vector3 (vector3 0 0 1) rot-theta rvec))

(set! geometry (append geometry (list (make block
			(material air)
			(center (vector3+ pvec rrvec)) (size (* N a) (* N a) h) 
			(e1 (rotate-vector3 (vector3 0 0 1) rot-theta (vector3 1 0 0)))
			(e2 (rotate-vector3 (vector3 0 0 1) rot-theta (vector3 0 1 0)))
			(e3 (vector3 0 0 1))))))

(set! pvec (vector3 0 (* -0.5 w) 0))
(set! cvec (vector3 (* -0.5 N a) (- (+ (* 0.5 N a) (* 0.5 w))) 0))
(set! rvec (vector3- cvec pvec))
(set! rrvec (rotate-vector3 (vector3 0 0 1) (- rot-theta) rvec))

(set! geometry (append geometry (list (make block
			(material air)
			(center (vector3+ pvec rrvec)) (size (* N a) (* N a) h) 
			(e1 (rotate-vector3 (vector3 0 0 1) (- rot-theta) (vector3 1 0 0)))
			(e2 (rotate-vector3 (vector3 0 0 1) (- rot-theta) (vector3 0 1 0)))
			(e3 (vector3 0 0 1))))))

; input waveguide
(set! geometry (append geometry (list
		 (make block (material air) (center (* -0.25 sxy) (+ (* 0.5 w) (* 0.5 a)) 0) (size (* 0.5 sxy) a h))
		 (make block (material air) (center (* -0.25 sxy) (- (+ (* 0.5 w) (* 0.5 a))) 0) (size (* 0.5 sxy) a h))
		 (make block (material Si) (center (* -0.25 sxy) 0 0) (size (* 0.5 sxy) w h)))))

; substrate
(set! geometry (append geometry (list (make block
			(material SiO2)
			(center 0 0 (+ (* -0.5 sz) (* 0.25 (- sz h))))
			(size infinity infinity (* 0.5 (- sz h)))))))

; surround the entire computational cell with PML
(define-param dpml 1.0)
(set! pml-layers (list (make pml (thickness dpml))))

; mode frequency
(define-param fcen (/ 1.55))

(set! sources (list (make eigenmode-source
		      (src (make gaussian-src (frequency fcen) (fwidth (* 0.2 fcen))))
		      (component Ey)
		      (size 0 (- sxy (* 2 dpml)) (- sz (* 2 dpml)))
		      (center (+ (* -0.5 sxy) dpml) 0 0)
		      (eig-match-freq? true)
		      (eig-parity ODD-Y)
		      (eig-kpoint (vector3 1.5 0 0))
		      (eig-resolution 32))))

(set! symmetries (list (make mirror-sym (direction Y) (phase -1))))
 

(define nearfield
  (add-near2far fcen 0 1
		(make near2far-region (center 0 0 (- (* 0.5 sz) dpml)) (size (- sxy (* 2 dpml)) (- sxy (* 2 dpml)) 0))))


(run-sources+ (stop-when-fields-decayed 50 Ey (vector3 0 0 0) 1e-6))



; far-field radius is 1000 wavelengths from the device center
(define-param r (* 1000 (/ fcen))) 

; number of far-field points to compute on the semicircle in XZ
(define-param npts 100)

; print the far-field data for each field component at each point on the semicircle
(map (lambda (n)
       (let ((ff (get-farfield nearfield (vector3 (* r (cos (* pi (/ n npts)))) 0 (* r (sin (* pi (/ n npts))))))))
	 (print "farfield:, " (number->string n) ", " (number->string (* pi (/ n npts))))
	 (map (lambda (m)
		(print ", " (number->string (list-ref ff m))))
	      (arith-sequence 0 1 6))
	 (print "\n")))
         (arith-sequence 0 1 npts))
