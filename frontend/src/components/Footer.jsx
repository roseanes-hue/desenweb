import React from 'react'

export default function Footer({ aoAbrirModalLeads }) {
  return (
    <footer className="bg-slate-950 text-slate-400 py-12 px-4 sm:px-6 lg:px-8 border-t border-slate-800/80">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6 text-center md:text-left">
        
        {/* Marca & Descrição */}
        <div className="space-y-1">
          <div className="flex items-center justify-center md:justify-start gap-2">
            <span className="text-xl">⚡</span>
            <span className="text-lg font-black text-white tracking-tight">AcademiStack Full Stack</span>
          </div>
          <p className="text-xs text-slate-400">
            Projeto Acadêmico para demonstração de arquitetura <strong className="text-sky-400">Python (FastAPI)</strong> + <strong className="text-cyan-400">React 18</strong> + <strong className="text-indigo-400">SQLite</strong>.
          </p>
        </div>

        {/* Badges & Atalho Modal */}
        <div className="flex flex-wrap items-center justify-center gap-3 text-xs">
          <span className="px-3 py-1.5 rounded-xl bg-slate-900 text-slate-300 border border-slate-800">
            Backend: Python / FastAPI
          </span>
          <span className="px-3 py-1.5 rounded-xl bg-slate-900 text-slate-300 border border-slate-800">
            Frontend: React 18 / Vite
          </span>
          <span className="px-3 py-1.5 rounded-xl bg-slate-900 text-slate-300 border border-slate-800">
            Banco: SQLite
          </span>
          <button
            onClick={aoAbrirModalLeads}
            className="px-3 py-1.5 rounded-xl bg-cyan-950 text-cyan-300 hover:bg-cyan-900 border border-cyan-500/30 transition font-bold"
          >
            🗄️ Ver Leads SQLite
          </button>
        </div>

      </div>

      <div className="max-w-7xl mx-auto border-t border-slate-900 mt-8 pt-6 text-center text-xs text-slate-600">
        &copy; 2026 AcademiStack. Desenvolvido para fins acadêmicos e educacionais.
      </div>
    </footer>
  )
}
