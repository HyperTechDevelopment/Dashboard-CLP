from datetime import datetime
from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import sqlite3

app = Flask(__name__)


def get_data(
    start_date=None, end_date=None, turno=None, modelo=None, exclude_duplicates=False
):
    conn = sqlite3.connect(
        r"INSIRA O CAMINHO DO BANCO AQUI."
    )

    if not start_date:
        start_date = datetime.now().strftime("%Y-%m-%d")
    if not end_date:
        end_date = start_date

    params = [start_date, end_date]
    extra_conditions = []

    if turno:
        extra_conditions.append("turno = ?")
        params.append(turno)
    if modelo:
        extra_conditions.append("modelo = ?")
        params.append(modelo)

    where_conditions = " AND ".join(extra_conditions)

    distinct_clause = "DISTINCT" if exclude_duplicates else ""
    case_clause = (
        f"CASE WHEN serial LIKE 'SN%' THEN serial ELSE {distinct_clause} serial END"
    )

    query = f"""
        SELECT linha_solicitante, COUNT({case_clause}) AS quantidade
        FROM lavagem_placas
        WHERE data BETWEEN ? AND ? {f'AND {where_conditions}' if where_conditions else ''}
        GROUP BY linha_solicitante
        ORDER BY quantidade DESC
    """

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


def create_figure(df, title):
    fig = px.bar(
        df,
        x="linha_solicitante",
        y="quantidade",
        color="quantidade",
        labels={
            "linha_solicitante": "Linhas SMT",
            "quantidade": "Quantidade",
        },  # Altere aqui
        title=title,
        color_continuous_scale=px.colors.sequential.Viridis,
    )
    fig.update_layout(
        autosize=False,
        width=2300,
        height=660,
        title_x=0.5,
        title_font_size=25,
        showlegend=False,
        xaxis=dict(
            title="Linhas SMT", title_font=dict(size=20), tickfont=dict(size=18)
        ),
        yaxis=dict(  # Adicione este bloco
            title="Quantidade",  
            title_font=dict(size=14),
            tickfont=dict(size=18),
        ),
    )
    fig.update_traces(
        texttemplate="%{y}", textposition="outside", textfont=dict(size=18)
    )
    return fig.to_html()


def get_turnos():
    conn = sqlite3.connect(
        r"INSIRA O CAMINHO DO BANCO AQUI."
    )
    turnos = pd.read_sql_query("SELECT DISTINCT turno FROM lavagem_placas", conn)
    conn.close()
    return turnos["turno"].tolist()


def get_modelos():
    conn = sqlite3.connect(
        r"INSIRA O CAMINHO DO BANCO AQUI."
    )
    modelos = pd.read_sql_query("SELECT DISTINCT modelo FROM lavagem_placas", conn)
    conn.close()
    return modelos["modelo"].tolist()


@app.route("/", methods=["GET", "POST"])
def dashboard():
    # Inicializa variáveis
    selected_date = request.form.get("date-filter")
    start_date = request.form.get("start-date")
    end_date = request.form.get("end-date")
    turno = request.form.get("turno")
    modelo = request.form.get("modelo")
    action = request.form.get("action", "single-date")
    exclude_duplicates = "exclude_duplicates" in request.form

    # Determina as datas formatadas
    formatted_date = (
        datetime.now().strftime("%d/%m/%Y")
        if not selected_date
        else datetime.strptime(selected_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    )
    formatted_start_date = (
        formatted_date
        if not start_date
        else datetime.strptime(start_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    )
    formatted_end_date = (
        formatted_date
        if not end_date
        else datetime.strptime(end_date, "%Y-%m-%d").strftime("%d/%m/%Y")
    )

    # Obtém os dados baseados na seleção do usuário
    df = get_data(
        formatted_start_date, formatted_end_date, turno, modelo, exclude_duplicates
    )

    # Atualiza o título com base nas seleções do usuário
    title_parts = ["Quantidade de Seriais"]
    if turno:
        title_parts.append(f"do {turno} Turno")
    if modelo:
        title_parts.append(f"do Modelo {modelo}")
    if action == "single-date":
        title_parts.append(f"da Data {formatted_date}")
    elif action == "date-range":
        title_parts.append(
            f"Entre os Dias {formatted_start_date} e {formatted_end_date}"
        )
    if exclude_duplicates:
        title_parts.append("(Duplicatas Excluídas)")

    title = " ".join(title_parts)

    # Prepara o HTML do gráfico
    graph_html = create_figure(df, title)
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Obtém os dados para os filtros de turno e modelo
    turnos = get_turnos()
    modelos = get_modelos()

    # Renderiza o template HTML passando as variáveis necessárias
    return render_template(
        "dashboard.html",
        graph_html=graph_html,
        current_date=current_date,
        turnos=turnos,
        modelos=modelos,
        selected_date=selected_date,
        start_date=start_date,
        end_date=end_date,
        turno_selecionado=turno,
        modelo_selecionado=modelo,
        exclude_duplicates=exclude_duplicates,
    )


if __name__ == "__main__":
    app.run(debug=True)
