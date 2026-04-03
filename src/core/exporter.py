from openpyxl import Workbook

class Exporter():
    def __init__(self):
        pass

    def export_to_excel(self, data_to_enter: list) -> None:
        wb = Workbook()
        ws = wb.active
        ws.title = "Extracted"
        ws = wb["Extracted"]

        headers = ["Type", "Text", "Left", "Top", "Width", "Height"]
        ws.append(headers)

        for bbx in data_to_enter:
            dt = bbx.area_domain()

            row = [dt['type'], dt['text'], dt['left'], dt['top'], dt['width'], dt['height']]

            ws.append(row)


        wb.save(r"C:/Users/697/Documents/output.xlsx")