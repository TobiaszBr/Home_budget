from datetime import date
from weasyprint import HTML, CSS


class ReportPdf:
    def __init__(self, data, report_file_name, img_path):
        self.data = data
        self.caption = ""
        self.headers = []
        self.rows = []
        self.report_file_name = report_file_name
        self.date = None
        self.img_path = img_path
        self.add_rows()

    def add_rows(self):
        # create caption
        self.date = date(int(self.data['year']), int(self.data['month']), 1)
        self.caption = f"Expenses report for {self.date.strftime('%B %Y')}"

        # create headers
        for key in self.data["data"][0].keys():
            header = f"<th>{key.title()}</th>"
            self.headers.append(header)

        # create data rows
        for element in self.data["data"]:
            row = f"<tr><td>{element['category']}</td><td>{element['total']}</td></tr>"
            self.rows.append(row)

    def define_style_css(self):
        stylesheet = """
            body {
                font-family: sans-serif;
            }
            
            table {
                width: 70%;
                border-collapse: collapse;
            }
            
            table.center {
                margin-left:auto; 
                margin-right:auto;
            }
            
            thead {
                background-color: #81AAAA
            }

            tr {
                border-bottom: 2px solid #777;
            }
            
            td {
                background-color: #D6EEEE
            }
            
            """

        stylesheet = """
            div.container_page {
                width: 210mm;
                height: 297mm;
                margin-top: -22mm;
                margin-left: -22mm;
                background-color: #499afa;
            }
            
            div.container_title {
                height: 20mm;
                margin-top: 20mm;
                margin-bottom: 20mm;
                background-color: #fab949;
            }
            
            div.container_subtitle1 {
                height: 10mm;
                margin-bottom: 10mm;
                background-color: #fab949;
            }
            
            div.container_first_chart_section {
                height: 83mm;
                width: 200mm;
                margin-left: 5mm;
                margin-right: 5mm;
                margin-bottom: 10mm;
                background-color: red;
            }
            
            div.container_table {
                float: left;
                height: 100%;
                width: 95mm;
                background-color: #fab949;
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
                margin-bottom: 10mm;
                background-color: #fa8010;
            }
            
            div.container_chart2 {
                height: 83mm;
                width: 95mm;
                margin-left: 57mm;
                background-color: green;
            }
            
            
        
        """

        return stylesheet

    def create_content(self):
        # <caption>{self.caption}</caption>
        content = f"""<table class="center">
            <h2>{self.caption}</h2>
            <thead>
                <tr>
                    {"".join(self.headers)}
                </tr>
            </thead>
            <tbody>
                {''.join(self.rows)}
            </tbody>
        </table>
        <img src ="{self.img_path}" width="300" height="200">"""

        content = f"""<div class="container_page">
            <div class="container_title"></div>
            <div class="container_subtitle1"></div>
            <div class="container_first_chart_section">
                <div class="container_table"></div>
                <div class="container_chart1"></div>
            </div>
            <div class="container_subtitle2"></div>
            <div class="container_chart2"></div>
 
        </div>
        """

        return content

    def save_pdf(self):
        content = self.create_content()
        stylesheet = self.define_style_css()
        html = HTML(string=content)
        css = CSS(string=stylesheet)
        html.write_pdf(f"{self.report_file_name}", stylesheets=[css])
