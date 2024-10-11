from python_paypal_api.base import PaypalApiException
from python_paypal_api.api import Transactions
import logging 
import json
import pandas as pd 

dir_credenziali = 'Credenziali\\credenziali.json'

class Paypal:
    
    # Restituice le credenziali del file json per poter effettuare l'accesso a paypal'
    global dir_credenziali
    def credenziali_load(dir):
        with open(dir) as f:
            credeziali_data = json.load(f)
            client_id = credeziali_data['client_id']
            client_secret = credeziali_data['client_secret']
            client_mode = credeziali_data['client_mode']
        return (client_id,client_secret,client_mode)
    
    # Restituisce un APIrepsonse contenente i di delle transazionei  
    def _py_get_list_transactions(**kwargs):
        logger = logging.getLogger("test")
        logger.info("---------------------------")
        logger.info("Transactions > py_get_list_transactions({})".format(kwargs))
        logger.info("---------------------------")
        try: 
            response = Transactions(credentials=Paypal.credenziali_load(dir_credenziali)).get_list_transactions(**kwargs)
            #print(type(response))
            return response.payload

        except PaypalApiException as error:
            logger.error(error) 
            
    # Restituisce il dataframe contenente valori e id solo delle uscite
    def requestTransaction(date_start,date_end):
        
        response = Paypal._py_get_list_transactions(page_size = 20,start_date = date_start,end_date=date_end)
        #conversione dati da APIresponse a str
        Json_data = json.dumps(response)
        #conversione dati da str a dict
        dict_data = json.loads(Json_data)
        
        #'vet_transaction_detail'
        vet_transaction_detail = [transaction_detail for transaction_detail in dict_data['transaction_details']]
        
        #'vet_transaction_info'    
        vet_transaction_info = [transaction_info['transaction_info'] for transaction_info in vet_transaction_detail]
    
        #vet_transaction_id  
        vet_transaction_id = [transaction_id['transaction_id'] for transaction_id in vet_transaction_info]   

        #'vet_available_balance'       
        vet_available_balance = [available_balance['transaction_amount'] for available_balance in vet_transaction_info]
        
        #'vet_value_negativi'      
        vet_value = [float(value['value']) for value in vet_available_balance] #if float(value['value']) < 0
        
        df = pd.DataFrame({     
            'value': vet_value,
            'id': vet_transaction_id
        })
        
        df = df.drop(df[df['value'] > 0].index) #cancella tutte le righe dove il valolre è maggiore di 0
        df['value'] = df['value'].abs()
        return df
    
    # Slava i dati restituiti da "requestTransaction"  nel file value.json
    def salva_registro_controllo(df):
        registro_confronto = pd.DataFrame({
            'value': df['value'],
            'id': df['id']
        })
        
        registro_confronto.to_json('Json\\value.json', orient='records',indent=4)
        
        
    # Permette di contollare che all'interno del file value.json non siano 
    # prensti le stesse transazioni presenti su dataframe passato coem parametro "requestTransaction"
    def controllo(df):
        with open('Json\\value.json','r') as file_control:
            controllo = pd.read_json(file_control)
            for id in df['id']:
                if id not in controllo['id'].values:
                    indice_id = df[df['id'] == id].index[0]  # Trova l'indice dell'ID
                    valore_id_associato =df.loc[indice_id, 'id']
                    valore_value_associato = df.loc[indice_id, 'value']  # Accedi al valore associato usando loc[]
                    return valore_value_associato,valore_id_associato
                
    



                


