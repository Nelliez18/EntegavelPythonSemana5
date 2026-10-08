# Documento README.md: Justificativa das validações aplicadas, explicação das exceções tratadas, exemplos de entrada (arquivo lido) e saída (relatório gerado):

# Sistema de Analise e Higienizacao de Dados em Python

Este projeto consiste em um sistema automatizado para leitura, tratamento e higienizacao de arquivos de dados no formato CSV, aplicando rotinas de validacao por meio de expressoes regulares (Regex) e blindagem contra falhas operacionais com tratamento de excecoes.

## Funcionalidades do Sistema

1. Leitura de Arquivos: Mapeamento estruturado de dados organizados em formato CSV.
2. Filtros com Expressoes Regulares: Validacao morfologica dos campos de E-mail, CPF, Telefone e Data.
3. Mecanismo de Tolerancia a Falhas: Tratamento integrado para arquivos ausentes, dados incompativeis ou falhas de cabecalho.
4. Geracao de Estatisticas: Emissao de relatorios gerenciais com percentuais de integridade dos registros lidos.

---

## Justificativa das Validacoes (Expressoes Regulares)

Para garantir que os dados estejam em conformidade com as regras de negocio de sistemas nacionais, apliquei as seguintes estruturas em Regex atraves do modulo re:

*   E-mail (^[\w.-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}\$)
    *   ^ e \$: Garantem que o texto inteiro seja avaliado, impedindo e-mails validos colados no meio de textos invalidos.
    *   [\w.-]+: Aceita caracteres alfanumericos, pontos e hifens antes da arroba.
    *   \.[a-zA-Z]{2,}: Certifica a presenca de um sufixo de dominio legitimo (ex: .com, .org, .net).
*   CPF (^\d{11}\$)
    *   A funcao primeiro remove qualquer formatacao visual (como pontos ou tracos) usando re.sub(r"\D", "", cpf).
    *   O padrao ^\d{11}\$ assegura que o dado final contenha estritamente onze digitos numericos sequenciais.
*   Telefone (^(\(?\d{2}\)?\s?)?\d{4,5}-?\d{4}\$)
    *   (\(?\d{2}\)?\s?)?: Torna a identificacao do DDD de 2 digitos opcional, aceitando numeros escritos com ou sem parenteses e espacos.
    *   \d{4,5}-?\d{4}: Aceita tanto numeros moveis (9 digitos) quanto fixos (8 digitos), com separador de hifen opcional.
*   Data (^\d{2}/\d{2}/\d{4}\$)
    *   \d{2}/\d{2}/\d{4}: Exige o formato padrao brasileiro Dia/Mes/Ano (DD/MM/AAAA) separado por barras longitudinais.

---

## Tratamento de Excecoes Aplicado

O software utiliza blocos estruturais try/except/else/finally para interceptar as seguintes anomalias de execucao:

1. FileNotFoundError: Capturado se o arquivo de dados indicado nao for localizado no diretorio corrente, evitando a interrupcao abrupta do programa.
2. KeyError: Disparado de forma controlada se o arquivo CSV lido nao apresentar as colunas obrigatorias declaradas no cabecalho (email, cpf, telefone, data).
3. ValueError: Capturado caso ocorram problemas na tipagem ou formatacao geral da estrutura do arquivo.
4. RegistroCorrompidoError (Excecao Personalizada): Criada estendendo a classe nativa Exception do Python. Ela intercepta regras de negocio criticas, atuando quando linhas inteiras de dados possuem campos vitais em branco, indicando que o arquivo de origem sofreu corrupcao fisica ou estrutural.

O uso do bloco else garante o isolamento da renderizacao do relatorio apenas sob condicoes normais de processamento, e o bloco finally atua encerrando a execucao de forma segura.

---

## Exemplos de Entrada e Saida

### Exemplo de Entrada (dados.csv)
```csv
email,cpf,telefone,data
joao@email.com,123.456.789-00,(11) 98888-7777,15/04/2024
maria_silva@empresa.org,98765432100,21977776666,02/11/2023
usuario-invalido.com,123.456,9999-9999,2024/12/31
```

### Exemplo de Saida Gerada no Terminal (Relatorio)
```text
=================================================================
            RELATORIO DE QUALIDADE E ANALISE DE DADOS            
=================================================================
 - Total de Registros Analisados : 3
 - Registros Validos             : 2
 - Registros com Inconsistencias : 1
 - Taxa de Integridade dos Dados : 66.67%
-----------------------------------------------------------------

[REGISTROS APROVADOS]:
 * joao@email.com           | CPF: 123.456.789-00  | Tel: (11) 98888-7777 | Data: 15/04/2024
 * maria_silva@empresa.org  | CPF: 98765432100     | Tel: 21977776666     | Data: 02/11/2023

[REGISTROS REJEITADOS / MOTIVOS]:
 * usuario-invalido.com     | Motivo: [E-mail Invalido, CPF Invalido, Data Invalida]
=================================================================

[FIM DA OPERACAO]: Rotina de processamento encerrada de forma segura.
```
