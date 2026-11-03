import flet as ft
from UI.view import View
from model.model import DepositoStrumenti

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: DepositoStrumenti):
        self._model = model
        self._view = view

    def get_nome(self):
        return self._model.nome

    def get_responsabile(self):
        return self._model.responsabile

    def set_responsabile(self, responsabile):
        self._model.responsabile = responsabile

    def conferma_responsabile(self, e):
        self._model.responsabile = self._view.input_responsabile.value
        self._view.txt_responsabile.value = f"Responsabile: {self._model.responsabile}"
        self._view.update()

    # Altre Funzioni Event Handler
    def mostra_strumenti(self, e):
        # 1. Pulisce la lista nell'interfaccia prima di inserire i nuovi dati
        self._view.lista_strumenti.controls.clear()

        # 2. Richiede la lista di oggetti Strumento al Modello
        strumenti = self._model.get_strumenti()

        # 3. Gestisce i possibili scenari (errore DB, DB vuoto, successo)
        if strumenti is None:
            self._view.show_alert("Errore di connessione al database!")
        elif len(strumenti) == 0:
            self._view.show_alert("Nessuno strumento presente nel deposito.")
        else:
            # Per ogni oggetto Strumento restituito, crea un elemento di testo per la View
            for strumento in strumenti:
                # Utilizzando str(strumento) Python richiama in automatico il metodo __str__
                # definito nella classe Strumento (file strumento.py)
                self._view.lista_strumenti.controls.append(ft.Text(str(strumento)))

        # 4. Comunica alla View di ridisegnare la pagina
        self._view.update()

    def cerca_strumento(self, e):
        # 1. Recupera il testo digitato dall'utente
        tipo_cercato = self._view.input_tipo_strumento.value

        # 2. Controllo validità: se il campo è vuoto o contiene solo spazi, blocca la ricerca
        if not tipo_cercato or tipo_cercato.strip() == "":
            self._view.show_alert("Inserisci un tipo di strumento da cercare!")
            return

        # 3. Pulisce la lista dei risultati di ricerca
        self._view.lista_strumenti_ricerca.controls.clear()

        # 4. Richiede al Modello di filtrare il database
        strumenti_filtrati = self._model.cerca_strumenti_per_tipo(tipo_cercato.strip())

        # 5. Gestisce i risultati
        if strumenti_filtrati is None:
            self._view.show_alert("Errore di connessione al database!")
        elif len(strumenti_filtrati) == 0:
            # Se non ci sono errori ma la query non produce risultati, mostra un messaggio inline
            self._view.lista_strumenti_ricerca.controls.append(
                ft.Text(f"Nessun risultato trovato per la ricerca: {tipo_cercato}", color=ft.colors.RED_400)
            )
        else:
            for strumento in strumenti_filtrati:
                self._view.lista_strumenti_ricerca.controls.append(ft.Text(str(strumento)))

        # 6. Aggiorna l'interfaccia
        self._view.update()