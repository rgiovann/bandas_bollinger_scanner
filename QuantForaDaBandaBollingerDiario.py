# =============================================================================
# Identifica fechamentos acima ou abaixo da banda de bollinger
# MME21 e MME34
# Busca por possiveis retrações do preço durante  a abertura
# =============================================================================

import datetime
import QuantUtilities as util
from pathlib import Path

cwd = str(Path.cwd())
str_path_hist = cwd + "\\Database_Python\\"
str_path_out_logs = cwd +"\\LOGS\\"
file_name = str_path_out_logs + "ForaBandaBoll_" + datetime.datetime.now().strftime('%Y_%d_%m_%H_%M_%S') + ".txt"
file_relat = open(file_name, "a")

EMA_VALOR = 21
DOIS_DP = 2
DOIS_E_MEIO_DP = 2.5
dict_ativos_precos = util.le_historico_ativos(str_path_hist,str_path_out_logs,file_relat)
printa_linha = False

print("|-----------------------------------------------------------|", file=file_relat)
print("|      ATIVOS COM FECHAMENTO FORA BB (MME21 diário)         |", file=file_relat)    
print("|-----------------------------------------------------------|", file=file_relat)
print("|                                                           |", file=file_relat)
print("| DATA:..........: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z%z")+"                     |", file=file_relat)
print("|                                                           |", file=file_relat)
print("|-----------------------------------------------------------|", file=file_relat) 
print("|     ATIVO     | 2.5DP(+) |  2.DP(+) | 2.5DP(-) |  2.DP(-) |", file=file_relat) 
print("|-----------------------------------------------------------|", file=file_relat)    

for k_ativo, v_preco in sorted(dict_ativos_precos.items()):

    # =============================================================================
    #  AQUI PROCESSO O SETUP 9.2 e 9.3          
    # =============================================================================
    v_preco = v_preco.iloc[::-1]    # datas mais recentes serão as ultimas linhas.    


    lista_IFR = (util.calculaIFR(v_preco['Fechamento'], 3)).tolist()

    # trato somente os LAG_PRECO_9X valores
    # NOCA CASO DE MEDIA MOVEL, PEGO PERIODO MAIOR

    v_preco['EMA21']  = v_preco['Fechamento'].ewm(span=EMA_VALOR, adjust=False).mean()
    
    v_preco['std_fechamento' ] = v_preco['Fechamento'].rolling(window = EMA_VALOR).std()
    
    banda_superior_EMA_VALOR_2DP = v_preco['Fechamento'].iloc[-1] + DOIS_DP*v_preco['std_fechamento'].iloc[-1]
    banda_inferior_EMA_VALOR_2DP = v_preco['Fechamento'].iloc[-1] - DOIS_DP*v_preco['std_fechamento'].iloc[-1]

    banda_superior_EMA_VALOR_2_E_MEIO_DP = v_preco['Fechamento'].iloc[-1] + DOIS_E_MEIO_DP*v_preco['std_fechamento'].iloc[-1]
    banda_inferior_EMA_VALOR_2_E_MEIO_DP = v_preco['Fechamento'].iloc[-1] - DOIS_E_MEIO_DP*v_preco['std_fechamento'].iloc[-1]
    
    str_2_E_MEIO_PLUS = ""
    str_2_E_MEIO_MINUS = ""
    str_2_PLUS = ""
    str_2_MINUS = ""    
    printa_linha = False

    if v_preco['Fechamento'].iloc[-1] >= v_preco['EMA21'].iloc[-1] + DOIS_E_MEIO_DP*v_preco['std_fechamento'].iloc[-1]:
        str_2_E_MEIO_PLUS ="*"
        printa_linha = True

    elif v_preco['Fechamento'].iloc[-1] >= v_preco['EMA21'].iloc[-1] + DOIS_DP*v_preco['std_fechamento'].iloc[-1]:
        str_2_PLUS = "*"
        printa_linha = True
    
    elif v_preco['Fechamento'].iloc[-1] <= v_preco['EMA21'].iloc[-1] - DOIS_E_MEIO_DP*v_preco['std_fechamento'].iloc[-1]:
        str_2_E_MEIO_MINUS ="*"
        printa_linha = True
        
    elif v_preco['Fechamento'].iloc[-1] <= v_preco['EMA21'].iloc[-1] - DOIS_DP*v_preco['std_fechamento'].iloc[-1]:
        str_2_MINUS = "*" 
        printa_linha = True
        
        
    if  printa_linha:
        print("|      {0:6s}   |    {1:3}   |    {2:3}   |    {3:3}   |    {4:3}   |".format(k_ativo,str_2_E_MEIO_PLUS,str_2_PLUS,str_2_E_MEIO_MINUS,str_2_MINUS), file=file_relat)       
        
print("|-----------------------------------------------------------|", file=file_relat)            
file_relat.close()
print("Execução encerrada, verifique o resultado em ..\LOGS, arquivo " + file_name )            

