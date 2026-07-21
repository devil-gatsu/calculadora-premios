import customtkinter as ctk

# Configurações de Design Deluxe
ctk.set_appearance_mode("dark")  # Modo escuro moderno
ctk.set_default_color_theme("blue")

class CalculadoraPremios(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela (Pequena e otimizada)
        self.title("Calculadora de Prêmios")
        self.geometry("450x700")
        self.resizable(False, False) # Impede redimensionamento para não quebrar o layout

        # Rodapé
        self.rodape = ctk.CTkLabel(self, text="Criado por Matheus Carvalho", font=("Arial", 10), text_color="gray")
        self.rodape.pack(side="bottom", pady=5)

        # Abas
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.pack(padx=20, pady=10, fill="both", expand=True)

        self.aba_fianca = self.tabview.add("Cálculo Fiança")
        self.aba_vida = self.tabview.add("Cálculo Vida")

        self.montar_aba_fianca()
        self.montar_aba_vida()

    def formatar_moeda(self, valor):
        # Formata float para padrão R$ 1.000,00
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def converter_para_float(self, string_valor):
        # Limpa a string digitada para converter em número
        try:
            limpo = string_valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
            return float(limpo)
        except ValueError:
            return 0.0

    def montar_aba_vida(self):
        lbl_construcao = ctk.CTkLabel(
            self.aba_vida, 
            text="🚧 Em construção...", 
            font=("Segoe UI", 24, "bold"),
            text_color="#F39C12"
        )
        lbl_construcao.pack(expand=True)

    def montar_aba_fianca(self):
        # --- Entradas (Inputs) ---
        frame_inputs = ctk.CTkFrame(self.aba_fianca, fg_color="transparent")
        frame_inputs.pack(fill="x", pady=10)

        # Linha 1: Parcelas
        self.ent_total_parcelas = ctk.CTkEntry(frame_inputs, placeholder_text="Total Parcelas Apólice")
        self.ent_total_parcelas.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.ent_parcelas_pagas = ctk.CTkEntry(frame_inputs, placeholder_text="Parcelas Pagas (2025)")
        self.ent_parcelas_pagas.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Linha 2: Prêmios
        self.ent_premio_liq = ctk.CTkEntry(frame_inputs, placeholder_text="Prêmio Líquido das Parcelas")
        self.ent_premio_liq.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        
        self.ent_premio_total_parc = ctk.CTkEntry(frame_inputs, placeholder_text="Prêmio Total das Parcelas")
        self.ent_premio_total_parc.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        frame_inputs.grid_columnconfigure((0, 1), weight=1)

        # Botão de Calcular com animação de hover nativa
        self.btn_calcular = ctk.CTkButton(
            self.aba_fianca, 
            text="CALCULAR", 
            font=("Segoe UI", 14, "bold"),
            height=40,
            command=self.calcular_fianca
        )
        self.btn_calcular.pack(pady=15, fill="x", padx=5)

        # --- Saídas (Outputs) ---
        self.frame_resultados = ctk.CTkScrollableFrame(self.aba_fianca, fg_color="transparent")
        self.frame_resultados.pack(fill="both", expand=True)

        # Destaques
        self.lbl_destaque_liq = ctk.CTkLabel(self.frame_resultados, text="Prêmio Líquido Atual: R$ 0,00", font=("Segoe UI", 18, "bold"), text_color="#2ECC71")
        self.lbl_destaque_liq.pack(pady=5, anchor="w")
        
        self.lbl_destaque_tot = ctk.CTkLabel(self.frame_resultados, text="Prêmio Total: R$ 0,00", font=("Segoe UI", 18, "bold"), text_color="#3498DB")
        self.lbl_destaque_tot.pack(pady=5, anchor="w")

        # Divisória
        ctk.CTkFrame(self.frame_resultados, height=2, fg_color="gray").pack(fill="x", pady=10)

        # Outros resultados
        font_res = ("Segoe UI", 13)
        self.lbl_qtd_parcelas = ctk.CTkLabel(self.frame_resultados, text="Qtd de Parcelas: 0", font=font_res)
        self.lbl_qtd_parcelas.pack(anchor="w")
        
        self.lbl_parc_inicial = ctk.CTkLabel(self.frame_resultados, text="Parcela Inicial MID: 0", font=font_res)
        self.lbl_parc_inicial.pack(anchor="w")
        
        self.lbl_premio_liq_apolice = ctk.CTkLabel(self.frame_resultados, text="Prêmio líquido apólice: R$ 0,00", font=font_res)
        self.lbl_premio_liq_apolice.pack(anchor="w")
        
        self.lbl_iof = ctk.CTkLabel(self.frame_resultados, text="IOF: R$ 0,00", font=font_res)
        self.lbl_iof.pack(anchor="w")
        
        self.lbl_premio_tot_apolice = ctk.CTkLabel(self.frame_resultados, text="Prêmio total apólice: R$ 0,00", font=font_res)
        self.lbl_premio_tot_apolice.pack(anchor="w")
        
        self.lbl_diferenca = ctk.CTkLabel(self.frame_resultados, text="Diferença de Prêmios: R$ 0,00", font=font_res)
        self.lbl_diferenca.pack(anchor="w")
        
        self.lbl_iof_atual = ctk.CTkLabel(self.frame_resultados, text="IOF atual: R$ 0,00", font=font_res)
        self.lbl_iof_atual.pack(anchor="w")

    def calcular_fianca(self):
        try:
            # Coleta de dados
            tot_parcelas = int(self.ent_total_parcelas.get() or 0)
            parc_pagas = int(self.ent_parcelas_pagas.get() or 0)
            premio_liq_parc = self.converter_para_float(self.ent_premio_liq.get())
            premio_tot_parc = self.converter_para_float(self.ent_premio_total_parc.get())

            # Formata os campos de entrada para manter o padrão R$ na tela
            self.ent_premio_liq.delete(0, 'end')
            self.ent_premio_liq.insert(0, self.formatar_moeda(premio_liq_parc))
            self.ent_premio_total_parc.delete(0, 'end')
            self.ent_premio_total_parc.insert(0, self.formatar_moeda(premio_tot_parc))

            # Cálculos exatos conforme solicitado
            qtd_parcelas = tot_parcelas - parc_pagas
            parc_inicial_mid = parc_pagas + 1
            
            premio_liq_apolice = premio_liq_parc * qtd_parcelas
            iof = (premio_liq_apolice * 7.38) / 100
            premio_tot_apolice = premio_liq_apolice + iof
            
            premio_total = premio_tot_parc * qtd_parcelas
            diferenca_premios = premio_total - premio_tot_apolice
            
            premio_liq_atual = premio_liq_apolice + diferenca_premios
            iof_atual = premio_total - premio_liq_atual

            # Atualização da Interface
            self.lbl_qtd_parcelas.configure(text=f"Qtd de Parcelas: {qtd_parcelas}")
            self.lbl_parc_inicial.configure(text=f"Parcela Inicial MID: {parc_inicial_mid}")
            
            self.lbl_premio_liq_apolice.configure(text=f"Prêmio líquido apólice: {self.formatar_moeda(premio_liq_apolice)}")
            self.lbl_iof.configure(text=f"IOF (7,38%): {self.formatar_moeda(iof)}")
            self.lbl_premio_tot_apolice.configure(text=f"Prêmio total apólice: {self.formatar_moeda(premio_tot_apolice)}")
            self.lbl_diferenca.configure(text=f"Diferença de Prêmios: {self.formatar_moeda(diferenca_premios)}")
            self.lbl_iof_atual.configure(text=f"IOF atual: {self.formatar_moeda(iof_atual)}")

            # Destaques
            self.lbl_destaque_liq.configure(text=f"Prêmio Líq. Atual: {self.formatar_moeda(premio_liq_atual)}")
            self.lbl_destaque_tot.configure(text=f"Prêmio Total: {self.formatar_moeda(premio_total)}")

        except Exception as e:
            self.lbl_destaque_tot.configure(text="Erro: Verifique os números", text_color="red")

if __name__ == "__main__":
    app = CalculadoraPremios()
    app.mainloop()
