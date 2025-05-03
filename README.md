# Busômetro API

API e painel para estimar ocupação de ônibus em tempo real.

## Rotas principais:
- `GET /onibus`: Lista a ocupação estimada dos ônibus.
- `POST /onibus`: Atualiza a ocupação de uma linha.
- `GET /painel`: Mostra um painel web com os dados.

## Executando localmente
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Acesse:
- Painel: http://127.0.0.1:8000/painel
- API: http://127.0.0.1:8000/onibus
- Docs: http://127.0.0.1:8000/docs
