
<p align="center">
  <b>Selecione o idioma / Select language:</b><br>
  <a href="#ptbr">🇧🇷 Português (BR)</a> |
  <a href="#enus">🇺🇸 English (US)</a>
</p>

---

## <a id="ptbr"></a>🇧🇷 Português (BR)

> **Observação:** Este repositório refere-se à versão **v0.0.2.0** do Projeto Economia APP. Apoie o projeto e adquira a versão paga através do link: [Instalar via Microsoft Store](https://apps.microsoft.com/detail/9PLR0KD6KSJJ)

<details>
<summary>Clique para expandir o README em português</summary>

# Calculadora de Economia de Engenharia (Economia APP)

Versão: v0.0.2.0  
Autor: Fernando Nillsson Cidade

Aplicação desktop em Python + PySide6 para cálculos clássicos de economia de engenharia: juros simples/compostos, anuidades, gradientes, equivalência de taxas, amortizações (SAC, Price, SAM), análise de investimentos (VPL e VAUE) e depreciação (linear e soma dos dígitos). Projeto organizado por pacotes `source.ui` (interfaces) e `source.services` (lógica de cálculo), com a classe principal `FinancialCalculatorApp`.

## Sumário
- Visão geral
- Pré-requisitos
- Executando
- Estrutura do projeto
- Descrição detalhada das funcionalidades (por aba)
- Notas de implementação

---

## Visão geral
A aplicação fornece uma interface em abas onde o usuário insere parâmetros (valores, taxas, número de períodos) e obtém:
- Resultado numérico formatado
- Passo a passo dos cálculos (texto explicativo)
- Para amortizações: tabela detalhada por período

---

## Pré-requisitos
- Python 3.8+
- PySide6

Instalação rápida:
```bash
pip install -r requirements.txt   # ou: pip install PySide6
```

---

## Executando
No Windows, em terminal do projeto:
```powershell
python main.py
```
O ponto de entrada é `main.py`, que instancia `FinancialCalculatorApp`.

---

## Estrutura principal de arquivos
- main.py — inicializa QApplication e a janela principal.
- source/
  - fca_01_FinancialCalculatorAPP.py — classe QMainWindow que monta a UI e injeta métodos.
  - ui/ — funções que constroem a interface (uma função por aba / helper).
    - ui_01_create_layout.py — layout base (form + painel direito).
    - ui_02_get_float_from_line_edit.py — conversor/validador de texto para float (trata vírgula e %).
    - ui_03_create_interest_tab.py — aba Juros.
    - ui_04_create_annuity_tab.py — aba Anuidades.
    - ui_05_create_gradient_tab.py — aba Gradientes.
    - ui_06_create_rates_tab.py — aba Equivalência de taxas e taxa real/aparente.
    - ui_07_create_amortization_tab.py — aba Amortização (tabela + controles).
    - ui_08_create_investment_tab.py — aba Análise de Investimentos (VPL/VAUE).
    - ui_09_create_depreciation_tab.py — aba Depreciação.
    - ui_10_generate_sac_table.py — gera tabela SAC.
    - ui_11_generate_price_table.py — gera tabela Price.
    - ui_12_generate_sam_table.py — gera tabela SAM (média SAC+Price).
    - ui_13_set_amort_table_row.py — helper para preencher linha da tabela.
    - ui_14_get_table_data.py — extrai dados da tabela.
  - services/ — implementação das regras e passos de cálculo.
    - sv_01_calculate_interest.py — juros simples e compostos (calcular F ou P).
    - sv_02_calculate_annuity.py — calcular A ou P para séries postecipada/antecipada.
    - sv_03_calculate_gradient.py — gradiente aritmético e geométrico (cálculo de P).
    - sv_04_calculate_real_rate_equivalence.py — equivalência de taxas efetivas e taxa real/aparente.
    - sv_05_calculate_amortization.py — lógica que organiza geração e passo a passo das amortizações.
    - sv_06_calculate_investment.py — VPL (Verdadeiro Presente Líquido) e VAUE (anualização).
    - sv_07_calculate_depreciation.py — depreciação linear e soma dos dígitos dos anos.
  - __init__.py — exporta `FinancialCalculatorApp`.
  - ui/__init__.py e services/__init__.py — reexportam as funções usadas pela classe principal.

---

## Funcionalidades detalhadas (por aba)

### Juros Simples e Compostos
Arquivo de serviço: `sv_01_calculate_interest.py`  
Funcionalidade:
- Permite calcular Montante (F) a partir do Principal (P) ou calcular Principal (P) a partir do Montante (F).
- Suporta regimes:
  - Juros Compostos: F = P * (1 + i)^n ; P = F / (1 + i)^n
  - Juros Simples: F = P * (1 + n * i) ; P = F / (1 + n * i)
- Produz texto com fórmulas, substituições, valores intermediários e resultado formatado.
- Inputs: P ou F, taxa i (como %), número de períodos n.

### Anuidades (Séries)
Arquivo de serviço: `sv_02_calculate_annuity.py`  
Funcionalidade:
- Calcular Prestação (A) ou Valor Presente (P) para séries:
  - Postecipada (vencimento ao final do período)
  - Antecipada (vencimento no início do período)
- Fórmulas utilizadas:
  - Postecipada: A = P * [i*(1+i)^n] / [(1+i)^n - 1]  e P = A * [(1+i)^n - 1] / [i*(1+i)^n]
  - Antecipada: usa potências (1+i)^(n-1) nas fórmulas equivalentes.
- Gera passos detalhados com componentes numéricos.

### Gradientes
Arquivo de serviço: `sv_03_calculate_gradient.py`  
Funcionalidade:
- Gradiente Aritmético (G): cálculo do Valor Presente P usando a fórmula
  P = (G / i) * [ (P/A, i, n) - n*(P/F, i, n) ]
- Gradiente Geométrico (g): cálculo do Valor Presente P para série crescente geometricamente:
  - Usa r = (1+g)/(1+i) e trata caso i == g como fórmula especial.
- Inputs: tipo de gradiente, g/G, i, n. Fornece passo a passo.

### Conversão de Taxas e Taxa Real/Aparente
Arquivo de serviço: `sv_04_calculate_real_rate_equivalence.py`  
Funcionalidade:
- Equivalência de Taxas Efetivas:
  - i_eq obtida por (1+i_eq) = (1+i)^(n2/n1) — converte entre períodos.
- Taxa Real e Aparente (considerando inflação θ):
  - Calcular taxa aparente i a partir de taxa real r e inflação θ: 1+i = (1+r)*(1+θ)
  - Calcular taxa real r a partir de i e θ: 1+r = (1+i)/(1+θ)
- Exibe substituições e valores intermediários.

### Amortização (SAC, Price, SAM)
Arquivo de serviço: `sv_05_calculate_amortization.py` + helpers em `ui_10..ui_14`  
Funcionalidade:
- Interface para escolher sistema de amortização:
  - Sistema Francês (Price): prestações constantes; fator (A/P) = [i*(1+i)^n] / [(1+i)^n - 1]
  - Sistema de Amortização Constante (SAC): amortização constante A_k = P / n; juros decrescentes.
  - Sistema Misto (SAM): média período a período entre SAC e Price.
- Geração de tabela com colunas: período, prestação, juros, amortização, saldo devedor.
- Helpers:
  - `generate_sac_table`, `generate_price_table`, `generate_sam_table` — constroem a tabela e retornam dados brutos.
  - `set_amort_table_row` — preenche linha formatada.
  - `get_table_data` — extrai os dados da tabela para uso posterior.
- Fornece demonstração do primeiro período e explicação das fórmulas aplicadas.

### Análise de Investimentos (VPL e VAUE)
Arquivo de serviço: `sv_06_calculate_investment.py`  
Funcionalidade:
- Calcula:
  - VPB (Valor Presente dos Benefícios) a partir de uma entrada periódica A: VPB = A * (P/A, i, n)
  - VPL = VPB - Investimento_inicial
  - VAUE = VPL * (A/P, i, n) — anualização do VPL
- Mostra fórmula do fator (P/A) e (A/P), valores intermediários e conclusão de viabilidade (VPL > 0).
- Inputs: investimento inicial, fluxo A, n, TMA (taxa mínima de atratividade em %).

### Depreciação
Arquivo de serviço: `sv_07_calculate_depreciation.py`  
Funcionalidade:
- Dois métodos:
  - Método Linear: DR_anual = (P - VRE) / N ; permite calcular valor contábil ao final do ano k: VC_k = P - k * DR
  - Soma dos Dígitos dos Anos: soma = N*(N+1)/2 ; quotas por ano decrescentes; calcula quota do ano k, depreciação acumulada e VC_k = P - dep_acumulada
- Inputs: valor de aquisição P, valor residual estimado VRE, vida útil N, opcional ano k.

---

## Notas de implementação / como o código está organizado
- A classe `FinancialCalculatorApp` em `fca_01_FinancialCalculatorAPP.py` injeta as funções do pacote `ui` e `services` como métodos da instância (atribuição de função a `FinancialCalculatorApp.<nome>`). Isso mantém os módulos organizados por responsabilidade (UI vs lógica).
- Conversões e validações:
  - `get_float_from_line_edit` trata entradas vazias, substitui vírgula por ponto e, se indicado, converte percentuais (divide por 100).
- A interface monta um painel esquerdo (formulários) e um painel direito (resultados e tabelas) por aba.
- Tratamento de erros: cada serviço captura exceções e escreve mensagem de erro no QTextEdit correspondente.

---

## Considerações finais
- O projeto prioriza legibilidade didática: cada cálculo mostra os passos algébricos e valores intermediários para facilitar o entendimento.
- Para evoluir:
  - Adicionar validações adicionais de domínio (ex.: taxas negativas, divisões por zero).
  - Exportar tabelas para CSV/Excel.
  - Internacionalização (i18n) se necessário.

---

</details>

## <a id="enus"></a>🇺🇸 English (US)

> **Note:** This repository refers to the **v0.0.2.0** version of the Economia APP Project. Support the project and purchase the paid version through the link: [Instalar via Microsoft Store](https://apps.microsoft.com/detail/9PLR0KD6KSJJ)

<details>
<summary>Click to expand the README in English</summary>

# Engineering Economy Calculator (Economia APP)

Version: v0.0.2.0  
Author: Fernando Nillsson Cidade

Desktop application in Python + PySide6 for classic engineering economy calculations: simple/compound interest, annuities, gradients, rate equivalence, amortizations (SAC, Price, SAM), investment analysis (NPV and annualized value) and depreciation (straight-line and sum-of-years-digits). Project organized into `source.ui` (interfaces) and `source.services` (calculation logic) packages, with the main class `FinancialCalculatorApp`.

## Table of contents
- Overview
- Requirements
- Running
- Project structure
- Detailed features (by tab)
- Implementation notes

---

## Overview
The application provides a tabbed interface where the user enters parameters (amounts, rates, number of periods) and receives:
- Formatted numeric result
- Step-by-step calculation explanation (text)
- For amortizations: detailed table per period

---

## Requirements
- Python 3.8+
- PySide6

Quick install:
```bash
pip install -r requirements.txt   # or: pip install PySide6
```

---

## Running
On Windows, in the project terminal:
```powershell
python main.py
```
The entry point is `main.py`, which instantiates `FinancialCalculatorApp`.

---

## Main file structure
- main.py — initializes QApplication and the main window.
- source/
  - fca_01_FinancialCalculatorAPP.py — QMainWindow class that builds the UI and injects methods.
  - ui/ — functions that build the interface (one function per tab / helper).
    - ui_01_create_layout.py — base layout (form + right panel).
    - ui_02_get_float_from_line_edit.py — text-to-float converter/validator (handles comma and %).
    - ui_03_create_interest_tab.py — Interest tab.
    - ui_04_create_annuity_tab.py — Annuities tab.
    - ui_05_create_gradient_tab.py — Gradients tab.
    - ui_06_create_rates_tab.py — Rate equivalence and real/apparent rate tab.
    - ui_07_create_amortization_tab.py — Amortization tab (table + controls).
    - ui_08_create_investment_tab.py — Investment Analysis (NPV/annualized) tab.
    - ui_09_create_depreciation_tab.py — Depreciation tab.
    - ui_10_generate_sac_table.py — generates SAC table.
    - ui_11_generate_price_table.py — generates Price table.
    - ui_12_generate_sam_table.py — generates SAM table (SAC+Price average).
    - ui_13_set_amort_table_row.py — helper to fill a table row.
    - ui_14_get_table_data.py — extracts data from the table.
  - services/ — implementation of rules and calculation steps.
    - sv_01_calculate_interest.py — simple and compound interest (calculate F or P).
    - sv_02_calculate_annuity.py — calculate A or P for ordinary/annuity-due series.
    - sv_03_calculate_gradient.py — arithmetic and geometric gradients (calculate P).
    - sv_04_calculate_real_rate_equivalence.py — effective rate equivalence and real/apparent rate.
    - sv_05_calculate_amortization.py — logic that organizes amortization generation and step-by-step.
    - sv_06_calculate_investment.py — NPV (Net Present Value) and annualization.
    - sv_07_calculate_depreciation.py — straight-line and sum-of-years-digits depreciation.
  - __init__.py — exports `FinancialCalculatorApp`.
  - ui/__init__.py and services/__init__.py — re-export functions used by the main class.

---

## Detailed features (by tab)

### Simple and Compound Interest
Service file: `sv_01_calculate_interest.py`  
Functionality:
- Allows calculating Future Value (F) from Principal (P) or calculating Principal (P) from Future Value (F).
- Supports regimes:
  - Compound Interest: F = P * (1 + i)^n ; P = F / (1 + i)^n
  - Simple Interest: F = P * (1 + n * i) ; P = F / (1 + n * i)
- Produces text with formulas, substitutions, intermediate values and formatted result.
- Inputs: P or F, rate i (as %), number of periods n.

### Annuities (Series)
Service file: `sv_02_calculate_annuity.py`  
Functionality:
- Calculate Payment (A) or Present Value (P) for series:
  - Ordinary (due at the end of the period)
  - Annuity-due (due at the beginning of the period)
- Formulas used:
  - Ordinary: A = P * [i*(1+i)^n] / [(1+i)^n - 1]  and P = A * [(1+i)^n - 1] / [i*(1+i)^n]
  - Annuity-due: uses powers (1+i)^(n-1) in the equivalent formulas.
- Generates detailed steps with numeric components.

### Gradients
Service file: `sv_03_calculate_gradient.py`  
Functionality:
- Arithmetic Gradient (G): present value P calculated using
  P = (G / i) * [ (P/A, i, n) - n*(P/F, i, n) ]
- Geometric Gradient (g): present value P for a geometrically growing series:
  - Uses r = (1+g)/(1+i) and handles the special case i == g.
- Inputs: gradient type, g/G, i, n. Provides step-by-step explanation.

### Rate Conversion and Real/Apparent Rate
Service file: `sv_04_calculate_real_rate_equivalence.py`  
Functionality:
- Effective Rate Equivalence:
  - i_eq obtained by (1+i_eq) = (1+i)^(n2/n1) — converts between periods.
- Real and Apparent Rate (considering inflation θ):
  - Calculate apparent rate i from real rate r and inflation θ: 1+i = (1+r)*(1+θ)
  - Calculate real rate r from i and θ: 1+r = (1+i)/(1+θ)
- Displays substitutions and intermediate values.

### Amortization (SAC, Price, SAM)
Service file: `sv_05_calculate_amortization.py` + helpers in `ui_10..ui_14`  
Functionality:
- Interface to choose amortization system:
  - French System (Price): constant payments; factor (A/P) = [i*(1+i)^n] / [(1+i)^n - 1]
  - Constant Amortization System (SAC): constant amortization A_k = P / n; decreasing interest.
  - Mixed System (SAM): period-by-period average between SAC and Price.
- Generates a table with columns: period, payment, interest, amortization, outstanding balance.
- Helpers:
  - `generate_sac_table`, `generate_price_table`, `generate_sam_table` — build the table and return raw data.
  - `set_amort_table_row` — fills a formatted row.
  - `get_table_data` — extracts table data for later use.
- Provides demonstration of the first period and explanation of applied formulas.

### Investment Analysis (NPV and Annualized Value)
Service file: `sv_06_calculate_investment.py`  
Functionality:
- Calculates:
  - PV of Benefits (VPB) from a periodic inflow A: VPB = A * (P/A, i, n)
  - NPV = VPB - Initial_Investment
  - Annualized NPV = NPV * (A/P, i, n) — annualization of the NPV
- Shows the (P/A) and (A/P) factor formulas, intermediate values and a viability conclusion (NPV > 0).
- Inputs: initial investment, cash flow A, n, MARR (minimum attractive rate in %).

### Depreciation
Service file: `sv_07_calculate_depreciation.py`  
Functionality:
- Two methods:
  - Straight-Line Method: annual_depr = (P - SRV) / N ; allows computing book value at the end of year k: BV_k = P - k * annual_depr
  - Sum-of-Years-Digits: sum = N*(N+1)/2 ; decreasing annual shares; computes year k quota, accumulated depreciation and BV_k = P - accumulated_depr
- Inputs: acquisition value P, estimated residual value SRV, useful life N, optional year k.

---

## Implementation notes / how the code is organized
- The `FinancialCalculatorApp` class in `fca_01_FinancialCalculatorAPP.py` injects functions from the `ui` and `services` packages as instance methods (assigning functions to `FinancialCalculatorApp.<name>`). This keeps modules organized by responsibility (UI vs logic).
- Conversions and validations:
  - `get_float_from_line_edit` handles empty inputs, replaces comma with dot and, if indicated, converts percentages (divides by 100).
- The interface builds a left panel (forms) and a right panel (results and tables) per tab.
- Error handling: each service captures exceptions and writes an error message to the corresponding QTextEdit.

---

## Final notes
- The project prioritizes didactic readability: each calculation shows algebraic steps and intermediate values to aid understanding.
- To evolve:
  - Add additional domain validations (e.g.: negative rates, division by zero).
  - Export tables to CSV/Excel.
  - Internationalization (i18n) if necessary.

---

</details>