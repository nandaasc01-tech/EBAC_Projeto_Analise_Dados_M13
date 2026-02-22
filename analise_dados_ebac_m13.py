
# Importando Bibliotecas que serão utilizadas.
from itertools import groupby

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv('MODULO7_PROJETOFINAL_BASE_SUPERMERCADO.csv')

# Visualizando dados que serão analisados

print(df.head(10).to_string())
df.info()

# Verificando os valores das colunas

dados_por_categoria = [df.groupby('Categoria')['Preco_Normal'].count().reset_index().sort_values(by=['Preco_Normal'], ascending=False).head(10)]
print(dados_por_categoria)

# Identificando a média por Categoria da coluna 'Preco_Normal'.

media_por_categoria_preco_normal = [df.groupby('Categoria')['Preco_Normal'].mean().reset_index().sort_values(by=['Preco_Normal'], ascending=False).head(10)]
print('Média por Categoria da coluna Preço Normal:\n ',media_por_categoria_preco_normal)

# Identificando a mediana por Categoria da coluna 'Preço_Normal'.

mediana_por_categoria_preco_normal = [df.groupby('Categoria')['Preco_Normal'].median().reset_index().sort_values(by=['Preco_Normal'], ascending=False).head(10)]
print('Mediana por Categoria da coluna Preço Normal:\n ',mediana_por_categoria_preco_normal)

# Identificando as categorias que tem a média a baixo ou acima da mediana.
# Agrupando a média e mediana em um DataFrema para garantir que as categorias batam

df_metricas = df.groupby('Categoria')['Preco_Normal'].agg(['mean','median']).reset_index()

print(df_metricas)

# Identificando as categorias onde a média é maior ou menos que a mediana.

categorias_media_maior = df_metricas[df_metricas['mean'] > df_metricas['median']] # Média maior
print('Categorias onde a média é maior do que a médiana:\n ',categorias_media_maior)

categorias_media_menor = df_metricas[df_metricas['mean'] < df_metricas['median']] # Média menor
print('Categorias onde a média é menor do que a médiana:\n ',categorias_media_menor)

# Verificando o Desvio padrão das categorias.

desvio_padrao_categorias = df.groupby('Categoria')['Preco_Normal'].std().reset_index()
print(' Desvio Padrão das Categorias:\n ', desvio_padrao_categorias)

# Plotando um boxplot para verificar os Outliers da Categoria Lacteos, pois foi a categoria que apresentou o maior desvio padrão.

dados_lacteos = df.loc[df['Categoria'] == 'lacteos']['Preco_Normal']

plt.figure(figsize=(8,6))
plt.boxplot(dados_lacteos, showmeans=True)

# Customizando o gráfico

plt.title('Distribuição de Preços : Categoria Lacteos', fontsize=20)
plt.ylabel('Preço Normal')
plt.xlabel('Lacteos')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show() # CONCLUSÃO: Foi identificado inúmeros outliers

# Plotando um gráfico de barras com a média de descontos por categoria

media_por_categoria_descontos = (df[df['Preco_Desconto'] > 0].groupby('Categoria')['Preco_Desconto'].mean().reset_index().sort_values(by=['Preco_Desconto'], ascending=False))
print(media_por_categoria_descontos)

plt.figure(figsize=(8,6))
plt.bar(media_por_categoria_descontos['Categoria'], media_por_categoria_descontos['Preco_Desconto'], color='skyblue')
plt.title('Distribuição de Descontos por Categoria', fontsize= 18)
plt.xlabel('Categoria', fontsize= 12)
plt.ylabel('Descontos', fontsize= 12)
plt.xticks(rotation=0, ha='right')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# Plotando um Gráfico de Mapa Interativo com Categoria, Marca e a Média de Descontos.
df_com_desconto = df[df['Preco_Desconto'] > 0]

# Criando uma lista para agrupar colunas

desconto_por_marca = df_com_desconto.groupby(['Categoria','Marca'])['Preco_Desconto'].mean().reset_index()
desconto_por_marca = desconto_por_marca.sort_values(by=['Preco_Desconto'], ascending=False)

print(desconto_por_marca)

# Plotando TreeMap

fig = px.treemap(desconto_por_marca,
                 path=['Categoria', 'Marca'],
                 values='Preco_Desconto',
                 title= 'Desconto por Marca e Categoria',
                 color= 'Preco_Desconto',
                 color_continuous_scale='RdBu')
fig.show()
