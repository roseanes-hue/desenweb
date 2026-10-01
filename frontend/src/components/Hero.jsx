import React, { useState } from 'react'

export default function Hero({ aoAbrirModalLeads }) {
  const [abaCodigo, setAbaCodigo] = useState('python')

  const snippetPython = `from fastapi import FastAPI, status
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="API Lead Capture")

class LeadSchema(BaseModel):
    nome_completo: str
    email: str
    telefone_whatsapp: str
    mensagem: str | None = None

@app.post("/api/leads", status_code=201)
def cadastrar_lead(lead: LeadSchema):
    # Processa sanitização e grava no SQLite
    return {"sucesso": True, "mensagem": "Lead salvo!"}`

  const snippetReact = `import { useState } from 'react'

export default function FormularioLead() {
  const [formData, setFormData] = useState({...})

  const enviarParaPython = async (e) => {
    e.preventDefault()
    const res = await fetch('/api/leads', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    })
    const data = await res.json()
    console.log("Resposta do FastAPI Python:", data)
  }
}`

  return (
    <section className="relative overflow-hidden bg-slate-950 py-20 lg:py-28 px-4 sm:px-6 lg:px-8 border-b border-slate-800/60">
      
      {/* Luzes decorativas de fundo (Orbs) */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[500px] bg-gradient-to-tr from-cyan-600/20 via-blue-600/20 to-purple-600/20 rounded-full blur-[120px] pointer-events-none animate-pulse-glow"></div>
      <div className="absolute top-10 right-10 w-96 h-96 bg-emerald-500/10 rounded-full blur-[100px] pointer-events-none"></div>

      <div className="max-w-7xl mx-auto grid lg:grid-cols-12 gap-12 lg:gap-8 items-center relative z-10">
        
        {/* Lado Esquerdo: Textos & CTAs */}
        <div className="lg:col-span-7 text-center lg:text-left space-y-6">
          
          {/* Badge Principal */}
          <div className="inline-flex items-center gap-2.5 px-4 py-2 rounded-full bg-slate-900/90 border border-slate-800 text-xs font-bold shadow-xl backdrop-blur-md">
            <span className="flex h-2.5 w-2.5 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
            <span className="text-slate-300">Arquitetura Moderna</span>
            <span className="text-slate-600">•</span>
            <span className="bg-gradient-to-r from-sky-400 to-cyan-400 bg-clip-text text-transparent font-extrabold">
              Backend Python + Frontend React
            </span>
          </div>

          {/* Título Principal Impactante */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-white tracking-tight leading-[1.1]">
            Backend poderoso em{' '}
            <span className="bg-gradient-to-r from-sky-400 via-cyan-400 to-indigo-400 bg-clip-text text-transparent underline decoration-cyan-500/40 decoration-wavy decoration-2">
              Python
            </span>
            ,<br /> Frontend reativo em{' '}
            <span className="bg-gradient-to-r from-cyan-400 via-teal-300 to-emerald-400 bg-clip-text text-transparent">
              React
            </span>
          </h1>

          {/* Subtítulo */}
          <p className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto lg:mx-0 leading-relaxed font-normal">
            Uma plataforma de alta performance desenvolvida para demonstrar na prática a integração fluida entre uma <strong>API RESTful em Python (FastAPI + Uvicorn + SQLite)</strong> e uma interface de usuário ultrarrápida construída com <strong>React 18, Vite e Tailwind CSS</strong>.
          </p>

          {/* Botões de Ação */}
          <div className="flex flex-wrap items-center justify-center lg:justify-start gap-4 pt-2">
            <a
              href="#formulario"
              className="px-8 py-4 rounded-2xl bg-gradient-to-r from-cyan-500 via-sky-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-extrabold text-base transition duration-300 shadow-xl shadow-cyan-500/25 hover:shadow-cyan-500/40 flex items-center gap-2 group"
            >
              <span>🐍 Testar Envio para API Python</span>
              <span className="group-hover:translate-x-1 transition-transform">➔</span>
            </a>

            <button
              onClick={aoAbrirModalLeads}
              className="px-6 py-4 rounded-2xl bg-slate-900 hover:bg-slate-800 text-slate-200 font-bold text-base border border-slate-800 hover:border-cyan-500/40 transition duration-300 flex items-center gap-2 shadow-inner"
            >
              <span>🗄️ Consultar Banco SQLite</span>
            </button>
          </div>

          {/* Badges de Tecnologias */}
          <div className="pt-6 border-t border-slate-900 flex flex-wrap items-center justify-center lg:justify-start gap-3 text-xs font-semibold text-slate-400">
            <span className="px-3 py-1.5 rounded-xl bg-slate-900/80 border border-slate-800 text-sky-300 flex items-center gap-1.5">
              🐍 Python 3.13
            </span>
            <span className="px-3 py-1.5 rounded-xl bg-slate-900/80 border border-slate-800 text-cyan-300 flex items-center gap-1.5">
              ⚡ FastAPI + Uvicorn
            </span>
            <span className="px-3 py-1.5 rounded-xl bg-slate-900/80 border border-slate-800 text-teal-300 flex items-center gap-1.5">
              ⚛️ React 18 (Vite)
            </span>
            <span className="px-3 py-1.5 rounded-xl bg-slate-900/80 border border-slate-800 text-blue-300 flex items-center gap-1.5">
              🗄️ SQLite WAL Mode
            </span>
          </div>

        </div>

        {/* Lado Direito: Preview Interativo de Código & Terminal */}
        <div className="lg:col-span-5">
          <div className="relative rounded-3xl p-1 bg-gradient-to-b from-slate-800 via-slate-900 to-slate-950 shadow-2xl border border-slate-800/80 glow-python">
            
            {/* Topbar do Card de Código */}
            <div className="bg-slate-950 px-5 py-3.5 rounded-t-[22px] flex items-center justify-between border-b border-slate-800/80">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-rose-500"></div>
                <div className="w-3 h-3 rounded-full bg-amber-500"></div>
                <div className="w-3 h-3 rounded-full bg-emerald-500"></div>
                <span className="ml-2 text-xs font-mono text-slate-400">
                  {abaCodigo === 'python' ? 'api/src/app.py' : 'frontend/Formulario.jsx'}
                </span>
              </div>

              {/* Trocador de Abas */}
              <div className="flex items-center bg-slate-900 p-1 rounded-xl border border-slate-800 text-xs">
                <button
                  onClick={() => setAbaCodigo('python')}
                  className={`px-3 py-1 rounded-lg font-bold transition ${
                    abaCodigo === 'python'
                      ? 'bg-sky-500 text-slate-950 shadow-sm'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  🐍 Python
                </button>
                <button
                  onClick={() => setAbaCodigo('react')}
                  className={`px-3 py-1 rounded-lg font-bold transition ${
                    abaCodigo === 'react'
                      ? 'bg-cyan-400 text-slate-950 shadow-sm'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  ⚛️ React
                </button>
              </div>
            </div>

            {/* Bloco de Código com Sintaxe Destacada */}
            <div className="bg-slate-950/90 p-5 rounded-b-[22px] font-mono text-xs text-slate-300 leading-relaxed overflow-x-auto">
              <pre className="text-slate-300">
                <code>
                  {abaCodigo === 'python' ? snippetPython : snippetReact}
                </code>
              </pre>
            </div>

            {/* Terminal Status Card */}
            <div className="mx-4 mb-4 p-3 rounded-2xl bg-slate-900/90 border border-slate-800 flex items-center justify-between text-xs font-mono">
              <div className="flex items-center gap-2 text-emerald-400 font-semibold">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                <span>STATUS 200 OK</span>
              </div>
              <span className="text-slate-400">FastAPI Uvicorn @ :3000</span>
            </div>

          </div>
        </div>

      </div>

    </section>
  )
}
