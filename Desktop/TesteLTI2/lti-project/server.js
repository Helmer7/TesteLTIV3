const express = require('express');
const cors = require('cors');
const app = express();
const port = process.env.PORT || 3000;


app.use(cors({
    origin: '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'x-csrf-token'],
    credentials: true
}));


app.use(express.json());


app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization");
    if (req.method === 'OPTIONS') {
        res.header('Access-Control-Allow-Methods', 'PUT, POST, PATCH, DELETE, GET');
        return res.status(200).json({});
    }
    next();
});


app.get('/', (req, res) => {
    res.send(`
        <html lang="pt-BR">
        <head>
            <title>Integração LTI</title>
        </head>
        <body>
            Servidor LTI rodando!
        </body>
        </html>
    `);
});


app.post('/lti', (req, res) => {
    console.log('Requisição recebida:', req.body);

    
    const username = req.body['User.username'] || req.body.username;
    const course = req.body['CourseTemplate.title'] || req.body.course;
    const startDate = req.body['ResourceLink.available.startDateTime'] || req.body.startDate;

    
    if (!username || !course || !startDate) {
        console.log("Erro: Dados insuficientes");
        return res.status(400).json({
            message: 'Erro: Dados insuficientes, certifique-se de que os parâmetros "username", "course" e "startDate" estão sendo enviados corretamente.'
        });
    }

    
    console.log(`LTI recebido: Aluno: ${username}, Curso: ${course}, Início: ${startDate}`);
    res.json({
        message: `LTI lançado com sucesso para o aluno ${username} no curso ${course}, início em ${startDate}`,
    });
});


app.listen(port, () => {
    console.log(`Servidor rodando na porta ${port}`);
});
