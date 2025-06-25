import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        if self._view.dd_min_ch.value is None:
            self._view.create_alert("Selezionare un valore per Chromosoma min")
            return
        else:
            cmin = int(self._view.dd_min_ch.value)

        if self._view.dd_max_ch.value is None:
            self._view.create_alert("Selezionare un valore per Chromosoma max")
            return
        else:
            cmax = int(self._view.dd_max_ch.value)

        if cmin > cmax:
            self._view.create_alert("Attenzione: deve essere Chromosoma min <= Chromosoma max")
            return

        # crea grafo e stampa info del grafo
        self._model.buildGraph(cmin, cmax)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Creato grafo con {self._model.getNumNodes()} nodi"
                                                       f" e {self._model.getNumEdges()} archi"))

        sorted_nodes = self._model.get_node_max_uscenti()
        n_nodi = min(len(sorted_nodes), 5)
        self._view.txt_result1.controls.append(ft.Text(f"\nI {n_nodi} nodi col maggior numero di archi uscenti sono:"))
        for i in range(n_nodi):
            self._view.txt_result1.controls.append(ft.Text(f"{sorted_nodes[i][0]} | "
                                                           f"num. archi uscenti: {sorted_nodes[i][1]}  | "
                                                           f"peso tot.: {sorted_nodes[i][2]}"))

        self._view.btn_dettagli.disabled = False
        self._view.btn_path.disabled = False
        self._view.update_page()






    def handle_dettagli(self, e):
        loc = self._view.dd_localization.value
        nodes = self._model.get_nodes_location(loc)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"\n Ci sono {len(nodes)} geni con location {loc}:"))
        for n in nodes:
            self._view.txt_result1.controls.append(ft.Text(f"{n}"))
        self._view.update_page()


    def handle_path(self, e):
        self._view.txt_result2.controls.clear()
        cammino_ottimo, costo_ottimo = self._model.trova_cammino()
        self._view.txt_result2.controls.append(ft.Text(f"Trovato un cammino ottimo di lunghezza {len(cammino_ottimo)}"))
        self._view.txt_result2.controls.append(ft.Text(f"Il costo del cammino ottimo è {costo_ottimo}"))
        self._view.txt_result2.controls.append(ft.Text(f"Le fermate del cammino sono:"))
        for n in cammino_ottimo:
            self._view.txt_result2.controls.append(ft.Text(f"{n}"))
        self._view.update_page()

    def fill_dd_localization(self):
        values = self._model.get_localizations()
        self._view.dd_localization.options = list(map(lambda x: ft.dropdown.Option(key=x, text=x), values))






    def fillDDCromosomaMin(self):
        for c in self._model.getCromosoma():
            self._view.dd_min_ch.options.append(ft.dropdown.Option(c))
        self._view.update_page()

    def fillDDCromosomaMax(self):
        for c in self._model.getCromosoma():
            self._view.dd_max_ch.options.append(ft.dropdown.Option(c))
        self._view.update_page()