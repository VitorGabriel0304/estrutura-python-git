from flask import Flask, render_template, request, url_for, flash

# cria a aplicação Flask
app = Flask(__name__)
app.secret_key = ""  # coloque qualquer texto aqui


# ------------------------------
# Página inicial
# ------------------------------

# GET: exibe o formulário
# POST: valida, calcula e renderiza os resultados
@app.route("/", methods=["GET", "POST"])
def index():

    dados_formulario = {}  # guarda o que o usuário digitou para re-popular em caso de erro

    if request.method == "POST":

        # --- coleta ---
        campo1_str = request.form.get("nome_do_campo1", "").strip()
        campo2_str = request.form.get("nome_do_campo2", "").strip()
        campo3_str = request.form.get("nome_do_campo3", "").strip()

        dados_formulario = {
            "nome_do_campo1": campo1_str,
            "nome_do_campo2": campo2_str,
            "nome_do_campo3": campo3_str,
        }

        # --- validação ---
        tem_erro = False

        if not campo1_str:
            flash("Campo 1 é obrigatório.", "danger")
            tem_erro = True
        else:
            try:
                campo1 = float(campo1_str.replace(",", "."))  # ou int()
                if campo1 <= 0:
                    flash("Campo 1 deve ser maior que zero.", "danger")
                    tem_erro = True
            except ValueError:
                flash("Campo 1 deve ser um número válido.", "danger")
                tem_erro = True
                campo1 = None

        if not campo2_str:
            flash("Campo 2 é obrigatório.", "danger")
            tem_erro = True
        else:
            try:
                campo2 = int(campo2_str)  # use int() para inteiros
                if campo2 <= 0:
                    flash("Campo 2 deve ser maior que zero.", "danger")
                    tem_erro = True
            except ValueError:
                flash("Campo 2 deve ser um número inteiro válido.", "danger")
                tem_erro = True
                campo2 = None

        if not campo3_str:
            flash("Campo 3 é obrigatório.", "danger")
            tem_erro = True
        else:
            try:
                campo3 = float(campo3_str.replace(",", "."))
                if campo3 < 0:
                    flash("Campo 3 não pode ser negativo.", "danger")
                    tem_erro = True
            except ValueError:
                flash("Campo 3 deve ser um número válido.", "danger")
                tem_erro = True
                campo3 = None

        # se houve erro volta ao formulário com os dados já digitados
        if tem_erro:
            return render_template("index.html", dados=dados_formulario)

        # --- cálculos ---
        resultado1 = campo1 * (campo3 / 100)   # ex.: valor_gorjeta = conta * (percentual / 100)
        resultado2 = campo1 + resultado1        # ex.: valor_total   = conta + gorjeta
        resultado3 = resultado2 / campo2        # ex.: por_pessoa    = total / pessoas

        # --- classificação ---
        # ajuste os valores e textos conforme o enunciado
        if campo3 < 5:
            classificacao = "Categoria A"
        elif campo3 <= 15:
            classificacao = "Categoria B"
        else:
            classificacao = "Categoria C"

        # --- monta dicionário e renderiza ---
        resultados = {
            "campo1_original": campo1,
            "campo2":          campo2,
            "campo3":          campo3,
            "resultado1":      resultado1,
            "resultado2":      resultado2,
            "resultado3":      resultado3,
            "classificacao":   classificacao,
        }

        return render_template("resultados.html", resultados=resultados)

    return render_template("index.html", dados=dados_formulario)



@app.route("/relatorios")
def relatorios():                       
    relatorios = [
        {"id": 1, "nome": "Item A", "valor": 100.50},
        {"id": 2, "nome": "Item B", "valor": 250.75},
        {"id": 3, "nome": "Item C", "valor": 75.20},
        {"id": 4, "nome": "Item D", "valor": 420.00},
    ]                                            
    return render_template("relatorios.html", relatorios=relatorios)



# ------------------------------
# Ponto de entrada
# ------------------------------

if __name__ == "__main__":
    app.run(debug=True)  # debug=True → reinicia ao salvar (nunca use em produção)