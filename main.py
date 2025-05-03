from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Onibus(BaseModel):
    linha: str
    ocupacao: int
    atualizado_em: float

onibus_db: List[Onibus] = [
    Onibus(linha="875C", ocupacao=38, atualizado_em=time.time()),
    Onibus(linha="302T", ocupacao=22, atualizado_em=time.time()),
    Onibus(linha="111A", ocupacao=10, atualizado_em=time.time()),
]

@app.get("/onibus", response_model=List[Onibus])
def listar_onibus():
    return onibus_db

@app.post("/onibus")
def atualizar_onibus(dados: Onibus):
    for i, bus in enumerate(onibus_db):
        if bus.linha == dados.linha:
            onibus_db[i] = dados
            return {"status": "atualizado"}
    onibus_db.append(dados)
    return {"status": "criado"}

@app.get("/painel", response_class=HTMLResponse)
def painel_visual():
    html = """
    <html>
        <head>
            <title>Painel Busômetro</title>
            <style>
                body { font-family: Arial; padding: 2rem; background: #f9f9f9; }
                h1 { color: #2563eb; }
                table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
                th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #ccc; }
                .baixa { background-color: #bbf7d0; }
                .media { background-color: #fde68a; }
                .alta { background-color: #fecaca; }
            </style>
        </head>
        <body>
            <h1>Ocupação dos Ônibus</h1>
            <table>
                <tr><th>Linha</th><th>Ocupação</th><th>Última Atualização</th></tr>
    """
    for onibus in onibus_db:
        cor = "baixa" if onibus.ocupacao <= 15 else "media" if onibus.ocupacao <= 30 else "alta"
        atualizado = time.strftime('%H:%M:%S', time.localtime(onibus.atualizado_em))
        html += f"<tr class='{cor}'><td>{onibus.linha}</td><td>{onibus.ocupacao} pessoas</td><td>{atualizado}</td></tr>"
    html += """
            </table>
        </body>
    </html>
    """
    return HTMLResponse(content=html)
