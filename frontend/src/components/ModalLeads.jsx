import React, { useState, useEffect } from 'react'

export default function ModalLeads({ aberto, aoFechar }) {
  const [leads, setLeads] = useState([])
  const [total, setTotal] = useState(0)
  const [carregando, setCarregando] = useState(false)
  const [erro, setErro] = useState('')

  const carregarLeads = async () => {
    setCarregando(true)
    setErro('')
    try {
      const res = await fetch('/api/leads?pagina=1&limite=50')
      const data = await res.json()
      if (data.sucesso) {
        setLeads(data.dados || [])
        setTotal(data.total || 0)
      } else {
        setErro('Erro ao carregar dados do SQLite.')
      }
    } catch {
      setErro('Erro ao se conectar com a API Python em /api/leads.')
    } finally {
      setCarregando(false)
    }
  }

  useEffect(() => {
    if (aberto) {
      carregarLeads()
    }
  }, [aberto])

  if (!aberto) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in">
      <div className="bg-slate-900 border border-slate-800 rounded-3xl w-full max-w-4xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden glow-python">
        
        {/* Header do Modal */}
        <div className="p-6 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-sky-950 border border-sky-500/30 flex items-center justify-center text-xl">
              🗄️
            </div>
            <div>
              <h3 className="text-lg font-black text-white flex items-center gap-2">
                Leads no Banco SQLite <span className="text-xs px-2.5 py-0.5 rounded-full bg-sky-900/60 text-sky-300 font-mono border border-sky-500/30">{total} Registros</span>
              </h3>
              <p className="text-xs text-slate-400">
                Dados retornados ao vivo pela API Python FastAPI (`GET /api/leads`)
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={carregarLeads}
              disabled={carregando}
              className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 transition flex items-center gap-1"
              title="Atualizar dados"
            >
              <span>🔄</span>
              <span className="hidden sm:inline">Atualizar</span>
            </button>

            <button
              onClick={aoFechar}
              className="p-2 rounded-xl bg-slate-800 hover:bg-rose-950 hover:text-rose-300 text-slate-400 transition"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Conteúdo da Tabela */}
        <div className="p-6 overflow-y-auto flex-1 font-mono text-xs space-y-4">
          
          {carregando && (
            <div className="py-12 text-center text-slate-400 space-y-3">
              <div className="w-8 h-8 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin mx-auto"></div>
              <p>Consultando banco SQLite via Python...</p>
            </div>
          )}

          {erro && (
            <div className="p-4 rounded-xl bg-rose-950/80 border border-rose-800 text-rose-300 text-center">
              {erro}
            </div>
          )}

          {!carregando && !erro && leads.length === 0 && (
            <div className="py-12 text-center text-slate-500">
              Nenhum lead cadastrado ainda no banco de dados SQLite.
            </div>
          )}

          {!carregando && !erro && leads.length > 0 && (
            <div className="overflow-x-auto rounded-2xl border border-slate-800">
              <table className="w-full text-left text-slate-300">
                <thead className="bg-slate-950 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                  <tr>
                    <th className="py-3.5 px-4"># ID</th>
                    <th className="py-3.5 px-4">Nome Completo</th>
                    <th className="py-3.5 px-4">E-mail</th>
                    <th className="py-3.5 px-4">WhatsApp</th>
                    <th className="py-3.5 px-4">Data Cadastro</th>
                    <th className="py-3.5 px-4">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 bg-slate-900/40">
                  {leads.map((lead) => (
                    <tr key={lead.id} className="hover:bg-slate-800/40 transition">
                      <td className="py-3 px-4 text-cyan-400 font-bold">#{lead.id}</td>
                      <td className="py-3 px-4 font-sans font-medium text-white">{lead.nome_completo}</td>
                      <td className="py-3 px-4 text-slate-300">{lead.email}</td>
                      <td className="py-3 px-4 text-slate-300">{lead.telefone_whatsapp}</td>
                      <td className="py-3 px-4 text-slate-400">{lead.data_cadastro}</td>
                      <td className="py-3 px-4">
                        <span className="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase bg-emerald-950 text-emerald-400 border border-emerald-500/30">
                          {lead.status_atendimento || 'novo'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

        </div>

        {/* Rodapé do Modal */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/60 text-right">
          <button
            onClick={aoFechar}
            className="px-6 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition"
          >
            Fechar Visualização
          </button>
        </div>

      </div>
    </div>
  )
}
