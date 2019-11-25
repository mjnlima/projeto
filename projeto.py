#!/usr/bin/env python
# coding: utf-8

# In[48]:


#bibliotecas
import pandas
from bokeh.io import output_file, output_notebook
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import reset_output
from bokeh.transform import factor_cmap, factor_mark, linear_cmap

#lê os dados de um CSV previamente tratado e o armazena num objeto dataframe do pandas
dados = pandas.read_csv("/home/njm/git/projeto/dados.csv",
	sep = ';',
	parse_dates=[0]
	)

#elimina registros duplicados
dados = dados.drop_duplicates()

#reindexa o dataframe
dados = dados.reset_index()

#adiciona uma coluna com 1 para cada registro a fim de facilitar a contagem de itens
dados = dados.assign(CONTAGEM=1)

dados.loc[:, 'QUANTIDADE_GERADA'] = dados.get('QUANTIDADE_GERADA').str.replace('.','')
dados.loc[:, 'QUANTIDADE_GERADA'] = dados.get('QUANTIDADE_GERADA').str.replace(',','.')

#configura a saída para um notebook jupyter
#output_notebook()
colunas = dados.columns

#ferramentas de interatividade
TOOLS = "crosshair, pan, wheel_zoom, box_zoom, reset, box_select, tap"


# In[49]:


#filtra dados de 2016
amostraPoluentes = (dados[(dados['ANO'] == '2016-01-01')]
	.loc[:, ['ANO', 'SIGLA_DA_UNIDADE_DA_FEDERACAO', 'MUNICIPIO', 'CATEGORIA_DE_ATIVIDADE', 'QUANTIDADE_GERADA', 'UNIDADE', 'PRODUTO_INTERNO_BRUTO_A_PRECOS_CORRENTES', 'POPULACAO', 'PRODUTO_INTERNO_BRUTO_PER_CAPITA', 'CONTAGEM', 'CNPJ_DO_GERADOR']]
	.sort_values(['ANO', 'SIGLA_DA_UNIDADE_DA_FEDERACAO', 'MUNICIPIO']))

#filtra registros medidos em kg
amostraPoluentes = amostraPoluentes[amostraPoluentes['UNIDADE'] == 'KILOGRAMAS']

dadosPoluentes = amostraPoluentes.drop_duplicates()


# In[66]:





# In[128]:


grafico2Empresas = dadosPoluentes.drop(columns=['ANO', 'MUNICIPIO', 'POPULACAO', 'QUANTIDADE_GERADA',
                                                'CATEGORIA_DE_ATIVIDADE', 'UNIDADE',
                                                'PRODUTO_INTERNO_BRUTO_A_PRECOS_CORRENTES',
                                                'PRODUTO_INTERNO_BRUTO_PER_CAPITA'])
grafico2Empresas = grafico2Empresas.drop_duplicates().groupby(['SIGLA_DA_UNIDADE_DA_FEDERACAO'], as_index=False).sum()
grafico1_DS = ColumnDataSource(grafico2Empresas)

grafico2Poluentes = dadosPoluentes.drop(columns=['ANO', 'MUNICIPIO', 'MUNICIPIO', 'UNIDADE',
                                                'PRODUTO_INTERNO_BRUTO_A_PRECOS_CORRENTES',
                                                ])
grafico2_DS = ColumnDataSource(grafico2Poluentes)

categorias = ['INDUSTRIA DE PRODUTOS MINERAIS NAO METALICOS',
              'TRANSPORTE, TERMINAIS, DEPOSITOS E COMERCIO',
              'INDUSTRIA DE BORRACHA',
              'INDUSTRIA DE COUROS E PELES',
              'INDUSTRIA QUIMICA',
              'INDUSTRIA DE PRODUTOS ALIMENTARES E BEBIDAS',
              'INDUSTRIA METALURGICA',
              'INDUSTRIA DE MATERIAL DE TRANSPORTE',
              'INDUSTRIA DE PAPEL E CELULOSE',
              'USO DE RECURSOS NATURAIS',
              'INDUSTRIA DE PRODUTOS DE MATERIA PLASTICA']


p1 = figure(x_range=grafico2Empresas.get('SIGLA_DA_UNIDADE_DA_FEDERACAO'),
           #x_axis_type=Auto,
           plot_height=512,
           plot_width=768,
           title="Número de empresas",
           tools=TOOLS
           )

p1.vbar(x='SIGLA_DA_UNIDADE_DA_FEDERACAO', top='CONTAGEM', width=0.8, source=grafico1_DS)

p1.xgrid.grid_line_color = None
p1.y_range.start = 0


marca = ['circle']

p2 = figure(title = 'Relação entre população, riqueza e poluentes emitidos',
            plot_width=512, plot_height=512, tools=TOOLS, toolbar_location='below')
p2.xaxis.axis_label = 'PIB per capita'
p2.yaxis.axis_label = 'Poluentes emitidos (kg)' # a ver redução de ordem (1000 t)

p2.scatter('PRODUTO_INTERNO_BRUTO_PER_CAPITA', 'QUANTIDADE_GERADA',
          fill_alpha=0.8, size=4,
          #marker=factor_mark('CATEGORIA_DE_ATIVIDADE', marca, categorias),
          #color=factor_cmap('POPULACAO', cores, categorias),
          color=linear_cmap('POPULACAO', 'Viridis256', 0, 200000, nan_color="#00FFFF"),
          selection_color='deepskyblue',
          nonselection_color='lightgray',
          source=grafico2_DS)


p3 = figure(title="Visão de população e riqueza", plot_width=512, plot_height=512, tools=TOOLS)
p3.xaxis.axis_label = 'População'
p3.yaxis.axis_label = 'PIB per capita'

p3.circle(x='POPULACAO', y='PRODUTO_INTERNO_BRUTO_PER_CAPITA',
        source=grafico2_DS,
        color=linear_cmap('PRODUTO_INTERNO_BRUTO_PER_CAPITA', 'Magma256', 0, 100000),
        radius='PRODUTO_INTERNO_BRUTO_PER_CAPITA',
        selection_color='deepskyblue',
        nonselection_color='lightgray')

grid = gridplot([[p1, p2, p3]])

show(grid)


# In[ ]:




