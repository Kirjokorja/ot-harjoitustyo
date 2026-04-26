
class ServiceBase:
    """Palveluiden emoluokka.

        Attributes:
            _repository (Repository): 
                tietokantatoiminnoista vastaava olio
            _exceptions: virheluokat
    """

    def __init__(self, repository, exceptions):
        """Alusta palvelut.

            Args:
                repository (RepositoryBase): 
                    tietokantatoiminnoista vastaava olio
                exceptions: virheluokat
        """
        self._repository = repository
        self._exceptions = exceptions

    def get_exceptions(self):
        """Antaa palvelun virheilmoitusluokat.

            Returns:
                _exceptions: palvelun virheilmoitusluokat
        """
        return self._exceptions
