import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph() # grafo diretto e pesato
        self._nodes = []
        self._edges = []
        self._idMapGene = {}

        self._cammino_ottimo = []
        self._peso_ottimo = 0
        self._localization_map = {}

    def getCromosoma(self):
        return DAO.getCromosoma()

    def buildGraph(self, cmin, cmax):
        self._graph.clear()
        self._nodes = DAO.getNodi(cmin, cmax)
        self._graph.add_nodes_from(self._nodes)
        self._idMapGene = {}
        for n in self._nodes:
            self._idMapGene[(n.GeneID, n.Function)] = n

        self.addAllArchi(cmin, cmax)

    def addAllArchi(self, cmin, cmax):
        self._edges = DAO.getArchi(cmin, cmax, self._idMapGene)
        for a in self._edges:
            self._graph.add_edge(a[0], a[1], weight=a[2])

    def getNumNodes(self):
        return self._graph.number_of_nodes()

    def getNumEdges(self):
        return self._graph.number_of_edges()

    def get_node_max_uscenti(self):
        '''I 5 nodi col maggiore numero di archi uscenti col numero di archi uscenti ed il peso complessivo di
        questi archi (la somma dei loro pesi). I nodi devono essere stampati in ordine decrescente per
        numero di archi uscenti.'''
        sorted_nodes = sorted(self._graph.nodes(), key=lambda n: self._graph.out_degree(n), reverse=True)
        result = []
        for i in range(min(len(sorted_nodes), 5)):
            peso_tot = 0.0
            for e in self._graph.out_edges(sorted_nodes[i], data=True):
                peso_tot += float(e[2].get("weight"))
            result.append((sorted_nodes[i], self._graph.out_degree(sorted_nodes[i]), peso_tot))
        return result







    #SECONDA PARTE

    def get_localizations(self):
        return DAO.get_all_localizations()

    def get_connesse(self):
        return nx.weakly_connected_components(self._graph)

    def get_nodes_location(self, loc):
        res = []
        nodes = list(self._graph.nodes())
        for n in nodes:
            if self._localization_map[n.GeneID] == loc:
                res.append(n)
        return res

    def trova_cammino(self):
        self._cammino_ottimo = []
        self._peso_ottimo = 0
        for n in self._graph.nodes():
            nuovi_successori = self._calcola_successori_ammissibili(n, [n])
            self._ricorsione([n], nuovi_successori)
        return self._cammino_ottimo, self._peso_ottimo

    def _ricorsione(self, parziale, successori):
        '''A partire dal grafo definito al punto 1, si vuole implementare una procedura ricorsiva che identifichi il
            cammino più lungo che minimizza la somma dei pesi del percorso, e con le seguenti caratteristiche:
            I. Un nodo può essere attraversato una sola volta.
            II. Gli archi possono essere attraversati solo nella loro direzione di percorrenza
            III. Nel cammino, non ci possono essere due geni consecutivi con lo stesso valore del campo Essential
            IV. Si possono attraversare solo archi di peso crescente (ovvero ogni nuovo arco percorso deve avere
            peso >= del precedente). '''
        # caso terminale
        if len(successori) == 0:
            if len(parziale) > len(self._cammino_ottimo):
                self._cammino_ottimo = copy.deepcopy(parziale)
                self._peso_ottimo = self._peso_cammino(self._cammino_ottimo)
            elif len(parziale) == len(self._cammino_ottimo) and self._peso_cammino(parziale) < self._peso_ottimo:
                self._cammino_ottimo = copy.deepcopy(parziale)
                self._peso_ottimo = self._peso_cammino(self._cammino_ottimo)
        # caso ricorsivo
        else:
            for n in successori:
                parziale.append(n)
                nuovi_successori = self._calcola_successori_ammissibili(n, parziale)
                self._ricorsione(parziale, nuovi_successori)
                parziale.pop()

    def _calcola_successori_ammissibili(self, n, parziale):
        last_essential = parziale[-1].Essential
        if len(parziale) == 1:
            nuovi_successori = [i for i in list(self._graph.successors(n)) if
                                i not in parziale and i.Essential != last_essential]
        else:
            last_peso = self._graph.get_edge_data(parziale[-2], parziale[-1])["weight"]
            nuovi_successori = [i for i in list(self._graph.successors(n)) if
                                i not in parziale and i.Essential != last_essential
                                and self._graph.get_edge_data(parziale[-1], i)["weight"] >= last_peso]
        return nuovi_successori

    def _peso_cammino(self, cammino):
        peso = 0
        if len(cammino) == 1:
            return peso
        for i in range(0, len(cammino) - 1):
            peso += self._graph.get_edge_data(cammino[i], cammino[i + 1])["weight"]
        return peso