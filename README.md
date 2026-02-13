# Customer Analytics – Segmentação RFM e Análise de Concentração de Receita

## Sobre o Projeto

Este projeto simula um ambiente real de Engenharia de Dados e Analytics aplicado à análise de clientes.

A partir de dados sintéticos de transações, construi um pipeline completo de dados no modelo **Bronze → Silver → Gold**, culminando em um dashboard analítico no Power BI com segmentação RFM e análise de concentração de receita (Pareto 80/20).
---

## Arquitetura do Projeto

O fluxo do projeto segue a arquitetura clássica de Data Lake:

Geração de Dados (Python)
↓
Bronze (dados brutos)
↓
Silver (dados limpos e estruturados)
↓
Gold (métricas agregadas - RFM)
↓
Power BI (Dashboard Analítico)


## 🛠 Tecnologias Utilizadas

- Python
- Pandas
- Parquet
- Power BI
- DAX
- Modelagem em camadas (Bronze / Silver / Gold)

## 🔄 Pipeline de Dados

### 1️⃣ Geração de Dados Sintéticos
- Criação de clientes e transações fictícias
- Catálogo de produtos com preços fixos
- Simulação de 1 ano de movimentação

### 2️⃣ Camada Bronze
- Ingestão de dados brutos em CSV
- Armazenamento inicial sem transformação

### 3️⃣ Camada Silver
- Limpeza e padronização dos dados
- Conversão para formato Parquet
- Tratamento de tipos e consistência

### 4️⃣ Camada Gold
- Agregação por cliente
- Construção do modelo RFM:
  - **Recency** → Dias desde a última compra
  - **Frequency** → Quantidade de transações
  - **Monetary** → Total gasto
- Criação de segmentação estratégica

---

## Análises Implementadas

### 🔹 Segmentação RFM
Classificação de clientes em grupos estratégicos como:
- Campeões
- Leais
- Potenciais
- Em risco
- Perdidos

### 🔹 KPIs Estratégicos
- Total de Clientes
- Receita Total
- Ticket Médio
- Percentual de Receita por Segmento

### 🔹 Análise de Concentração de Receita (Pareto 80/20)
- Ranking de clientes por faturamento
- Receita acumulada
- Identificação do percentual da base responsável por 80% da receita

## Principais Insights

- Identificação de clientes de alto valor
- Avaliação do nível de concentração de receita
- Distribuição estratégica da base de clientes
---

![Dashboard Analítico](dashborad\dashboard_print.png)