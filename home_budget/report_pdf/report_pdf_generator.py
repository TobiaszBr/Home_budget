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

        return content

    def save_pdf(self):
        content = self.create_content()
        stylesheet = self.define_style_css()
        html = HTML(string=content)
        css = CSS(string=stylesheet)
        html.write_pdf(f"{self.report_file_name}", stylesheets=[css])
