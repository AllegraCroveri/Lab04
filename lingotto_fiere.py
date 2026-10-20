class Espositore():
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome

    def __eq__(self, other):
        if isinstance(other, Espositore):
            return self.codice == other.codice
        return False

    def __str__(self):
        return f"{self.codice}: {self.nome} {self.cognome}"

class Stand():
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = float(superficie)
        self.padiglione = int(padiglione)
        self.prezzo_base = float(prezzo_base)

        #quando viene creato lo stand all'inizio non appartiene a nessuno
        #successivamente conterrà l'oggetto espositore a cui lo stand verrà assegnato
        self.espositore=None #inizialmente è vuoto

    # chiedo se l'attributo self.espositore è uguale a None, ovvero che non è ancora occupato
    #se è True allora lo stand è libero
    def is_disponibile(self):
        return self.espositore is None

    def calcola_prezzo_finale(self):
        return self.prezzo_base

    def __eq__(self, other):
        return isinstance(other, Stand) and self.codice == other.codice

    def __lt__(self, other):
        return self.calcola_prezzo_finale() < other.calcola_prezzo_finale()

class StandStandard(Stand):
    def __str__(self):
        stato = f"Assegnato a {self.espositore.codice}" if self.espositore else "Disponibile"
        return f"{self.codice}: Standard | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo: {self.calcola_prezzo_finale():.2f}€ - {stato}"

class StandPreseExtra(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, prese_extra):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.prese_extra = int(prese_extra)

    def calcola_prezzo_finale(self):
        return self.prezzo_base * (1 + 0.07 * self.prese_extra)

    def __str__(self):
        stato = f"Assegnato a {self.espositore.codice}" if self.espositore else "Disponibile"
        return f"{self.codice}: Prese Extra ({self.prese_extra}) | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo: {self.calcola_prezzo_finale():.2f}€ - {stato}"

class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione = posizione

    def calcola_prezzo_finale(self):
        return self.prezzo_base * 1.30

    def __str__(self):
        stato = f"Assegnato a {self.espositore.codice}" if self.espositore else "Disponibile"
        return f"{self.codice}: Premium ({self.posizione}) | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo: {self.calcola_prezzo_finale():.2f}€ - {stato}"





class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        """Aggiungere setter e getter se necessari"""
        self.nome = nome
        # utilizzo dei dizionari perché si possono trovare velocemente gli oggetti con l'uso della chiave
        self.stand = {}  # dizionario che memorizza gli stand
        self.espositori = {}  # dizionario che memorizza gli espositori

    # get serve a leggere il valore dell'attributo
    def get_nome(self):
        return self.nome

    # set invece serve a modificare il valore di self.nome con nome_nuovo
    def set_nome(self, nuovo_nome):
        self.nome = nuovo_nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        try:
            with open(file_path, 'r', encoding="utf-8") as f:
                for riga in f:
                    riga = riga.strip()
                    if not riga:
                        continue  # salta le righe vuote

                    campi = riga.split(',')

                    # se ha 3 campi e non inizia con ST, allora è un espositore
                    if len(campi) == 3 and not campi[0].startswith('ST'):
                        codice, nome, cognome = campi
                        espositore = Espositore(codice.strip(), nome.strip(), cognome.strip())
                        self.espositori[espositore.codice] = espositore

                    # se ha 4 o più campi è uno stand
                    elif len(campi)>=4:
                        codice, superficie, padiglione, prezzo_base = campi[0], campi[1], campi[2], campi[3]

                        # è uno stand standard quando ci sono esattamente 4 campi
                        if len(campi)==4:
                            stand=StandStandard(codice, superficie, padiglione, prezzo_base)

                        # quando ha 5 campi può avere prese extra oppure essere uno stand premium
                        elif len(campi)==5:
                            extra=campi[4].strip()

                            #se extra è un numero allora sono prese elettriche extra
                            if extra.isdigit():
                                stand=StandPreseExtra(codice, superficie, padiglione, prezzo_base, int(extra))

                            # se extra non è un numero allora significa che è uno stand premium
                            else:
                                stand=StandPremium(codice, superficie, padiglione, prezzo_base, extra)

                        # se la riga ha più di 5 campi, il programma va avanti e non legge quella riga ma
                        # legge direttamente la riga dopo
                        else:
                            continue

                        # self.stand è il dizionario che abbiamo creato prima
                        # [stand.codice] è la chiave del dizionario, il codice univoco dello stand
                        self.stand[stand.codice] = stand
        #se c'è un errore nel file
        except FileNotFoundError:
            raise FileNotFoundError(f'il file {file_path} non è stato trovato!')


    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        #devo prima controllare che lo stand esista
        if codice_stand not in self.stand:
            raise ValueError(f'lo stand {codice_stand} non esiste')

        #e controllare se l'espositore esista
        if codice_espositore not in self.espositori:
            raise ValueError(f"l'espositore {codice_espositore} non esiste")

        stand = self.stand[codice_stand]
        espositore=self.espositori[codice_espositore]

        # prima di assegnare uno stand devo verificare che non sia già occupato
        if not stand.is_disponibile():
            raise ValueError(f'lo stand {codice_stand} è già assegnato ')
        #controllo adesso che l'espositore non abbia già un altro stand
        for s in self.stand.values():
            if s.espositore==espositore:
                raise ValueError(f"l'espositore {codice_espositore} ha già un altro stand" )

        #se passa tutti i controlli, assegno lol stand
        stand.espositore=espositore

    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        if not self.espositori:
            print('nessun espositore registrato nel sistema')

        for espositore in self.espositori.values():
            # Cerca se questo espositore ha uno stand assegnato
            stand_associato = None
            for s in self.stand.values():
                if s.espositore == espositore:
                    stand_associato = s
                    break

            # Stampa il risultato in base alla presenza o meno dello stand
            if stand_associato:
                print(f"• {espositore} — Stand assegnato: {stand_associato.codice}")
            else:
                print(f"• {espositore} — Nessuno stand assegnato")

    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(list(self.stand.values()))