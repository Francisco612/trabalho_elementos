# Análise de Desemprego Jovem e Abandono Escolar em Portugal
Alunos da Universidade da Beira Interior, Francisco Sousa (Nº53642), Inês Alves (Nº55182), cujos ID's no GitHub são Francisco612 e inestalves correspondente.

Para este trabalho, explorámos o portal da Pordata com o objetivo de encontrar relações entre as estatísticas sobre Portugal. Após analisarmos vários estatisticas tentando perceber quais poderiam apresentar uma relação entre si, decidimos focar-nos em dois temas muito relevantes e de nosso intresse:

* A taxa de retenção e desistência no ensino secundário por modalidade de ensino.
* O desemprego registado nos centros de emprego por grupo etário

O nosso objetivo foi perceber:

* Se a educação secundária è o fator decisivo para conseguir emprego.
* Se existe uma correlação entre os municípios com maior abandono escolar e maior taxa de desemprego entre os jovens.
---
##  Estrutura do Projeto

trabalho_elementos/
│
├── analise_dados/                     
│   ├── __init__.py
│   ├── analise_dados.py              
│   └── graficos_dados_ausentes.py    
│
├── csv_analise/                       
│   ├── 386.csv
│   └── 439.csv
│
├── limpeza_processamento_dados/     
│   ├── __init__.py
│   ├── remover_outliers.py           
│   └── valores_ausentes.py           
│
├── resultados_csv/                   
│   ├── data_final.csv                
│   ├── data_final_limpo.csv          
│   └── data_final_sem_va.csv        
│
├── analiseDescritiva.py            
├── main.py                           
├── recolha_dados.py                  
├── testes.py                         
├── requirements.txt                   
└── README.md                         


---

##  Fonte de Dados

- **Fonte:** [PORDATA](https://www.pordata.pt)
- **Indicadores usados:**
  - *Desemprego registado nos centros de emprego (para menores de 25 anos)*
  - *Taxa de retenção e desistência no ensino secundário por modalidade de ensino*
- **Intrevalo de tempo:** 2009 a 2023  


---

## Metodologia

O projeto foi desenvolvido em várias fases, conforme o enunciado:

1. **Recolha de Dados**  
   Seleção e download dos indicadores desejados no formato CSV, a partir do PORDATA.

2. **Integração de Dados**  
   Fusão dos datasets num único ficheiro

3. **🔍 Análise Exploratória**  
   Verificação de correlações, outliers, valores em falta, e redundância nas variáveis.

4. ** Limpeza e Pré-processamento**  
   - Remoção de colunas irrelevantes ou com muitos valores nulos.
   - Preenchimento ou exclusão de valores em falta.
   - Normalização dos dados.

5. **Análise Descritiva**  
   - Redução da dimensionalidade com PCA.
   - Agrupamento de municípios com KMeans.
   - Identificação de extremos: municípios com maiores/menores taxas de desemprego e desistência.

---

##  Instalação e Requisitos

### Requisitos
- contourpy==1.3.2
- cycler==0.12.1
- fonttools==4.58.1
- joblib==1.5.1
- kiwisolver==1.4.8
- matplotlib==3.10.3
- numpy==2.2.6
- packaging==25.0
- pandas==2.2.3
- pillow==11.2.1
- pyparsing==3.2.3
- python-dateutil==2.9.0.post0
- pytz==2025.2
- scikit-learn==1.6.1
- scipy==1.15.3
- seaborn==0.13.2
- six==1.17.0
- threadpoolctl==3.6.0
- tzdata==2025.2

### Instalação

```bash
pip install -r requirements.txt
```
---
## Como executar
* Colonar este repositótio: 
```bash
git clone https://github.com/Francisco612/trabalho_elementos
cd trabalho_elementos
```
* Instalar dependências:
```bash
pip install -r requirements.txt
```
___
### Conclusão

Com base na análise descritiva, conseguimos identificar padrões relevantes entre os municípios portugueses no que se refere ao desemprego jovem e à desistência escolar. A segmentação em três grupos distintos evidencia que fatores como a oferta educativa (profissional vs. geral) e as políticas locais podem ter um impacto significativo nos resultados obtidos por cada município.

Assim, esta análise oferece informações importantes para decisões educacionais e sociais mais orientadas, reforçando a utilidade de abordagens baseadas em dados para o planeamento territoral e a promoção da inclusão juvenil.

