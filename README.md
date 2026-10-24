# Comparador de Índices Econômicos

> Este projeto foi gerado automaticamente por IA e revisado por um agente automatizado, nao por uma pessoa. Leia o codigo antes de usar.

## Descrição

CLI em Python para consultar uma série SGS pública do Banco Central do Brasil (BCB) em um intervalo de datas e calcular a variação percentual acumulada entre a primeira e a última observação retornadas.

A saída é apresentada como uma tabela no terminal, com o intervalo solicitado, as datas efetivas das observações, os valores inicial e final e a variação acumulada.

## Objetivo

Apoiar a consulta de indicadores econômicos e o cálculo transparente de sua variação em um período informado, reduzindo a necessidade de interpretar manualmente datas e valores retornados pelo serviço SGS do BCB.

## Como funciona

1. A CLI recebe o código numérico da série SGS, a data inicial e a data final no formato `DD/MM/AAAA`.
2. As datas são convertidas e enviadas à API SGS do BCB como `dataInicial` e `dataFinal`.
3. A resposta JSON é validada e cada observação é convertida para data e `Decimal`.
4. As observações são ordenadas por data.
5. A primeira e a última observação disponíveis são usadas para o cálculo:

   ```text
   variação (%) = ((valor final / valor inicial) - 1) × 100
   ```

6. O resultado é renderizado em uma tabela.

A aplicação informa erros amigáveis para código de série não numérico, datas inválidas, falhas de consulta, dados inesperados ou ausentes e valor inicial igual a zero.

## Arquitetura

O projeto é organizado como um pacote Python em `src/comparador_indices/`:

- `requirements.txt`: dependências necessárias para executar o experimento.
- `src/comparador_indices/__init__.py`: expõe modelos e funções públicas do pacote.
- `src/comparador_indices/__main__.py`: ponto de entrada para `python -m comparador_indices`.
- `src/comparador_indices/cli.py`: define os argumentos da CLI, trata erros esperados e renderiza a tabela.
- `src/comparador_indices/bcb_client.py`: consulta a API SGS do BCB e converte a resposta em observações.
- `src/comparador_indices/models.py`: define as dataclasses `Observation` e `Comparison`, além dos erros de domínio.
- `src/comparador_indices/service.py`: valida datas, ordena observações e calcula a variação acumulada.
- `tests/conftest.py`: configuração de apoio aos testes.
- `tests/test_bcb_client.py`: testes do cliente do BCB.
- `tests/test_cli.py`: testes da interface de linha de comando.
- `tests/test_service.py`: testes das regras de serviço e cálculo.

## Tecnologias

- Python 3.11+
- `httpx`, para consultas HTTP à API do BCB
- `tabulate`, para renderização da tabela no terminal
- `dataclasses`, `datetime`, `decimal`, `argparse` e demais recursos da biblioteca padrão
- pytest, fornecido pelo ambiente de execução

## Instalação

É necessário ter Python 3.11 ou superior.

Instale as dependências do projeto com:

```bash
python -m pip install -r requirements.txt
```

O pacote está sob `src/` e o projeto não possui arquivo de instalação. Portanto, defina `PYTHONPATH=src` antes de executá-lo.

## Configuração

A aplicação lê a seguinte variável de ambiente:

| Variável | Descrição | Valor padrão |
|---|---|---|
| `BCB_SGS_BASE_URL` | URL base do serviço SGS consultado pelo cliente. | `https://api.bcb.gov.br/dados/serie/bcdata.sgs` |

Não há configuração de credenciais.

## Uso

A CLI recebe três argumentos posicionais:

```text
python -m comparador_indices <serie> <data_inicial> <data_final>
```

- `serie`: código SGS composto somente por números.
- `data_inicial`: data no formato `DD/MM/AAAA`.
- `data_final`: data no formato `DD/MM/AAAA`.

No Linux/macOS:

```bash
PYTHONPATH=src python -m comparador_indices <serie> <data_inicial> <data_final>
```

No Windows (PowerShell):

```powershell
$env:PYTHONPATH="src"; python -m comparador_indices <serie> <data_inicial> <data_final>
```

Use `--help` para exibir a ajuda dos argumentos.

## Exemplos

Exemplo de consulta usando um código SGS numérico ilustrativo:

No Linux/macOS:

```bash
PYTHONPATH=src python -m comparador_indices 1 01/01/2024 31/01/2024
```

No Windows (PowerShell):

```powershell
$env:PYTHONPATH="src"; python -m comparador_indices 1 01/01/2024 31/01/2024
```

Em caso de sucesso, a saída contém uma tabela com os campos:

- série;
- intervalo solicitado;
- data e valor inicial;
- data e valor final;
- variação acumulada em percentual.

## Testes

Execute os testes com:

```bash
python -m pytest
```

Os testes não acessam a rede: a consulta HTTP é dublada durante sua execução.

## Limitações

- A CLI consulta somente uma série SGS por execução.
- O código da série deve ser informado pelo usuário; não há catálogo, busca por nome ou apelidos de indicadores.
- A variação usa a primeira e a última observação efetivamente retornadas pela API, que podem não corresponder exatamente às datas solicitadas.
- Não há persistência de consultas, exportação de dados, gráficos, cache ou agendamento.
- A execução normal depende da disponibilidade da API pública do BCB e de conectividade de rede.
- O cálculo não é realizado quando o valor inicial da observação é zero.

## O que foi aprendido

O experimento demonstra uma integração HTTP pequena e separada da lógica de domínio: o cliente consulta e normaliza os dados, enquanto o serviço ordena observações e calcula a variação com `Decimal`.

Também evidencia a importância de tratar respostas HTTP, JSON inválido, estruturas inesperadas, datas e valores inválidos com mensagens voltadas ao usuário, além de dublar a integração externa nos testes.

## Possível aplicação na FOX

A ferramenta pode apoiar consultas rápidas para premissas econômicas em reajustes, orçamentos e acompanhamento de indicadores. A separação entre CLI, cliente do BCB e cálculo também oferece uma base simples para integrações públicas que precisem de validação e cálculos rastreáveis.

## Status

O relatório de testes recebido informa que a execução foi aprovada: **9 testes coletados e 9 testes passaram**.
