import React, { useState } from 'react'
import Header from './components/Header'
import Hero from './components/Hero'
import Beneficios from './components/Beneficios'
import FormularioLead from './components/FormularioLead'
import ModalLeads from './components/ModalLeads'
import Toast from './components/Toast'
import Footer from './components/Footer'

export default function App() {
  const [toastState, setToastState] = useState({
    mensagem: '',
    tipo: 'sucesso',
    visivel: false
  })

  const [modalLeadsAberto, setModalLeadsAberto] = useState(false)

  const exibirToastSucesso = (mensagem) => {
    setToastState({ mensagem, tipo: 'sucesso', visivel: true })
  }

  const exibirToastErro = (mensagem) => {
    setToastState({ mensagem, tipo: 'erro', visivel: true })
  }

  const fecharToast = () => {
    setToastState(prev => ({ ...prev, visivel: false }))
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 selection:bg-cyan-500 selection:text-white">
      <Header aoAbrirModalLeads={() => setModalLeadsAberto(true)} />
      
      <main className="flex-1">
        <Hero aoAbrirModalLeads={() => setModalLeadsAberto(true)} />
        <Beneficios />
        <FormularioLead
          emSucesso={exibirToastSucesso}
          emErro={exibirToastErro}
          aoAbrirModalLeads={() => setModalLeadsAberto(true)}
        />
      </main>

      <Footer aoAbrirModalLeads={() => setModalLeadsAberto(true)} />

      <ModalLeads
        aberto={modalLeadsAberto}
        aoFechar={() => setModalLeadsAberto(false)}
      />

      <Toast
        mensagem={toastState.mensagem}
        tipo={toastState.tipo}
        visivel={toastState.visivel}
        aoFechar={fecharToast}
      />
    </div>
  )
}
