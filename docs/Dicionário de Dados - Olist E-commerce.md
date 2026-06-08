# **📊 Dicionário de Dados & Metadados: E-commerce Olist**

Este documento apresenta o mapeamento detalhado, a tipagem e as regras de negócio das tabelas que compõem a base de dados pública de comércio eletrónico da Olist (Brasil). Esta documentação serve como base estrutural para a nossa **Análise Exploratória de Dados (EDA)**.

## **🗺️ Visão Geral do Modelo de Dados**

A base de dados é composta por **9 tabelas relacionais**, ligadas através de chaves primárias e estrangeiras. O ecossistema permite analisar o ciclo de vida completo de uma compra, desde a navegação do cliente e processamento do pagamento até à entrega logística e avaliação final do serviço.

## **📋 Detalhe das Tabelas e Atributos**

### **1\. Tabela: orders (Pedidos)**

*Esta é a tabela central do ecossistema. Regista a jornada de compra do cliente e os tempos associados à operação logística.*

| Nome da Coluna | Tipo Original | Tipo Proposto | Descrição |
| :---- | :---- | :---- | :---- |
| **order\_id** | str (object) | str | Identificador único de cada pedido. |
| **customer\_id** | str (object) | str | Chave estrangeira que liga o pedido ao cliente (ID exclusivo por transação). |
| **order\_status** | str (object) | category | Estado atual do pedido (ex: delivered, canceled, shipped, processing). |
| **order\_purchase\_timestamp** | str (object) | datetime64 | Data e hora em que a compra foi realizada na plataforma. |
| **order\_approved\_at** | str (object) | datetime64 | Data e hora em que a instituição financeira aprovou o pagamento. |
| **order\_delivered\_carrier\_date** | str (object) | datetime64 | Data e hora em que o pacote foi entregue à transportadora parceira. |
| **order\_delivered\_customer\_date** | str (object) | datetime64 | Data e hora em que o cliente recebeu efetivamente o produto em sua casa. |
| **order\_estimated\_delivery\_date** | str (object) | datetime64 | Data estimada de entrega prometida ao cliente no momento do checkout. |

### **2\. Tabela: order\_items (Itens dos Pedidos)**

*Detala os produtos individuais contidos em cada pedido, os seus valores e as datas-limite de envio.*

| Nome da Coluna | Tipo Original | Tipo Proposto | Descrição |
| :---- | :---- | :---- | :---- |
| **order\_id** | str (object) | str | Chave de ligação com a tabela orders (pode repetir-se em carrinhos multi-item). |
| **order\_item\_id** | int64 | int64 | Número sequencial que identifica o item dentro de um mesmo pedido (ex: 1, 2, 3). |
| **product\_id** | str (object) | str | Chave estrangeira de ligação com a tabela de produtos. |
| **seller\_id** | str (object) | str | Chave estrangeira de ligação com a tabela de vendedores. |
| **shipping\_limit\_date** | str (object) | datetime64 | Data limite estipulada pelo parceiro logístico para o vendedor enviar o produto. |
| **price** | float64 | float64 | Preço de venda unitário do produto (exclui o custo do frete). |
| **freight\_value** | float64 | float64 | Valor cobrado pelo transporte do produto até ao destino final. |

### **3\. Tabela: products (Produtos)**

*Contém os atributos físicos, dimensões e categorias dos produtos disponíveis para venda.*

| Nome da Coluna | Tipo Original | Tipo Proposto | Descrição |
| :---- | :---- | :---- | :---- |
| **product\_id** | str (object) | str | Identificador único de cada produto. |
| **product\_category\_name** | str (object) | str | Nome da categoria do produto (em português). |
| **product\_name\_lenght** | float64 | int16 | Comprimento em caracteres do título do anúncio do produto. |
| **product\_description\_lenght** | float64 | int16 | Comprimento em caracteres da descrição detalhada do produto. |
| **product\_photos\_qty** | float64 | int8 | Quantidade total de fotografias exibidas na página do anúncio. |
| **product\_weight\_g** | float64 | float64 | Peso físico do produto embalado em gramas (g). |
| **product\_length\_cm** | float64 | float64 | Comprimento do pacote em centímetros (cm). |
| **product\_height\_cm** | float64 | float64 | Altura do pacote em centímetros (cm). |
| **product\_width\_cm** | float64 | float64 | Largura do pacote em centímetros (cm). |

### **4\. Tabela: customers (Clientes)**

*Regista os dados demográficos e de localização dos clientes registados.*

| Nome da Coluna | Tipo Original | Tipo Proposto | Descrição |
| :---- | :---- | :---- | :---- |
| **customer\_id** | str (object) | str | ID transacional gerado por compra (usado para ligar com orders). |
| **customer\_unique\_id** | str (object) | str | ID permanente do cliente (permite calcular recorrência, retenção e LTV). |
| **customer\_zip\_code\_prefix** | int64 | int64 | Primeiros 5 dígitos do código postal (CEP) do cliente. |
| **customer\_city** | str (object) | str | Nome da cidade de destino onde o cliente reside. |
| **customer\_state** | str (object) | category | Sigla do Estado (Unidade Federativa) de destino do cliente. |

### **5\. Tabela: payments (Pagamentos)**

*Detala os aspetos financeiros e as condições de pagamento escolhidas pelos utilizadores.*

| Nome da Coluna | Tipo Original | Tipo Proposto | Descrição |
| :---- | :---- | :---- | :---- |
| **order\_id** | str (object) | str | Chave estrangeira que aponta para o pedido associado ao pagamento. |
| **payment\_sequential** | int64 | int8 | Sequência caso o pagamento tenha sido dividido em vários métodos (ex: 2 cartões). |
| **payment\_type** | str (object) | category | Método de pagamento (credit\_card, boleto, voucher, debit\_card). |
| **payment\_installments** | int64 | int8 | Número de prestações/parcelas mensais acordadas na transação. |
| **payment\_value** | float64 | float64 | Valor financeiro total pago nesta transação (inclui taxas de frete). |

### **6\. Tabela: reviews (Avaliações)**

*Recolhe o feedback dos consumidores após o término da jornada logística.*

| Nome da Coluna | Tipo Original | Tipo Proposto | Descrição |
| :---- | :---- | :---- | :---- |
| **review\_id** | str (object) | str | Identificador exclusivo da avaliação de satisfação. |
| **order\_id** | str (object) | str | Chave estrangeira que aponta para o pedido avaliado pelo cliente. |
| **review\_score** | int64 | int8 | Classificação quantitativa de satisfação atribuída de 1 a 5 (estrelas). |
| **review\_comment\_title** | str (object) | str | Título resumo da mensagem de avaliação deixada pelo cliente. |
| **review\_comment\_message** | str (object) | str | Comentário em texto corrido detalhando a experiência do utilizador. |
| **review\_creation\_date** | str (object) | datetime64 | Data em que o convite para responder ao inquérito de satisfação foi enviado. |
| **review\_answer\_timestamp** | str (object) | datetime64 | Data e hora em que o cliente respondeu efetivamente à avaliação. |

## **🔍 Primeiras Descobertas & Gargalos Operacionais Encontrados**

Durante o processo inicial de análise e auditoria de metadados, identificámos as seguintes situações críticas a serem resolvidas no Pipeline de Dados:

### **1\. Incoerência de Tipagem temporal**

Múltiplas colunas críticas de data e hora (ex: order\_purchase\_timestamp, shipping\_limit\_date) foram inicialmente carregadas como strings (object). Foi necessário implementar um bloco de conversão explícita para datetime64 antes de prosseguir para as métricas temporais e de SLA.

### **2\. Anomalias nos Registos de Entrega (orders)**

Verificou-se que cerca de 3% dos pedidos possuem valores nulos na coluna order\_delivered\_customer\_date. Através de uma análise cruzada, validámos que se trata de uma regra estrutural do negócio:

* A esmagadora maioria refere-se a transações que ainda se encontram em trânsito (shipped), foram canceladas (canceled) ou estão indisponíveis (unavailable).  
* **Anomalia Identificada:** Foram detetados exatamente **8 pedidos** com o status delivered mas sem a respetiva data de entrega registada. Estes casos deverão ser isolados e reportados como anomalias de engenharia de dados.

### **3\. Gestão e Análise de Clientes Recorrentes**

Há uma distinção vital entre customer\_id e customer\_unique\_id. O primeiro varia a cada nova compra, enquanto o segundo permanece idêntico e consistente. Para qualquer análise de segmentação (RFM), taxa de recompra ou valor do tempo de vida do cliente (LTV), é mandatório agrupar as transações através do customer\_unique\_id.