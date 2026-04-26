class Project:
    """Luokka kuvaa yksittäistä hanketta.

    Attributes:
            p_id (int): hankkeen tunnusluku ja pääavain tietokannassa
            title (str): hankkeen nimi
            p_type (TypeClass): hankkeen luokka
            description (str): hankkeen kuvaus
            owner (User): hankkeen omistava käyttäjä
    """

    def __init__(self, params):
        """Alusta hanke.

        Args:
            params (dict): hajautustaulu, joka sisältää luokan jäsenien arvot
                keys:
                    ip_id (int): hankkeen tunnusluku ja pääavain tietokannassa
                    title (str): hankkeen nimi
                    type (TypeClass): hankkeen luokka
                    description (str): hankkeen kuvaus
                    owner (User): hankkeen omistava käyttäjä
        """
        self.p_id = params["id"]
        self.title = params["title"]
        self.p_type = params["type"]
        self.description = params["description"]
        self.owner = params["owner"]
