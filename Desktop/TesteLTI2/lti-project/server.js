const express = require('express');
const cors = require('cors');
const app = express();
const port = process.env.PORT || 3000;

app.use(cors({
    origin: '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
}));

app.use(express.json());

app.get('/', (req, res) => {
    res.send('Servidor LTI rodando!');
});

app.post('/lti', (req, res) => {
    const { username, course } = req.body;
    res.json({
        message: `LTI lançado com sucesso para o aluno ${username} no curso ${course}`,
    });
});

app.listen(port, () => {
    console.log(`Servidor rodando na porta ${port}`);
});
