# -*- coding: utf-8 -*-
from __future__ import division
from numpy import (maximum as max_, logical_not as not_, absolute as abs_, minimum as min_, select, where)
from openfisca_france.model.base import *  # noqa analysis:ignore

class paris_nam_eligibilite_personnelle(Variable):
    value_type = bool
    label = u"Éligibité des personnes Paris NAM"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        return individu.famille('parisien', period) * (
            + individu('paris_personnes_agees', period)
            + individu('paris_personnes_handicap', period)
            )


class paris_nam_eligibilite_financiere(Variable):
    value_type = bool
    label = u"Éligibilité financière au Paris NAM"
    entity = FoyerFiscal
    definition_period = MONTH

    def formula(foyer_fiscal, period):
        eligibilite_personnelle = foyer_fiscal.members('paris_nam_eligibilite_personnelle', period.last_year, options = [ADD])
        renouvelement = foyer_fiscal.sum(eligibilite_personnelle)
        return (
            + (-foyer_fiscal('irpp', period.n_2) <= 2028)
            + renouvelement * (-foyer_fiscal('irpp', period.n_2) <= 2430)
            )


class paris_nam(Variable):
    value_type = bool
    label = u"Éligibilité au Paris NAM"
    entity = Individu
    definition_period = MONTH

    def formula(individu, period):
        eligibilite_personnelle = individu('paris_nam_eligibilite_personnelle', period)
        eligibilite_financiere = individu.foyer_fiscal('paris_nam_eligibilite_financiere', period)
        return eligibilite_personnelle * eligibilite_financiere
