import pandas as pd
from datetime import datetime
import json 
class uscite:
    
    def __init__(self):
        """crea un dizonario di vettori per l'oggetto usicte"""
        self.riga = {
            'istante':[] ,
            'id':[] ,
            'orario':[],
            'categoria':[] ,
            'spesa':[] ,
            'value':[],
            'modificata':[]  
                }
          
    #Reestituiscono il vettore per ogni chiave
    def getIstante(self):
        return self.riga['istante'] 
    def getID(self):
        return self.riga['id'] 
    def getOrario(self):
        return self.riga['orario']
    def getcategoria(self):
        return self.riga['categoria'] 
    def getspesa(self):
        return self.riga['spesa'] 
    def getvalue(self):
        return self.riga['value'] 
    def getmodifica(self):
        return self.riga['modificata']
    def getriga(self):
        return self.riga

    #non implementatato nel programma finale
    def modifica(self, indice:int, istante: datetime = None,orario: datetime = None, categoria: str = None, spesa: str = None,id:str = None, value: float = None):
        
        if istante is not None:
            self.riga['istante'][indice] = istante
        
        if orario is not None:
            self.riga['orario'][indice] = orario
        if categoria is not None:
            self.riga['categoria'][indice] = categoria
        if spesa is not None:
            self.riga['spesa'][indice] = spesa
        if id is not None:
            self.riga['id'][indice] = id
        if value is not None:
            self.riga['value'][indice] = value
            
        self.riga['modificata'][indice]=True
    

    def adduscita(self,categoria: str, spesa:str ,value:float,id:str = None):
        """
        Aggiunge una nuova transazione all'oggetto Uscite, registrando dettagli come categoria,
        spesa, valore e ID. Imposta automaticamente l'istante e l'orario della transazione al momento
        corrente e segna la transazione come non modificata.
        """
        data= datetime.now() 
        self.riga['istante'].append(data.strftime("%Y-%m-%d"))
        self.riga['id'].append(id)
        self.riga['orario'].append(data.strftime("%H:%M:%S"))
        self.riga['categoria'].append(categoria)
        self.riga['spesa'].append(spesa)
        self.riga['value'].append(value)
        self.riga['modificata'].append(False)

    def __str__(self):
        """
        Rappresentazione in stringa dell'oggetto Uscite per facilitare la visualizzazione
        dei dettagli delle uscite nel terminale.
        """
        return f'Istante:{self.riga['istante']},\n'\
                    f'Orario:{self.riga['orario']},\n'\
                        f'Categoria:{self.riga['categoria']},\n'\
                            f'Spesa:{self.riga['spesa']},\n'\
                                f'Costo:{self.riga['value']},\n'\
                                    f'ID:{self.riga['id']},\n'\
                                        f'Modifica:{self.riga['modificata']},\n'


    def saveUscite_json(agenda):
        """
        Salva le ultime uscite giornaliere in un file JSON.
        """
        df_esistente = pd.read_json('Json\\transaction.json')
        df = pd.DataFrame(agenda.getriga())              
        update= pd.concat([df_esistente,df.tail(1)],ignore_index=True)
        update.to_json('Json\\transaction.json', orient='records',indent=4)
        

    def removeuscita_json(indice: str):
        """
        Elimina una transazione specifica dal file JSON in base all'ID fornito.
        """
        try:
            with open('Json\\transaction.json', 'r') as file:
                data = json.load(file)

            new_data= [transazione for transazione in data if transazione['id'] != indice]

            with open('Json\\transaction.json', 'w') as file:
                json.dump(new_data, file, indent=4)
        except FileNotFoundError:
                print(f"Errore: il filenon è stato trovato.")
                
    def removeusicta(self,id_uscita:str):
        """
        Rimuove le uscite dalla lista interna dell'agenda giornaliera basandosi sull'identificatore di categoria.
        Utilizza pandas per manipolare i dati
        """
        df = pd.DataFrame(self.riga)
        for index,transazione in df.iterrows():
            if transazione['categoria']==id_uscita:
                indice = transazione['categoria'].index()
                self.riga['istante'].pop(indice)
                self.riga['id'].pop(indice)
                self.riga['orario'].pop(indice)
                self.riga['categoria'].pop(indice)
                self.riga['spesa'].pop(indice)
                self.riga['value'].pop(indice)
                self.riga['modificata'].pop(indice)
