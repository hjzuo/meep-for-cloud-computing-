(set-param! resolution 64)  ; pixels/µm
(define-param w 0.50)       ; waveguide width
(define-param h 0.22)       ; waveguide height
(define-param sc-y 2)       ; supercell width
(define-param sc-z 2)       ; supercell height

(set! geometry-lattice (make lattice (size no-size sc-y sc-z)))

(define-param nSi 3.45)
(define-param nSiO2 1.45)
(define Si (make dielectric (index nSi)))
(define SiO2 (make dielectric (index nSiO2)))
  
(set! geometry (list
    (make block (size infinity w h)
          (center 0 0 0) (material Si))
    (make block (size infinity infinity (* 0.5 (- sc-z h)))
          (center 0 0 (* 0.25 (+ sc-z h))) (material SiO2))))

(set-param! num-bands 4)

(define-param num-k 20)
(define-param k-min 0.1)
(define-param k-max 2.0)
(set! k-points (interpolate num-k (list (vector3 k-min) (vector3 k-max))))
(run display-yparities)
  
(define-param f-mode (/ 1.55))    ; frequency corresponding to 1.55 um
(define-param band-min 1)
(define-param band-max 1)
(define-param kdir (vector3 1 0 0))
(define-param tol 1e-6)
(define-param kmag-guess (* f-mode nSi))
(define-param kmag-min (* f-mode 0.1))
(define-param kmag-max (* f-mode 4))

(find-k ODD-Y f-mode band-min band-max kdir tol
        kmag-guess kmag-min kmag-max
        output-poynting-x display-group-velocities)