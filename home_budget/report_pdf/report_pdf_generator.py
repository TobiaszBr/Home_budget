from datetime import date
from weasyprint import HTML, CSS


class ReportPdf:
    def __init__(self, data, report_file_name):
        self.data = data
        self.caption = ""
        self.headers = []
        self.rows = []
        self.report_file_name = report_file_name
        self.date = None
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

    def create_content(self):
        content = f"""<table style="width:50%">
            <caption>{self.caption}</caption>
            <thead>
                <tr>
                    {"".join(self.headers)}
                </tr>
            </thead>
            <tbody>
                {''.join(self.rows)}
            </tbody>
        </table>"""

        return content

    def save_pdf(self):
        content = self.create_content()
        html = HTML(string=content)
        html.write_pdf(f"{self.report_file_name}")
