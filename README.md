# scrap-car-front

Interface web do projeto **scrap-carros** — TCC. Permite estimar o preço justo de um carro com base em suas características, consumindo a API do `scrap-car-back`.

## Stack

- Python 3.14
- Streamlit
- Requests

## Pré-requisitos

- Python 3.14 instalado
- API do `scrap-car-back` rodando em `http://localhost:8000`

## Instalação

```bash
pip install -r requirements.txt
```

## Executando

```bash
make run
```

Ou diretamente:

```bash
py -3.14 -m streamlit run app.py
```

Acessa em `http://localhost:8501`.

## Fluxo de uso

1. Seleciona a **marca** do carro
2. Seleciona o **modelo**
3. Seleciona o **ano**
4. Seleciona o **câmbio** (opções baseadas no modelo/ano)
5. Seleciona o **combustível**
6. Seleciona a **direção**
7. Seleciona a **faixa de quilometragem**
8. Clica em **Estimar Preço Justo**

A interface retorna a estimativa de preço pelo **Modelo Geral** e, quando aplicável, pelo **Modelo Popular** (carros das marcas mais vendidas no Brasil).

## Estrutura

```
scrap-car-front/
├── app.py              ← interface Streamlit
├── services/
│   └── carro_service.py← regras e formatação
└── clients/
    └── api_client.py   ← chamadas HTTP para a API
```
