from datetime import date
from weasyprint import HTML, CSS


class ReportPdf:
    def __init__(self, data, report_file_name, img_path1, img_path2):
        self.data = data
        self.caption = ""
        self.headers = []
        self.rows = []
        self.report_file_name = report_file_name
        self.date = None
        self.img_path1 = img_path1
        self.img_path2 = img_path2
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
                margin-bottom: 10mm;
                background-color: #86af49;
                display: flex; 
                justify-content: center; 
                align-items: center; 
            }
            
            div.container_chart2 {
                height: 88mm;
                width: 95mm;
                margin-left: 57mm;
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
            
            table.center {
                margin-left:auto; 
                margin-right:auto;
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
        data_table = f"""<table class="center">
            <thead>
                <tr>
                    {"".join(self.headers)}
                </tr>
            </thead>
            <tbody>
                {''.join(self.rows)}
            </tbody>
        </table>"""

        content = f"""<div class="container_page"> 
            <div class="container_title"><h1>{self.caption}</h1></div>
            <div class="container_subtitle1"><h2>Summary in terms of amounts</h2></div>
            <div class="container_first_chart_section">
                <div class="container_table">{data_table}</div>
                <div class="container_chart1"><img class="displayed" src ="{self.img_path1}"></div>
            </div>
            <div class="container_subtitle2"><h2>Percentage share of a given category</h2></div>
            <div class="container_chart2"><img class="displayed" src ="{self.img_path2}"></div>
        </div>
        """

        return content

    def save_pdf(self):
        content = self.create_content()
        stylesheet = self.define_style_css()
        html = HTML(string=content)
        css = CSS(string=stylesheet)
        html.write_pdf(f"{self.report_file_name}", stylesheets=[css])
