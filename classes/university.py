from classes.gclass import Gclass
import datetime
import plotly.graph_objects as go
import pandas as pd
import sqlite3
import webbrowser
import os
from pathlib import Path


class University(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id', '_name', '_creation_date']
    header = 'Universities'
    des = ['Id', 'Name', 'Date of Creation']

    def __init__(self, id, name, creation_date):
        super().__init__()

        id = University.get_id(id)

        self._id = id
        self._name = name
        self._creation_date = datetime.datetime.strptime(
            creation_date, "%d/%m/%Y"
        ).date()

        University.obj[id] = self
        University.lst.append(id)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, creation_date):
        self._creation_date = creation_date

    @property
    def age(self):
        tday = datetime.date.today()
        age = tday.year - self.creation_date.year

        if tday.month < self.creation_date.month or \
           (tday.month == self.creation_date.month and tday.day < self.creation_date.day):
            age -= 1

        return age

    @classmethod
    def gerar_treemap_labs_detalhado(cls):
        """Gera um treemap hierárquico mostrando universidades com pelo menos 1 lab e os respetivos labs"""
        try:
            base_dir = Path(__file__).resolve().parent.parent
            db_path = base_dir / "data" / "g22_db.db"
            html_path = base_dir / "treemap_labs_detalhado.html"
    
            def formatar_nome_universidade(nome):
                """Se o nome tiver mais de 2 palavras, divide em linhas."""
                palavras = str(nome).split()
    
                if len(palavras) <= 2:
                    return nome
    
                linhas = []
                for i in range(0, len(palavras), 2):
                    linha = " ".join(palavras[i:i + 2])
                    linhas.append(linha)
    
                return "<br>".join(linhas)
    
            conn = sqlite3.connect(str(db_path))
    
            query_universidades = """
            SELECT 
                u.university_id,
                u.name AS Universidade,
                COUNT(l.lab_id) AS Quantidade_Labs
            FROM University u
            LEFT JOIN Lab l 
                ON u.university_id = l.university_id
            GROUP BY u.university_id, u.name
            HAVING COUNT(l.lab_id) > 0
            ORDER BY Quantidade_Labs DESC, u.name ASC
            """
    
            df_universidades = pd.read_sql_query(query_universidades, conn)
    
            query_labs = """
            SELECT 
                u.university_id,
                u.name AS Universidade,
                l.lab_id,
                l.extra_info AS Lab_Info
            FROM Lab l
            JOIN University u 
                ON l.university_id = u.university_id
            ORDER BY u.name, l.lab_id
            """
    
            df_labs = pd.read_sql_query(query_labs, conn)
            conn.close()
    
            
    
            ids = []
            labels = []
            parents = []
            values = []
            colors = []
            hover_text = []
            text_display = []
    
            total_labs = int(df_labs["lab_id"].count())
            total_universidades = len(df_universidades)
    
            # Root / bloco principal
            ids.append("root")
            labels.append("Universidades")
            parents.append("")
            values.append(total_labs)
            colors.append("#c0392b")  # vermelho, fora da escala
    
            text_display.append(
                "Universidades<br>"
                f"<b>{total_universidades}</b><br>"
                "universidades<br>"
                f"<b>{total_labs}</b> labs"
            )
    
            hover_text.append(
                f"<b>Universidades</b><br>"
                f"Total de universidades com labs: {total_universidades}<br>"
                f"Total de labs: {total_labs}"
            )
    
            for _, uni_row in df_universidades.iterrows():
                uni_db_id = uni_row["university_id"]
                uni_id = f"uni_{uni_db_id}"
                nome_uni = uni_row["Universidade"]
                nome_uni_formatado = formatar_nome_universidade(nome_uni)
                quantidade_labs = int(uni_row["Quantidade_Labs"])
    
                # Escala visual: 1, 2 ou 3+
                if quantidade_labs <= 1:
                    cor = "#5ec962"
                elif quantidade_labs == 2:
                    cor = "#21918c"
                else:
                    cor = "#3b528b"
    
                ids.append(uni_id)
                labels.append(nome_uni)
                parents.append("root")
                values.append(quantidade_labs)
                colors.append(cor)
    
                if quantidade_labs == 1:
                    texto_labs = "1 lab"
                else:
                    texto_labs = f"{quantidade_labs} labs"
    
                text_display.append(
                    f"<b>{nome_uni_formatado}</b><br>"
                    f"{texto_labs}"
                )
    
                hover_text.append(
                    f"<b>{nome_uni}</b><br>"
                    f"Quantidade de Labs: {quantidade_labs}<br>"
                    f"Clica para expandir"
                )
    
                labs_uni = df_labs[df_labs["university_id"] == uni_db_id]
    
                for _, lab_row in labs_uni.iterrows():
                    lab_db_id = lab_row["lab_id"]
                    lab_id = f"lab_{uni_db_id}_{lab_db_id}"
    
                    lab_info = lab_row["Lab_Info"]
    
                    if pd.isna(lab_info) or lab_info == "":
                        lab_info = "Sem informação extra"
    
                    ids.append(lab_id)
                    labels.append(f"Lab {lab_db_id}")
                    parents.append(uni_id)
                    values.append(1)
                    colors.append("#bdbdbd")  # cinzento, fora da escala
    
                    text_display.append(
                        f"<b>Lab {lab_db_id}</b><br>"
                        f"{lab_info}"
                    )
    
                    hover_text.append(
                        f"<b>Lab {lab_db_id}</b><br>"
                        f"Universidade: {nome_uni}<br>"
                        f"Info: {lab_info}"
                    )
    
            
    
            treemap = go.Treemap(
                ids=ids,
                labels=labels,
                parents=parents,
                values=values,
                branchvalues="total",
                maxdepth=2,
    
                text=text_display,
                textinfo="text",
                textposition="middle center",
    
                marker=dict(
                    colors=colors,
                    line=dict(width=2, color="white")
                ),
    
                hovertext=hover_text,
                hoverinfo="text",
    
                textfont=dict(
                    size=13,
                    color="white",
                    family="Arial"
                ),
    
                tiling=dict(
                    pad=3
                )
            )
    
            # Trace invisível só para manter a escala lateral 1-3
            escala = go.Scatter(
                x=[None],
                y=[None],
                mode="markers",
                marker=dict(
                    colorscale=[
                        [0.00, "#5ec962"],
                        [0.50, "#21918c"],
                        [1.00, "#3b528b"]
                    ],
                    cmin=1,
                    cmax=3,
                    color=[1, 2, 3],
                    showscale=True,
                    colorbar=dict(
                        title="Nº Labs",
                        tickmode="array",
                        tickvals=[1, 2, 3],
                        ticktext=["1", "2", "3+"],
                        len=0.55,
                        thickness=14,
                        x=1.02,
                        outlinewidth=0
                    )
                ),
                hoverinfo="skip",
                showlegend=False
            )
    
            fig = go.Figure(data=[treemap, escala])
    
            fig.update_layout(
                title={
                    "text": "Labs por Universidade<br><sub>Clica numa universidade para expandir e ver os labs</sub>",
                    "x": 0.5,
                    "xanchor": "center"
                },
                height=900,
                margin=dict(t=100, l=20, r=90, b=20),
                font=dict(size=12, family="Arial"),
    
                paper_bgcolor="#f2f2f2",
                plot_bgcolor="#f2f2f2",
    
                xaxis=dict(
                    visible=False,
                    showgrid=False,
                    zeroline=False
                ),
                yaxis=dict(
                    visible=False,
                    showgrid=False,
                    zeroline=False
                )
            )
    
            fig.write_html(str(html_path))
    
            webbrowser.open_new_tab(html_path.resolve().as_uri())

            print(" Treemap aberto no browser.")
    
    
            return df_universidades
    
        except Exception as e:
            print(f"❌ Erro: {str(e)}")
            import traceback
            traceback.print_exc()
            raise



