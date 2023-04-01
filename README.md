<h2> Scanner de fechamentos de preços diário acima ou abaixo das bandas de Bollinger (BB) faixas de +/- 2 e +/- 2,5 desvios padrões</h2>
<p><h4> O algoritmo escaneia uma lista de ativos configurárveis pelo usuário e baseado no histórico de preços sem ajuste
extraidos manualmente do home broker Tryd são salvos no diretório ..\Database_Tryd e então mapeados em 
listas csv que podem ser lidas pelo Python no diretório ..\Database_Python, a seguir o algortimo é executado e o resultado do scan é armazenado no diretório ..\LOGS.

Os passos para executar o scan dos ativos que tocam as BB são os seguinte:
<ol>
    <li> Delete todos os arquivos que existam no diretório ..\Database_Tryd, estão desatualizados  </li>
    <li> Defina quais o ativos a serem escaneados </li>
    <li> Modifique a lista de ativos no arquivo <i>QuantMT5ConstantesGlobais.py</i> variável LISTA_B3</li>
    <li> Execute o script <i>Migracao_Unica_Precos_do_Tryd_para_Python.py</i>para popular o diretório ..\Database_Python</li>
    <li> Execute o arquivo  <i>QuantForaDaBandaBollingerDiario.py</i></li>
    <li> Verifique o resultado no diretório ..\LOGS</i></li>
</ol>

No caso do exemplo deste repositório, nos temos os seguintes ativos monitorados:
For production environments...

```sh
LISTA_B3 = {'ABEV3', 'BBAS3','ENBR3','EQTL3','GGBR4','GOLL4','HYPE3','IGTI3','ITUB4','JBSS3','LREN3',
            'MDIA3','MRFG3','PETR4','QUAL3','RENT3','SAPR4','SUZB3','TIMS3','USIM5','VALE3'}
```

Os arquivos correspondentes já estão salvos nos diretórios ..\Database_Tryd  e ..\Database_Pytho, logo ao executar o script, temos

```sh
Importação de dados bem sucedida!...Total de ativos importados : 21

Execução encerrada, verifique o resultado em ..\LOGS, arquivo E:\FINANCAS_QUANTITATIVAS\Source_Code\BOLLINGER_BANDS\LOGS\ForaBandaBoll_2023_31_03_22_45_54.txt
```

E no arquivo em questão:

```sh
|-----------------------------------------------------------|
|      ATIVOS COM FECHAMENTO FORA BB (MME21 diário)         |
|-----------------------------------------------------------|
|                                                           |
| DATA:..........: 2023-03-31 22:55:13                      |
|                                                           |
|-----------------------------------------------------------|
|     ATIVO     | 2.5DP(+) |  2.DP(+) | 2.5DP(-) |  2.DP(-) |
|-----------------------------------------------------------|
|      HYPE3    |          |          |    *     |          |
|-----------------------------------------------------------|

```

O ativo HYPE3 (Hyperfarma) fechou abaixo da banda de bollinger de média exponencial de 21 periódos (uma média bem conhecida em Análise Técnica). Ao analisarmos o gráfico de candles do ativo, realmente
o preço de fechamento ficou abaixo da banda de bollinger inferior de 2,5 desvios padrões (linha amarela)



<h3>🛠 Informações úteis</h3>

O que são bandas de bollinger : https://es.wikipedia.org/wiki/Bandas_de_Bollinger

Home Broker Tryd : https://www.tryd.com.br/</h3>

Análise Técnica: https://pt.wikipedia.org/wiki/An%C3%A1lise_t%C3%A9cnica
</h4>
