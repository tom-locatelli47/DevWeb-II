from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# Modelo para itens
class Item(BaseModel):
    id: int
    nome: str
    preco: float

# Modelo para entrada de dados (POST/PUT)
class ItemInput(BaseModel):
    nome: str = Field(..., min_length=1, description="Nome não pode ser vazio")
    preco: float = Field(..., gt=0, description="Preço deve ser maior que zero")

# Modelo para resposta de POST
class ItemInputResponse(BaseModel):
    message: str
    dados: Item

# Lista de itens em memória
# Lista de itens em memória
items = [
    Item(id=1, nome="Notebook", preco=3500.00),
    Item(id=2, nome="Mouse", preco=80.00),
    Item(id=3, nome="Teclado", preco=150.00),
    Item(id=4, nome="Monitor", preco=1200.00),
    Item(id=5, nome="Impressora", preco=300.00),
    Item(id=6, nome="Cadeira Gamer", preco=950.00),
    Item(id=7, nome="Headset", preco=250.00),
    Item(id=8, nome="HD Externo 1TB", preco=400.00),
    Item(id=9, nome="SSD 512GB", preco=600.00),
    Item(id=10, nome="Placa de Vídeo RTX 3060", preco=2500.00),
    Item(id=11, nome="Memória RAM 16GB", preco=320.00),
    Item(id=12, nome="Fonte 600W", preco=450.00),
    Item(id=13, nome="Gabinete Gamer", preco=350.00),
    Item(id=14, nome="Processador Ryzen 5", preco=1100.00),
    Item(id=15, nome="Placa-Mãe ASUS", preco=900.00),
    Item(id=16, nome="Webcam Full HD", preco=270.00),
    Item(id=17, nome="Microfone Condensador", preco=420.00),
    Item(id=18, nome="Notebook Gamer", preco=5800.00),
    Item(id=19, nome="Smartphone", preco=2200.00),
    Item(id=20, nome="Tablet", preco=1500.00),
    Item(id=21, nome="Smartwatch", preco=800.00),
    Item(id=22, nome="Roteador Wi-Fi 6", preco=500.00),
    Item(id=23, nome="Caixa de Som Bluetooth", preco=300.00),
    Item(id=24, nome="Pen Drive 128GB", preco=90.00),
    Item(id=25, nome="Carregador Portátil", preco=150.00),
]


# Listar todos os produtos (GET)
@app.get("/produtos", response_model=list[Item])
def listar_produtos(min_preco: float | None = None, max_preco: float | None = None, 
                    ordenar_por: str = "id",
                    ordem: str = "asc",
                    pagina: int = 0,
                     por_pagina: int = 10):
    resultado = items
    if min_preco is not None:
        resultado = [item for item in resultado if item.preco >= min_preco]
    if max_preco is not None:
        resultado = [item for item in resultado if item.preco <= max_preco]

    resultado.sort(key=lambda x: getattr(x, ordenar_por), reverse=(ordem == "desc"))

    return resultado[pagina * por_pagina : (pagina + 1) * por_pagina]

# Listar produto por ID (GET)
@app.get("/produtos/{item_id}", response_model=Item)
def listar_produto_por_id(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Produto não encontrado")

# Criar novo produto (POST)
@app.post("/produtos", response_model=ItemInputResponse)
def criar_produto(item: ItemInput):
    novo_id = max(item_existente.id for item_existente in items) + 1
    novo_item = Item(id=novo_id, **item.model_dump())
    items.append(novo_item)
    return ItemInputResponse(message="Produto criado com sucesso", dados=novo_item)

# Atualizar produto (PUT)
@app.put("/produtos/{item_id}", response_model=ItemInputResponse)
def atualizar_produto(item_id: int, item_atualizado: ItemInput):
    for i, item in enumerate(items):
        if item.id == item_id:
            items[i] = Item(id=item_id, **item_atualizado.model_dump())
            return ItemInputResponse(message="Produto atualizado com sucesso", dados=items[i])
    raise HTTPException(status_code=404, detail="Produto não encontrado")

# Remover produto (DELETE)
@app.delete("/produtos/{item_id}")
def remover_produto(item_id: int):
    for i, item in enumerate(items):
        if item.id == item_id:
            items.pop(i)
            return {"message": "Produto removido com sucesso"}
    raise HTTPException(status_code=404, detail="Produto não encontrado")

# Rodar servidor:

# .venv\Scripts\Activate
  
# uvicorn main:app --reload

# Acesse a documentação da API em http://localhost:8000/docs