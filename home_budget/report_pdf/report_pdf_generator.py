from datetime import date
import os
from pathlib import Path
import matplotlib
from matplotlib import pyplot as plt
from weasyprint import HTML, CSS


# pyplot backend needs to be chnged
matplotlib.use("Agg")


class ReportPdf:
    def __init__(self, data):
        self.data = data
        self.report_date = date(int(self.data["year"]), int(self.data["month"]), 1)
        self.table_headers = []
        self.table_rows = []
        self.report_directory = "report_pdf"
        self.report_name = "report.pdf"
        self.bar_chart_name = "bar_chart.jpg"
        self.pie_chart_name = "pie_chart.jpg"
        self.chart_axis_x = []
        self.chart_axis_y = []
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.bar_char_path = None
        self.pie_char_path = None

        # html content variavles
        self.doc_title = f"Expenses report for {self.report_date.strftime('%B %Y')}"
        self.subtitle1 = "Summary in terms of amounts"
        self.subtitle2 = "Percentage share of a given category"
        self.page_color = "#d5e1df"

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
        plt.bar(self.chart_axis_x, self.chart_axis_y, width=0.5, color="#86af49")
        plt.grid(axis="y")
        plt.xticks(rotation=20, ha="right")
        plt.tight_layout()
        bar_chart_path = os.path.join(self.BASE_DIR, self.report_directory, self.bar_chart_name)
        plt.savefig(bar_chart_path)
        self.bar_char_path = "file:\\\\" + bar_chart_path
        plt.close()

    def create_pie_chart(self):
        plt.pie(self.chart_axis_y, labels=self.chart_axis_x, autopct=lambda pct: f"{pct:.1f}%")
        pie_chart_path = os.path.join(self.BASE_DIR, self.report_directory, self.pie_chart_name)
        plt.savefig(pie_chart_path)
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
                background-color: #537c16;
                display: flex; 
                justify-content: center; 
                align-items: center; 
            }
            
            div.container_subtitle1 {
                height: 10mm;
                margin-bottom: 10mm;
                background-color: #86af49;
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
                background-color: #86af49;
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
                background-color: #86af49;
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
        report_save_path = os.path.join(self.report_directory, self.report_name)
        html.write_pdf(report_save_path, stylesheets=[css])
