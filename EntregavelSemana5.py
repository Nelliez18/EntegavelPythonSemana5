import os
import re
import csv

# --- EXCECOES PERSONALIZADAS (Regras de Negocio) ---

class RegistroCorrompidoError(Exception):
    """Excecao lancada quando uma linha do arquivo possui dados ausentes."""
    def __init__(self, mensagem="O registro possui dados ausentes ou estrutura corrompida."):
        self.mensagem = mensagem
        super().__init__(self.mensagem)



# --- FUNCOES DE VALIDACAO COM EXPRESSOES REGULARES (REGEX) ---


def validar_email(email):
    padrao = r"^[\w.-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(padrao, email.strip()))

def validar_cpf(cpf):
    cpf_limpo = re.sub(r"\D", "", cpf)
    padrao = r"^\d{11}$"
    return bool(re.match(padrao, cpf_limpo))

def validar_telefone(telefone):
    padrao = r"^(\(?\d{2}\)?\s?)?\d{4,5}-?\d{4}$"
    return bool(re.match(padrao, telefone.strip()))

def validar_data(data):
    padrao = r"^\d{2}/\d{2}/\d{4}$"
    return bool(re.match(padrao, data.strip()))



# ---FUNCAO PRINCIPAL DE ANALISE DE DADOS ---


def analisar_arquivo_dados(caminho_arquivo):
    dados_validos = []
    dados_invalidos = []
    
    total_registros = 0
    total_validos = 0
    total_invalidos = 0

    print(f"Iniciando a leitura do arquivo: {caminho_arquivo}")

    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            
            if not leitor.fieldnames:
                raise ValueError("O arquivo esta vazio ou sem cabecalho.")
            
            colunas_obrigatorias = ["email", "cpf", "telefone", "data"]
            for col in colunas_obrigatorias:
                if col not in leitor.fieldnames:
                    raise KeyError(f"A coluna obrigatoria '{col}' nao foi encontrada.")

            for linha in leitor:
                total_registros += 1
                
                if not linha["email"] or not list(linha.values()):
                    raise RegistroCorrompidoError(f"Erro na linha {total_registros + 1}: Dados ausentes.")

                email_ok = validar_email(linha["email"])
                cpf_ok = validar_cpf(linha["cpf"])
                telefone_ok = validar_telefone(linha["telefone"])
                data_ok = validar_data(linha["data"])

                registro_processado = {
                    "dados": linha,
                    "status": {"email": email_ok, "cpf": cpf_ok, "telefone": telefone_ok, "data": data_ok}
                }

                if email_ok and cpf_ok and telefone_ok and data_ok:
                    dados_validos.append(registro_processado)
                    total_validos += 1
                else:
                    dados_invalidos.append(registro_processado)
                    total_invalidos += 1

    except FileNotFoundError:
        print(f"[ERRO]: O arquivo '{caminho_arquivo}' nao foi encontrado.")
    except ValueError as e:
        print(f"[ERRO DE VALOR]: Falha no processamento. Detalhes: {e}")
    except KeyError as e:
        print(f"[ERRO DE COLUNA]: A estrutura do arquivo CSV esta invalida. {e}")
    except RegistroCorrompidoError as e:
        print(f"[ERRO DE NEGOCIO]: {e.mensagem}")

    else:
        print("Arquivo processado com sucesso!")
        
        # --- GERADOR DE RELATORIO LIMPO ---
        print("\n" + "-"*65)
        print(f"{'RELATORIO DE QUALIDADE E ANALISE DE DADOS':^65}")
        print("-"*65)
        
        print(f"   Total de Registros Analisados : {total_registros}")
        print(f"   Registros Validos             : {total_validos}")
        print(f"   Registros com Inconsistencias : {total_invalidos}")
        if total_registros > 0:
            print(f"   Taxa de Integridade dos Dados : {(total_validos / total_registros) * 100:.2f}%")
        print("-"*65)

        print("\n[REGISTROS APROVADOS]:")
        for item in dados_validos:
            d = item["dados"]
            print(f" * {d['email']:<25} | CPF: {d['cpf']:<14} | Tel: {d['telefone']:<15} | Data: {d['data']}")

        print("\n[REGISTROS REJEITADOS E MOTIVOS]:")
        for item in dados_invalidos:
            d = item["dados"]
            st = item["status"]
            
            erros = []
            if not st["email"]: erros.append("E-mail Invalido")
            if not st["cpf"]: erros.append("CPF Invalido")
            if not st["telefone"]: erros.append("Telefone Invalido")
            if not st["data"]: erros.append("Data Invalida")
            
            motivo = ", ".join(erros)
            print(f" * {d['email'] or 'Vazio':<25} | Motivo: [{motivo}]")
            
        print("-"*65)

    finally:
        print("\n[FIM DA OPERACAO]: Rotina de processamento encerrada de forma segura.")

# --- AMBIENTE DE EXECUCAO AUTOMATIZADO ---
if __name__ == "__main__":
    nome_arquivo_teste = "dados.csv"

    if not os.path.exists(nome_arquivo_teste):
        print(f"Criando arquivo de teste '{nome_arquivo_teste}'...")
        with open(nome_arquivo_teste, mode='w', encoding='utf-8', newline='') as f:
            escritor = csv.writer(f)
            escritor.writerow(["email", "cpf", "telefone", "data"])
            escritor.writerow(["joao@email.com", "123.456.789-00", "(11) 98888-7777", "15/04/2024"])
            escritor.writerow(["maria_silva@empresa.org", "98765432100", "21977776666", "02/11/2023"])
            escritor.writerow(["usuario-invalido.com", "123.456", "9999-9999", "2024/12/31"])

    analisar_arquivo_dados(nome_arquivo_teste)
