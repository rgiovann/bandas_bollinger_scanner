import pandas as pd
import sys
import QuantMT5ConstantesGlobais as CTE
from pathlib import Path
pd.options.mode.chained_assignment = None  # default='warn'
#import pandas as pd

############################################################################################
############################################################################################
#  AUTOR: GIOVANNI L. ROZZA
#  DATA: 07.04.2020
#  ESSE SCRIPT LE OS ARQUIVOS DO TRYD E GERA 
#  O BANCO DE DADOS PARA USAR NOS SCRIPT DE LONG-SHORT
#  SÓ DEVE SER EXECUTADO *** UMA VEZ ***  OU QUANDO O BANCO
#  DE DADOS DO PYTHON PERDER O SINCRONISMO (NÃO FOR ATUALIZADO TODO DIA)
#  -- 18.04.2020 -- CONSIDERA MAX E MIN TAMBÉM
#  -- 09.09.2020 -- ATUALIZADO PARA MIGRAR BANCO DE DADOS EM QQ CONTEXTO
#  -- 28.12.2020 -- MIGRAÇÃO PARA NOVO NOTEBOOK (PATH DIFERENTE)
############################################################################################
############################################################################################
 
############################################################################################
# CONFIGURACOES PARA MIGRACAO UNICA DO TRYD PARA
# DATABASE PYTHON
# NAO ESQUECER DE CONFIGURAR QUAIS
# ATIVOS MIGRAR NO LISTA_B3 em QuantMT5ConstantesGlobais.py
############################################################################################

print(" ---------- Versão do Script de Migração Única: V. - 1.1 28.12.2020 ----------")

# define se quer todas as linahs ou um numero especifico
NUMERO_DE_LINHAS = 530
bLeTodasLinhas = True

# colunas padrão
colunas_Tryd_Basica = ['Data','Fechamento','Máxima','Mínima']     # as colunas essenciais são DATA, FECHAMENTO, MAXIMA E MINIMA

# caso leitura de colunas adicionais
colunas_Tryd_Extra  = ['Data','Hora','Fechamento','Máxima','Mínima'] 
lColunasExtras = False
cwd = str(Path.cwd())
for ativo in CTE.LISTA_B3:
    
    # diario
    str_path_tryd = cwd + "\\Database_Tryd\\"+ ativo + "_tryd.csv" 

    
    #diario
    str_path_py  = cwd + "\\Database_Python\\"+ ativo + "_python.csv"

    try:
        precos = pd.read_csv(str_path_tryd,encoding = "ISO-8859-1")

    except ( IOError, NameError,PermissionError,FileNotFoundError) as e:
        print("#################################################################################################")
        print("                ### ATENÇÃO ### ocorreu um problema na leitura arquivo DB Tryd ativo: " + ativo )
        print(e)
        print("#################################################################################################")
        sys.exit()
 
        
    ##############################################
    # processa só preco de fechamento, 
    # troca virgula por ponto, transforma em 
    # numerico
    ##############################################
    # define quantas linhas ler
    if bLeTodasLinhas:
        nr_linhas = len(precos.index)
    else:
        nr_linhas = NUMERO_DE_LINHAS
    
    # define se le as colunas padrão ou extras
    if not lColunasExtras:
        qColunas = colunas_Tryd_Basica
    else:
        qColunas = colunas_Tryd_Extra
        
    df_csv_python = precos[qColunas].head(nr_linhas)
    
    # tira acentos do titulo para as colunas maxima, minima (essenciais)
    df_csv_python.rename(columns={'Máxima':'Maxima','Mínima':'Minima' },inplace=True)
        
    # virgula vira ponto (numeracao USA)
    for idx in df_csv_python.index: 
        for str_coluna in df_csv_python.columns:
            str_tmp = df_csv_python[str_coluna][idx]
            # no caso do mini indice tem ponto 100.203,000 - remover o ponto
            df_csv_python[str_coluna][idx] = str_tmp.replace('.','')
            
            # aqui troca a virgula pelo ponto.
            str_tmp = df_csv_python[str_coluna][idx]
            df_csv_python[str_coluna][idx] = str_tmp.replace(',','.')
        
 
        
   ############################# TESTE  ############################
   
        # df_csv_python_reversed = df_csv_python.iloc[::-1]
        # print(df_csv_python_reversed['Fechamento'][0])
        # print(df_csv_python['Fechamento'][0])
       
        # list_A = df_csv_python['Fechamento'].tolist()
        # list_A_rev = df_csv_python_reversed['Fechamento'].tolist()
        
        # for idx, (_, value) in enumerate(df_csv_python_reversed.iterrows()):
        #     #print(df_csv_python_reversed['Fechamento'][idx])
        #     print( df_csv_python_reversed['Fechamento'][ df_csv_python_reversed.index.get_loc(idx) ])
        #     list(df_csv_python_reversed.index)
 
   ############################# FIM TESTE  ############################
    
    ##############################################
    # salva panda serie em dataframe
    # e salve em arquivo csv
    ##############################################
     
    # migração para o BD Python...
    try:
        df_csv_python.to_csv(str_path_py, index=False)

    except ( IOError, NameError,PermissionError,FileNotFoundError) as e:
        print("#################################################################################################")
        print("         ### ATENÇÃO ### ocorreu um problema nas escrita do arquivo DB Python ativo: " + ativo )
        print(e)
        print("#################################################################################################")
        # SÓ PRINTA O ERRO E VAI ATE O FIM
        #sys.exit()

print("\n")
print("### ATENÇÃO ### Criação DB Python bem sucedida!!")
