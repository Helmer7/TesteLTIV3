const express = require('express');
const cors = require('cors');
const axios = require('axios');  // Importa Axios para chamadas de API
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
            <style>
                body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
                h1 { color: #333; }
            </style>
        </head>
        <body>
            <h1>Servidor LTI rodando!</h1>
        </body>
        </html>
    `);
});

app.post('/lti', async (req, res) => {
    console.log('Requisição recebida:', JSON.stringify(req.body, null, 2));  
    
    const username = req.body['User.username'] || req.body.username;
    const course = req.body['CourseTemplate.title'] || req.body.course;
    const startDate = req.body['ResourceLink.available.startDateTime'] || req.body.startDate;

    if (!username || !course || !startDate) {
        console.log("Erro: Dados insuficientes");
        
        return res.send(`
            <html lang="pt-BR">
            <head>
                <title>Erro de Dados</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
                    h1 { color: red; }
                    p { color: #333; font-size: 16px; }
                </style>
            </head>
            <body>
                <h1>Erro: Dados insuficientes!</h1>
                <p>Por favor, verifique se os parâmetros obrigatórios estão sendo enviados corretamente:</p>
                <ul>
                    <li>Username: ${username ? username : '<b>Faltando</b>'}</li>
                    <li>Curso: ${course ? course : '<b>Faltando</b>'}</li>
                    <li>Data de início: ${startDate ? startDate : '<b>Faltando</b>'}</li>
                </ul>
            </body>
            </html>
        `);
    }

    try {
        // Exemplo de requisição para a API externa para obter mais informações
        const apiResponse = await axios.get(`https://sua-api.com/api/v1/nead/alunos/${username}`, {
            headers: { 'Authorization': 'Bearer SEU_TOKEN_DE_ACESSO' }
        });

        const alunoInfo = apiResponse.data;

        console.log(`Dados do aluno recebidos da API: ${JSON.stringify(alunoInfo, null, 2)}`);

        // Renderiza a página com os dados recebidos
        res.send(`
            <html lang="pt-BR">
            <head>
                <title>Sucesso LTI</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
                    h1 { color: green; }
                    p { color: #333; font-size: 16px; }
                </style>
            </head>
            <body>
                <h1>LTI lançado com sucesso!</h1>
                <p>Aluno: <strong>${alunoInfo.nome}</strong></p>
                <p>Curso: <strong>${course}</strong></p>
                <p>Data de Início: <strong>${startDate}</strong></p>
                <p>Dados adicionais do aluno: ${alunoInfo.detalhes}</p>
            </body>
            </html>
        `);
    } catch (error) {
        console.error('Erro ao buscar informações adicionais do aluno:', error);
        res.status(500).send("Erro ao processar a requisição.");
    }
});

app.listen(port, () => {
    console.log(`Servidor rodando na porta ${port}`);
});
