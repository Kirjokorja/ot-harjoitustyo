
def ceildiv(a, b):
    """Laskee jakolaskun ja pyöristää vastauksen ylöspäin.
        Tämä on toteutettu alaspäin pyöristävällä jakolaskulla, 
        josta on otettu käänteinen tulos.
        Metodi math.ceil voi antaa vääriä tuloksia, ks. 
        https://stackoverflow.com/questions/14822184/is-there-a-ceiling-equivalent-of-operator-in-python.

        Args:
            a (int): jaettava
            b (int): jakaja

        Returns:
            int: jakolaskun tulos
    """
    return -(a//-b)
