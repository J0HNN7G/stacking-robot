(define (domain blocks-world)
    (:requirements :adl)

    (:types table block)

    (:predicates
        (On ?x - block ?y - object)
        (Clear ?b - object)
        (Up ?b - block)
    )

    (:constants Table - table)

    (:action PICKUP
        :parameters (?b - block ?x - object)
        :precondition (and (On ?b ?x) (Clear ?b) (not (= ?b ?x)))
        :effect (and (Up ?b) (Clear ?x) (not (On ?b ?x)))
    )

    (:action DROP
        :parameters (?b -block ?y - block)
        :precondition (and (Up ?b) (Clear ?b) (Clear ?y) (not (= ?b ?y)))
        :effect (and (On ?b ?y) (not (Clear ?y)))
    )

    (:action DROP-ON-TABLE
        :parameters (?b - block)
        :precondition (and (Up ?b))
        :effect (and (On ?b Table))
    )
)