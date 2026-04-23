
class ServiceBase:
    """Palveluiden emoluokka.

        Attribuutit:
            _repository (Repository): 
                tietokantatoiminnoista vastaava olio
            _exceptions: virheluokat
    """

    def __init__(self, repository, exceptions):
        """Alusta palvelut.

            Muuttujat:
                repository (RepositoryBase): 
                    tietokantatoiminnoista vastaava olio
                exceptions: virheluokat
        """
        self._repository = repository
        self._exceptions = exceptions

    def get_exceptions(self):
        """Antaa palvelun virheilmoitusluokat.

            Palauttaa:
                _exceptions: palvelun virheilmoitusluokat
        """
        return self._exceptions
