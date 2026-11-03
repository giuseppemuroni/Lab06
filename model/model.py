from database.DB_connect import get_connection
from model.strumento import Strumento
from model.prestito import Prestito

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        self._nome = nome
        self._responsabile = responsabile

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, responsabile):
        self._responsabile = responsabile

    def get_strumenti(self) -> list[Strumento] | None:
        """
            Funzione che legge tutti gli strumenti nel database
            :return: una lista con tutti gli strumenti presenti oppure None
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = "SELECT * FROM strumento"
            cursor.execute(query)

            risultato = []
            for row in cursor.fetchall():
                # Assumendo che il costruttore di Strumento rispetti l'ordine delle colonne SQL:
                # codice, tipo, marca, anno_acquisto, valore, disponibile
                strumento = Strumento(row[0], row[1], row[2], row[3], row[4], row[5])
                risultato.append(strumento)

            cursor.close()
            conn.close()
            return risultato

        except Exception as e:
            print(f"Errore DB in get_strumenti: {e}")
            return None

    def cerca_strumenti_per_tipo(self, tipo) -> list[Strumento] | None:
        """
            Funzione che recupera una lista con tutti gli strumenti presenti nel database di un certo tipo
            :param tipo: il tipo dello strumento (es. "Chitarra")
            :return: una lista con tutti gli strumenti del tipo indicato oppure None
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Utilizzo del parametro %s per evitare SQL Injection
            query = "SELECT * FROM strumento WHERE tipo = %s"
            cursor.execute(query, (tipo,))

            risultato = []
            for row in cursor.fetchall():
                strumento = Strumento(row[0], row[1], row[2], row[3], row[4], row[5])
                risultato.append(strumento)

            cursor.close()
            conn.close()
            return risultato

        except Exception as e:
            print(f"Errore DB in cerca_strumenti_per_tipo: {e}")
            return None
