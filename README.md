# Calculadora de Economia de Engenharia (Economia_APP)

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
