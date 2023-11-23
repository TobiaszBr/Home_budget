from datetime import date
import os
from pathlib import Path
import matplotlib
from matplotlib import pyplot as plt
from weasyprint import HTML, CSS


# pyplot backend needs to be changed
matplotlib.use("Agg")


class ReportPdf:
    def __init__(self, data, user):
        self.data = data
        self.user = user
        self.report_year = int(self.data["year"])
        self.report_month = int(self.data["month"]) if self.data["month"] else 1
        self.report_date = date(self.report_year, self.report_month, 1)
        self.table_headers = []
        self.table_rows = []
        self.report_directory = "report_pdf"
        if self.data["month"]:
            self.report_name = f"report_user_id_{self.user.id}_{self.report_year}_{self.report_month}.pdf"
        else:
            self.report_name = f"report_user_id_{self.user.id}_{self.report_year}.pdf"
        self.report_save_path = os.path.join(self.report_directory, self.report_name)
        self.bar_chart_name = "bar_chart.jpg"
        self.pie_chart_name = "pie_chart.jpg"
        self.chart_axis_x = []
        self.chart_axis_y = []
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.bar_char_path = None
        self.pie_char_path = None

        # html content variables
        title_format = "%B %Y" if self.data.get("month", "") else "%Y"
        self.doc_title = (
            f"Expenses report for {self.report_date.strftime(title_format)}"
        )
        self.subtitle1 = "Summary in terms of amounts"
        self.subtitle2 = "Percentage share of a given category"
        self.char_colors = [
            "#2f4858",
            "#3e6066",
            "#597771",
            "#7a8d7d",
            "#9fa28e",
            "#c4b7a6",
            "#1c6960",
            "#4a7964",
            "#6d886c",
            "#8e8272",
        ]

        # call create methods
        self.create_table()
        self.create_bar_chart()
        self.create_pie_chart()
        self.content = self.create_content()
        self.stylesheet = self.create_style_css()

    def create_table(self):
        # create table headers
        for key in self.data["data"][0].keys():
            header = f"<th>{key.title()}</th>"
            self.table_headers.append(header)

        # create data rows
        for element in self.data["data"]:
            row = f"<tr><td>{element['category']}</td><td>{element['total']}</td></tr>"
            self.table_rows.append(row)

            # create x and y chart axis
            self.chart_axis_x.append(element["category"])
            self.chart_axis_y.append(element["total"])

    def create_bar_chart(self):
        plt.bar(self.chart_axis_x, self.chart_axis_y, width=0.5, color=self.char_colors)
        plt.grid(axis="y")
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout()
        bar_chart_path = os.path.join(
            self.BASE_DIR, self.report_directory, self.bar_chart_name
        )
        plt.savefig(bar_chart_path)
        self.bar_char_path = "file:\\\\" + bar_chart_path
        plt.close()

    def create_pie_chart(self):
        patches, texts, autotexts = plt.pie(
            self.chart_axis_y,
            labels=self.chart_axis_x,
            autopct="%.1f%%",
            colors=self.char_colors,
        )
        for autotext in autotexts:
            autotext.set_color("white")

        pie_chart_path = os.path.join(
            self.BASE_DIR, self.report_directory, self.pie_chart_name
        )

        plt.savefig(pie_chart_path, bbox_inches="tight")
        self.pie_char_path = "file:\\\\" + pie_chart_path
        plt.close()

    @staticmethod
    def create_style_css():
        stylesheet = """
            div.container_page {
                width: 210mm;
                height: 297mm;
                margin-top: -22mm;
                margin-left: -22mm;
                background-color: #d5e1df;
            }
            
            div.container_title {
                height: 40mm;
                margin-top: 0mm;
                margin-bottom: 10mm;
                background-color: #3e6066;
                display: flex; 
                justify-content: center; 
                align-items: center; 
            }
            
            div.container_subtitle1 {
                height: 10mm;
                margin-bottom: 10mm;
                background-color: #7a8d7d;
                display: flex; 
                justify-content: center; 
                align-items: center; 
            }
            
            div.container_first_chart_section {
                height: 88mm;
                width: 200mm;
                margin-left: 5mm;
                margin-right: 5mm;
                margin-bottom: 10mm;
                background-color: #d5e1df;
            }
            
            div.container_table {
                float: left;
                height: 100%;
                width: 95mm;
                background-color: #d5e1df;;
            }
            
            div.container_chart1 {
                float: left;
                height: 100%;
                width: 95mm;
                margin-left: 9mm;
                background-color: green;
            }
            
            div.container_subtitle2 {
                height: 10mm;
                background-color: #7a8d7d;
                margin-bottom: 10mm;
                display: flex; 
                justify-content: center; 
                align-items: center; 
            }
            
            div.container_chart2 {
                height: 88mm;
                width: 115mm;
                margin-left: 47mm;
                background-color: green;
            }
            
            h1, h2 {
                color: white;
            }
            
            h1 {
                font-size: 48px;
            }
            
            img.displayed {
                display: block;
                height: 100%;
                width: 100%;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
            }
            
            thead {
                background-color: #99b0a8;
                color: white;
                font-size: 26px;
            }

            tr {
                border-bottom: 2px solid black;
            }
            
            td {
                background-color:  #d5e1df;
                font-size: 20px;
            }
        """
        return stylesheet

    def create_content(self):
        data_table = f"""<table>
            <thead>
                <tr>
                    {"".join(self.table_headers)}
                </tr>
            </thead>
            <tbody>
                {''.join(self.table_rows)}
            </tbody>
        </table>"""

        content = f"""<div class="container_page"> 
            <div class="container_title"><h1>{self.doc_title}</h1></div>
            <div class="container_subtitle1"><h2>{self.subtitle1}</h2></div>
            <div class="container_first_chart_section">
                <div class="container_table">{data_table}</div>
                <div class="container_chart1"><img class="displayed" src="{self.bar_char_path}"></div>
            </div>
            <div class="container_subtitle2"><h2>{self.subtitle2}</h2></div>
            <div class="container_chart2"><img class="displayed" src="{self.pie_char_path}"></div>
        </div>
        """

        return content

    def save_pdf(self):
        html = HTML(string=self.content)
        css = CSS(string=self.stylesheet)
        html.write_pdf(self.report_save_path, stylesheets=[css])
