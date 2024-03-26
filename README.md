# Webscrap Linkedin

Um webscrap para recuperar vagas do linkedin utilizando python e selenium.

## Documentação
O Webscrap é feito na versão 'deslogada' do Linkedin, para evitar problemas com a conta pessoal. Devido a isso, o acesso a informações é menor, e o rate limit é maior. O que torna o processo um pouco mais demorado em alguns casos.


## Como funciona:
- Primeiramente, devido aos problemas com authwall e erro 429 devido ao limite da api, é inserido um limite de páginas no loop do programa, então mesmo que não consiga encontrar todas as vagas devido ao limite, as vagas que foram capturadas ainda serão salvas.

- Seguindo com o programa, o driver do Selenium é inicializado
- Pagina do linkedin, no endpoint de vagas é aberta (com parametros na url especificados como localização, nome do cargo, entre outros)
- O selenium varre a página até o fim, se tiver um botão para acessar mais vagas, ele é apertado automaticamente.
- Após isso, todas essas vagas estarão armazenadas em uma outra lista, e em um loop for, cada página de detalhe da vaga será acessada através do link da vaga (Nessa página, mais informações estão disponíveis mesmo estando deslogado)
- Após esse processo, finalmente os dados estão prontos e são armazenados em um banco de dados sqlite de forma temporária.

A estrutura dos dados capturados é:

![image](https://github.com/PedroCozzati/webscrap-linkedin/assets/80106385/1b0ecb60-ccf7-4990-9d56-52cc321725f7)

Obs: Algumas informações que precisam ser capturadas dentro da página de detalhes da vaga podem vir nulas, devido ao fato que a cada request para uma nova página, o linkedin pode bloquear com uma authwall, exigindo uma autenticação

Esse projeto foi utilizado em outro >> [ETL-LINKEDIN](https://github.com/PedroCozzati/pipeline-airflow-etl-linkedin)

## Tecnologias utilizadas

Python

Selenium

Beautiful Soap


