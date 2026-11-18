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

1. Escolhe o **modelo de estimativa**: Geral (todas as marcas, R²=0.86) ou Popular (9 marcas, R²=0.95)
2. Seleciona a **marca** (filtrada pelas marcas do modelo escolhido)
3. Seleciona o **modelo**
4. Seleciona o **ano**
5. Seleciona o **câmbio** (opções baseadas no modelo/ano)
6. Seleciona o **combustível**
7. Seleciona a **direção**
8. Seleciona a **faixa de quilometragem**
9. Clica em **Estimar Preço Justo**

A interface retorna a estimativa de preço pelo modelo selecionado, a média e o desvio padrão dos anúncios reais com os mesmos filtros, e um aviso caso a estimativa esteja fora do desvio padrão de mercado.

## Estrutura

```
scrap-car-front/
├── app.py                      ← entrada: orquestra filtros, estimativa e anúncios
├── components/
│   ├── filtros.py              ← seleção em cascata + escolha do modelo
│   ├── estimativa.py           ← chama /ml/prever e /ml/media, exibe resultado
│   └── anuncios.py             ← lista anúncios reais com comparativo de preço
├── services/
│   └── carro_service.py        ← fachada entre components e api_client
└── clients/
    └── api_client.py           ← chamadas HTTP para a API
```
