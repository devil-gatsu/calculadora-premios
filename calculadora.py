import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CalculadoraPremios(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Calculadora de Prêmios")
        # Janela super compacta, reduzida à metade da original e sem barra de rolagem
        self.geometry("420x520")
        self.resizable(False, False)

        self.rodape = ctk.CTkLabel(self, text="Criado por Matheus Carvalho", font=("Arial", 9), text_color="gray")
        self.rodape.pack(side="bottom", pady=2)

        self.tabview = ctk.CTkTabview(self, corner_radius=8)
        self.tabview.pack(padx=10, pady=0, fill="both", expand=True)

        self.aba_fianca = self.tabview.add("Cálculo Fiança")
        self.aba_vida = self.tabview.add("Cálculo Vida")

        # Dicionário para armazenar as referências de cada linha de resultado
        self.resultados_widgets = {}
        
        self.montar_aba_fianca()
        self.montar_aba_vida()

    def formatar_moeda(self, valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def converter_para_float(self, string_valor):
        try:
            limpo = string_valor.replace("R$", "").replace(".", "").replace(",", ".").strip()
            return float(limpo)
        except ValueError:
            return 0.0

    def copiar_valor(self, valor):
        # Limpa a área de transferência e injeta o valor exato
        self.clipboard_clear()
        self.clipboard_append(valor)
        self.update()

    def montar_aba_vida(self):
        lbl_construcao = ctk.CTkLabel(self.aba_vida, text="🚧 Em construção...", font=("Segoe UI", 18, "bold"), text_color="#F39C12")
        lbl_construcao.pack(expand=True)

    def montar_aba_fianca(self):
        # Frame de Entradas (Grid mais enxuto e compacto)
        f_in = ctk.CTkFrame(self.aba_fianca, fg_color="transparent")
        f_in.pack(fill="x", pady=5)

        self.e_tot_parc = ctk.CTkEntry(f_in, placeholder_text="Tot. Parc. Apólice", height=28)
        self.e_tot_parc.grid(row=0, column=0, padx=3, pady=3, sticky="ew")
        self.e_parc_pag = ctk.CTkEntry(f_in, placeholder_text="Parc. Pagas (2025)", height=28)
        self.e_parc_pag.grid(row=0, column=1, padx=3, pady=3, sticky="ew")

        self.e_prem_liq = ctk.CTkEntry(f_in, placeholder_text="Prêmio Líq. Parc.", height=28)
        self.e_prem_liq.grid(row=1, column=0, padx=3, pady=3, sticky="ew")
        self.e_prem_tot = ctk.CTkEntry(f_in, placeholder_text="Prêmio Tot. Parc.", height=28)
        self.e_prem_tot.grid(row=1, column=1, padx=3, pady=3, sticky="ew")
        f_in.grid_columnconfigure((0, 1), weight=1)

        btn_calc = ctk.CTkButton(self.aba_fianca, text="CALCULAR", height=30, font=("Segoe UI", 12, "bold"), command=self.calcular)
        btn_calc.pack(pady=5, fill="x", padx=3)

        # Frame de Resultados 
        f_out = ctk.CTkFrame(self.aba_fianca, fg_color="transparent")
        f_out.pack(fill="both", expand=True)

        def add_linha(chave, texto, cor, fonte):
            # Cria uma linha espremida para poupar espaço vertical
            linha = ctk.CTkFrame(f_out, fg_color="transparent", height=24)
            linha.pack(fill="x", pady=1)
            linha.pack_propagate(False) 
            
            lbl = ctk.CTkLabel(linha, text=f"{texto}: --", font=fonte, text_color=cor)
            lbl.pack(side="left")
            
            # Botão de cópia individual
            btn = ctk.CTkButton(linha, text="📋", width=26, height=20, font=("Segoe UI", 10), 
                                fg_color="#333", hover_color="#555")
            btn.pack(side="right")
            
            self.resultados_widgets[chave] = {"lbl": lbl, "btn": btn, "texto": texto}

        fonte_destaque = ("Segoe UI", 14, "bold")
        fonte_normal = ("Segoe UI", 12)

        # Inserindo todas as linhas
        add_linha("liq_atual", "Prêmio Líq. Atual", "#2ECC71", fonte_destaque)
        add_linha("tot", "Prêmio Total", "#3498DB", fonte_destaque)
        
        ctk.CTkFrame(f_out, height=1, fg_color="#444").pack(fill="x", pady=4)
        
        add_linha("qtd", "Qtd de Parcelas", "white", fonte_normal)
        add_linha("mid", "Parcela Inicial MID", "white", fonte_normal)
        add_linha("liq_apo", "Prêmio líq. apólice", "white", fonte_normal)
        add_linha("iof", "IOF (7,38%)", "white", fonte_normal)
        add_linha("tot_apo", "Prêmio total apólice", "white", fonte_normal)
        add_linha("dif", "Diferença de Prêmios", "white", fonte_normal)
        add_linha("iof_atual", "IOF atual", "white", fonte_normal)

    def atualizar_linha(self, chave, valor_str):
        # Atualiza o texto visual e embute o valor exato no botão de cópia
        w = self.resultados_widgets[chave]
        w["lbl"].configure(text=f"{w['texto']}: {valor_str}")
        w["btn"].configure(command=lambda v=valor_str: self.copiar_valor(v))

    def calcular(self):
        try:
            tot_parcelas = int(self.e_tot_parc.get() or 0)
            parc_pagas = int(self.e_parc_pag.get() or 0)
            p_liq_parc = self.converter_para_float(self.e_prem_liq.get())
            p_tot_parc = self.converter_para_float(self.e_prem_tot.get())

            # Devolve a formatação para os inputs
            self.e_prem_liq.delete(0, 'end')
            self.e_prem_liq.insert(0, self.formatar_moeda(p_liq_parc))
            self.e_prem_tot.delete(0, 'end')
            self.e_prem_tot.insert(0, self.formatar_moeda(p_tot_parc))

            # Cálculos
            qtd = tot_parcelas - parc_pagas
            mid = parc_pagas + 1
            liq_apo = p_liq_parc * qtd
            iof = (liq_apo * 7.38) / 100
            tot_apo = liq_apo + iof
            tot = p_tot_parc * qtd
            dif = tot - tot_apo
            liq_atual = liq_apo + dif
            iof_atual = tot - liq_atual

            # Atualiza os painéis visuais e os botões de copiar
            self.atualizar_linha("qtd", str(qtd))
            self.atualizar_linha("mid", str(mid))
            self.atualizar_linha("liq_apo", self.formatar_moeda(liq_apo))
            self.atualizar_linha("iof", self.formatar_moeda(iof))
            self.atualizar_linha("tot_apo", self.formatar_moeda(tot_apo))
            self.atualizar_linha("dif", self.formatar_moeda(dif))
            self.atualizar_linha("iof_atual", self.formatar_moeda(iof_atual))
            
            self.atualizar_linha("liq_atual", self.formatar_moeda(liq_atual))
            self.atualizar_linha("tot", self.formatar_moeda(tot))

        except Exception:
            self.resultados_widgets["liq_atual"]["lbl"].configure(text="Erro: Verifique os números preenchidos.")
            
if __name__ == "__main__":
    app = CalculadoraPremios()
    app.mainloop()
