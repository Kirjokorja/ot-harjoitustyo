from entities.type_class import TypeClass


class RepositoryBase:
    """Luokka vastaa tietokantatoiminnoista.

        Attribuutit:
            _db (DatabaseInterface): tietokannan käyttöliittymäolio
    """

    def __init__(self, db):
        """Luo repo.

            Muuttujat:
                db (DatabaseInterface): tietokannan käyttöliittymäolio
        """
        self._db = db

    def _get_class_from_row(self, row):
        return TypeClass(t_id=row["id"], title=row["title"], value=row["value"]) if row else None

    def _get_classes_from_rows(self, rows):
        return list(map(self._get_class_from_row, rows))

    def get_classes(self, title):
        """Hakee luokan arvot.

            Muuttujat:
                title (str): luokan nimi

            Palauttaa:
                list: lista luokkaolioita        
        """
        sql = """SELECT id, title, value FROM Classes
            WHERE title = ?
            ORDER BY id"""
        result = self._db.query(sql, [title])
        return self._get_classes_from_rows(result)
