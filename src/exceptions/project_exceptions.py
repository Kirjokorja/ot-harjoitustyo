class FailedToCreateProject(Exception):
    """Luokka käsittelee ilmoituksia poikkeustilanteessa, 
        jossa hanketta ei kyetty luomaan.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ProjectHasNoTitle(Exception):
    """Luokka käsittelee ilmoituksia poikkeustilanteessa, 
        jossa hankkeelle ei ole annettu nimeä.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ProjectHasNoType(Exception):
    """Luokka käsittelee ilmoituksia poikkeustilanteessa, 
        jossa hankkeelle ei ole annettu luokkaa.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ProjectHasNoOwner(Exception):
    """Luokka käsittelee ilmoituksia poikkeustilanteessa, 
        jossa hankkeelle ei ole annettu haltijaa.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
