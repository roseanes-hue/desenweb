from fastapi import Response, status
from fastapi.responses import JSONResponse
from ..config.conexao_banco import obter_conexao
from ..utilitarios.validadores import validar_lead

def cadastrar_lead_controlador(payload: dict):
    resultado = validar_lead(payload)
    if not resultado['valido']:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                'sucesso': False,
                'mensagem': 'Falha na validação dos dados.',
                'erros': resultado['erros']
            }
        )

    dados = resultado['dados']
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        cursor.execute(
            'INSERT INTO leads (nome_completo, email, telefone_whatsapp, mensagem) VALUES (?, ?, ?, ?)',
            (dados['nome_completo'], dados['email'], dados['telefone_whatsapp'], dados['mensagem'])
        )
        conexao.commit()
    except Exception:
        conexao.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'sucesso': False,
                'mensagem': 'Erro interno ao salvar dados. Tente novamente.'
            }
        )
    finally:
        conexao.close()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            'sucesso': True,
            'mensagem': 'Dados recebidos e salvos com sucesso.'
        }
    )

def listar_leads_controlador(pagina: int = 1, limite: int = 20):
    if pagina < 1:
        pagina = 1
    if limite < 1:
        limite = 20

    offset = (pagina - 1) * limite
    conexao = obter_conexao()
    try:
        cursor = conexao.cursor()
        cursor.execute('SELECT COUNT(*) AS total FROM leads')
        row_total = cursor.fetchone()
        total = row_total['total'] if row_total else 0

        cursor.execute(
            'SELECT id, nome_completo, email, telefone_whatsapp, data_cadastro, status_atendimento FROM leads ORDER BY data_cadastro DESC LIMIT ? OFFSET ?',
            (limite, offset)
        )
        leads = cursor.fetchall()
    except Exception:
        return {
            'sucesso': False,
            'erros': ['Erro interno ao listar leads.']
        }
    finally:
        conexao.close()

    return {
        'sucesso': True,
        'dados': leads,
        'total': total,
        'pagina': pagina,
        'limite': limite
    }
