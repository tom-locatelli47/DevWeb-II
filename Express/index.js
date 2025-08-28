const express = require("express");
const app = express();
app.use(express.json());

let produtos = [
  { id: 1, nome: "Notebook", preco: 3500.0 },
  { id: 2, nome: "Mouse", preco: 80.0 },
  { id: 3, nome: "Teclado", preco: 150.0 },
  { id: 4, nome: "Monitor", preco: 1200.0 },
  { id: 5, nome: "Impressora", preco: 300.0 },
];

// GET /produtos com filtros, ordenação e paginação
app.get("/produtos", (req, res) => {
  let resultado = [...produtos];
  const { min_preco, max_preco, ordenar_por, ordem, pagina, por_pagina } =
    req.query;

  if (min_preco)
    resultado = resultado.filter((p) => p.preco >= parseFloat(min_preco));
  if (max_preco)
    resultado = resultado.filter((p) => p.preco <= parseFloat(max_preco));

  if (ordenar_por) {
    resultado.sort((a, b) => {
      if (a[ordenar_por] < b[ordenar_por]) return ordem === "desc" ? 1 : -1;
      if (a[ordenar_por] > b[ordenar_por]) return ordem === "desc" ? -1 : 1;
      return 0;
    });
  }

  let pag = parseInt(pagina) || 0;
  let porPag = parseInt(por_pagina) || resultado.length;
  resultado = resultado.slice(pag * porPag, pag * porPag + porPag);
  res.json(resultado);
});

app.post("/produtos", (req, res) => {
  // Remover a lógica de filtragem, ordenação e paginação do POST /produtos
  const { nome, preco } = req.body;
  if (!nome || nome.trim() === "") {
    return res.status(400).json({ error: "O nome não pode ser vazio" });
  }
  if (typeof preco !== "number" || preco <= 0) {
    return res.status(400).json({ error: "O preço deve ser maior que zero" });
  }
  const novoId = produtos.length
    ? Math.max(...produtos.map((p) => p.id)) + 1
    : 1;
  const novoProduto = { id: novoId, nome, preco };
  produtos.push(novoProduto);
  res.json({ message: "Produto criado com sucesso", dados: novoProduto });
});

app.get("/produtos/:id", (req, res) => {
  const produto = produtos.find((p) => p.id === parseInt(req.params.id));
  if (!produto)
    return res.status(404).json({ error: "Produto não encontrado" });
  res.json(produto);
});

app.post("/produtos", (req, res) => {
  const { nome, preco } = req.body;
  const novoId = produtos.length
    ? Math.max(...produtos.map((p) => p.id)) + 1
    : 1;
  const novoProduto = { id: novoId, nome, preco };
  produtos.push(novoProduto);
  res.json({ message: "Produto criado com sucesso", dados: novoProduto });
});

app.put("/produtos/:id", (req, res) => {
  const index = produtos.findIndex((p) => p.id === parseInt(req.params.id));
  if (index === -1)
    return res.status(404).json({ error: "Produto não encontrado" });
  produtos[index] = { id: parseInt(req.params.id), ...req.body };
  res.json({
    message: "Produto atualizado com sucesso",
    dados: produtos[index],
  });
});

app.delete("/produtos/:id", (req, res) => {
  const index = produtos.findIndex((p) => p.id === parseInt(req.params.id));
  if (index === -1)
    return res.status(404).json({ error: "Produto não encontrado" });
  produtos.splice(index, 1);
  res.json({ message: "Produto removido com sucesso" });
});

app.listen(8000, () => console.log("Servidor rodando na porta 8000"));

// Rodar servidor:
// npm install express
// node index.js
