import React, { useState } from 'react'

export default function FormularioLead({ emSucesso, emErro, aoAbrirModalLeads }) {
  const [formData, setFormData] = useState({
    nome_completo: '',
    email: '',
    telefone_whatsapp: '',
    mensagem: ''
  })
  const [carregando, setCarregando] = useState(false)

  // Máscara dinâmica de telefone WhatsApp (xx) xxxxx-xxxx
  const tratarMascaraTelefone = (valor) => {
    let digitos = valor.replace(/\D/g, '').slice(0, 11)
    if (digitos.length > 2) digitos = `(${digitos.slice(0, 2)}) ${digitos.slice(2)}`
    if (digitos.length > 10) digitos = `${digitos.slice(0, 10)}-${digitos.slice(10)}`
    return digitos
  }

  const aoMudarInput = (e) => {
    const { name, value } = e.target
    if (name === 'telefone_whatsapp') {
      setFormData(prev => ({ ...prev, [name]: tratarMascaraTelefone(value) }))
    } else {
      setFormData(prev => ({ ...prev, [name]: value }))
    }
  }

  const aoSubmeter = async (e) => {
    e.preventDefault()
    if (carregando) return

    setCarregando(true)

    try {
      const resposta = await fetch('/api/leads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          nome_completo: formData.nome_completo.trim(),
          email: formData.email.trim(),
          telefone_whatsapp: formData.telefone_whatsapp,
          mensagem: formData.mensagem.trim()
        })
      })

      const resultado = await resposta.json()

      if (resultado.sucesso) {
        emSucesso(resultado.mensagem || 'Lead cadastrado com sucesso no servidor Python (FastAPI)!')
        setFormData({
          nome_completo: '',
          email: '',
          telefone_whatsapp: '',
          mensagem: ''
        })
      } else {
        const msg = resultado.erros ? resultado.erros.join(' ') : resultado.mensagem
        emErro(msg || 'Erro de validação retornado pela API Python.')
      }
    } catch (err) {
      emErro('Não foi possível se conectar à API Python em http://localhost:3000.')
    } finally {
      setCarregando(false)
    }
  }

  return (
    <section id="formulario" className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-950 relative overflow-hidden">
      
      {/* Glow de fundo */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-gradient-to-r from-sky-600/10 via-cyan-600/10 to-indigo-600/10 rounded-full blur-[100px] pointer-events-none"></div>

      <div className="max-w-3xl mx-auto relative z-10">
        
        {/* Cabeçalho */}
        <div className="text-center mb-12 space-y-3">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-xs font-bold text-sky-400">
            <span>🐍 Teste de Integração Real-Time</span>
          </div>

          <h2 className="text-3xl sm:text-4xl font-black text-white tracking-tight">
            Envie um Lead para o Backend <span className="bg-gradient-to-r from-sky-400 to-cyan-400 bg-clip-text text-transparent">Python</span>
          </h2>

          <p className="text-slate-400 text-sm sm:text-base max-w-xl mx-auto">
            Preencha os campos do formulário reativo em <strong>React 18</strong> para disparar uma requisição POST assíncrona ao servidor <strong>FastAPI em Python</strong>.
          </p>
        </div>

        {/* Card do Formulário */}
        <form
          onSubmit={aoSubmeter}
          className="bg-slate-900/80 backdrop-blur-2xl p-8 sm:p-10 rounded-3xl border border-slate-800 shadow-2xl space-y-6 relative overflow-hidden glow-python"
          noValidate
        >
          {/* Header do Card */}
          <div className="flex items-center justify-between pb-6 border-b border-slate-800">
            <div className="flex items-center gap-3">
              <span className="w-3 h-3 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="text-xs font-mono text-slate-300">Endpoint: POST /api/leads</span>
            </div>
            <span className="text-xs font-mono text-slate-500 hidden sm:block">Porta: 3000 (Uvicorn)</span>
          </div>

          {/* Campo Nome Completo */}
          <div>
            <label htmlFor="nome_completo" className="block text-xs font-bold uppercase text-slate-300 tracking-wider mb-2">
              Nome Completo (Aluno / Avaliador) *
            </label>
            <input
              type="text"
              id="nome_completo"
              name="nome_completo"
              required
              minLength={3}
              maxLength={150}
              placeholder="Ex: Carlos David"
              value={formData.nome_completo}
              onChange={aoMudarInput}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3.5 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition text-sm font-medium"
            />
          </div>

          {/* Grid E-mail & Telefone */}
          <div className="grid sm:grid-cols-2 gap-6">
            <div>
              <label htmlFor="email" className="block text-xs font-bold uppercase text-slate-300 tracking-wider mb-2">
                E-mail de Contato *
              </label>
              <input
                type="email"
                id="email"
                name="email"
                required
                placeholder="dev@exemplo.com"
                value={formData.email}
                onChange={aoMudarInput}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3.5 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition text-sm font-medium"
              />
            </div>

            <div>
              <label htmlFor="telefone_whatsapp" className="block text-xs font-bold uppercase text-slate-300 tracking-wider mb-2">
                Telefone WhatsApp (com DDD) *
              </label>
              <input
                type="tel"
                id="telefone_whatsapp"
                name="telefone_whatsapp"
                required
                maxLength={15}
                placeholder="(11) 99999-8888"
                value={formData.telefone_whatsapp}
                onChange={aoMudarInput}
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3.5 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition text-sm font-medium font-mono"
              />
            </div>
          </div>

          {/* Mensagem Opcional */}
          <div>
            <label htmlFor="mensagem" className="block text-xs font-bold uppercase text-slate-300 tracking-wider mb-2">
              Mensagem ou Avaliação do Projeto (Opcional)
            </label>
            <textarea
              id="mensagem"
              name="mensagem"
              rows={3}
              maxLength={500}
              placeholder="Escreva um comentário sobre o backend em Python ou o frontend em React..."
              value={formData.mensagem}
              onChange={aoMudarInput}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3.5 text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition text-sm font-medium resize-none"
            ></textarea>
          </div>

          {/* Botão de Envio */}
          <button
            type="submit"
            disabled={carregando}
            className="w-full bg-gradient-to-r from-cyan-500 via-sky-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-extrabold py-4 px-6 rounded-xl transition duration-300 shadow-xl shadow-cyan-500/25 flex items-center justify-center gap-3 disabled:opacity-60 disabled:cursor-not-allowed text-base tracking-wide"
          >
            <span>{carregando ? 'Processando na API Python...' : '🐍 Enviar Lead para o Backend Python'}</span>
            {carregando && (
              <span className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            )}
          </button>

          {/* Botão Secundário para Consultar Leads */}
          <div className="pt-2 text-center">
            <button
              type="button"
              onClick={aoAbrirModalLeads}
              className="text-xs text-slate-400 hover:text-cyan-400 underline font-semibold transition inline-flex items-center gap-1.5"
            >
              <span>🔍 Clique para ver a lista de Leads cadastrados no SQLite</span>
            </button>
          </div>

        </form>

      </div>
    </section>
  )
}
