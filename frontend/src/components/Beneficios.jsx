import React from 'react'

const pilaresArquitetura = [
  {
    icone: '🐍',
    badge: 'Backend de Alta Performance',
    titulo: 'API RESTful em Python & FastAPI',
    subtitulo: 'Execução Assíncrona & Uvicorn',
    descricao: 'Backend reconstruído do zero em Python 3.13 com FastAPI. Oferece alta concorrência, roteamento declarativo, middlewares de CORS e respostas JSON sintonizadas.',
    corGlow: 'from-sky-500/20 to-blue-600/20',
    corBorda: 'border-sky-500/30 group-hover:border-sky-400',
    corBadge: 'bg-sky-950/80 text-sky-300 border-sky-500/30'
  },
  {
    icone: '⚛️',
    badge: 'Interface Reativa & Flutuante',
    titulo: 'Frontend em React 18 & Vite',
    subtitulo: 'Componentização & State Hooks',
    descricao: 'Interface de usuário construída com React 18 e Vite. Componentes modulares, hooks reativos para manipulação de formulários, máscaras e notificações fluídas.',
    corGlow: 'from-cyan-500/20 to-teal-500/20',
    corBorda: 'border-cyan-500/30 group-hover:border-cyan-400',
    corBadge: 'bg-cyan-950/80 text-cyan-300 border-cyan-500/30'
  },
  {
    icone: '🗄️',
    badge: 'Persistência Relacional Leve',
    titulo: 'Banco SQLite & WAL Mode',
    subtitulo: 'Consultas Preparadas & Performance',
    descricao: 'Integração direta com SQLite utilizando o módulo nativo de Python com suporte a Prepared Statements (consultas parametrizadas) e arquivo local landing.db.',
    corGlow: 'from-indigo-500/20 to-purple-500/20',
    corBorda: 'border-indigo-500/30 group-hover:border-indigo-400',
    corBadge: 'bg-indigo-950/80 text-indigo-300 border-indigo-500/30'
  },
  {
    icone: '🛡️',
    badge: 'Segurança & Integridade',
    titulo: 'Sanitização & Validação Pydantic',
    subtitulo: 'Proteção XSS e Máscara Dinâmica',
    descricao: 'Sanitização estrita contra scripts maliciosos (HTML escaping), validação precisa de e-mail e extração de dígitos telefônicos com formatação automática.',
    corGlow: 'from-emerald-500/20 to-teal-500/20',
    corBorda: 'border-emerald-500/30 group-hover:border-emerald-400',
    corBadge: 'bg-emerald-950/80 text-emerald-300 border-emerald-500/30'
  }
]

export default function Beneficios() {
  return (
    <section id="tecnologias" className="py-24 px-4 sm:px-6 lg:px-8 bg-slate-950 relative overflow-hidden">
      
      {/* Grade decorativa de fundo */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b15_1px,transparent_1px),linear-gradient(to_bottom,#1e293b15_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_50%,#000_70%,transparent_100%)] pointer-events-none"></div>

      <div className="max-w-7xl mx-auto relative z-10">
        
        {/* Cabeçalho da Seção */}
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900 text-cyan-400 text-xs font-extrabold uppercase tracking-widest border border-slate-800 shadow-md">
            <span>⚡ Arquitetura da Aplicação</span>
          </span>

          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black text-white tracking-tight">
            Por que o combo <span className="bg-gradient-to-r from-sky-400 to-cyan-400 bg-clip-text text-transparent">Python</span> + <span className="bg-gradient-to-r from-cyan-400 to-emerald-400 bg-clip-text text-transparent">React</span> é imbatível?
          </h2>

          <p className="text-slate-400 text-base sm:text-lg leading-relaxed">
            Uma combinação perfeita de robustez no servidor e dinamismo no cliente. Entenda como cada pilar contribui para a experiência completa do sistema.
          </p>
        </div>

        {/* Grid de Cards dos Pilares */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {pilaresArquitetura.map((item, index) => (
            <div
              key={index}
              className={`group relative rounded-3xl p-7 bg-slate-900/60 backdrop-blur-xl border ${item.corBorda} transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl flex flex-col justify-between overflow-hidden`}
            >
              {/* Efeito de brilho de fundo no hover */}
              <div className={`absolute -inset-px bg-gradient-to-br ${item.corGlow} opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none rounded-3xl`}></div>

              <div className="relative z-10 space-y-5">
                
                {/* Ícone & Badge */}
                <div className="flex items-center justify-between">
                  <div className="w-14 h-14 rounded-2xl bg-slate-800/90 border border-slate-700/80 flex items-center justify-center text-3xl shadow-lg group-hover:scale-110 transition-transform">
                    {item.icone}
                  </div>
                  <span className={`text-[10px] font-extrabold px-2.5 py-1 rounded-full border ${item.corBadge}`}>
                    {item.badge}
                  </span>
                </div>

                {/* Título & Subtítulo */}
                <div>
                  <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">
                    {item.subtitulo}
                  </span>
                  <h3 className="text-xl font-bold text-white tracking-tight group-hover:text-cyan-300 transition-colors">
                    {item.titulo}
                  </h3>
                </div>

                {/* Descrição */}
                <p className="text-slate-300 text-sm leading-relaxed">
                  {item.descricao}
                </p>
              </div>

              {/* Detalhe no rodapé do card */}
              <div className="relative z-10 pt-6 mt-6 border-t border-slate-800/80 flex items-center justify-between text-xs font-mono text-slate-400">
                <span>Stack Item #0{index + 1}</span>
                <span className="group-hover:translate-x-1 transition-transform text-cyan-400 font-bold">➔</span>
              </div>

            </div>
          ))}
        </div>

      </div>
    </section>
  )
}
