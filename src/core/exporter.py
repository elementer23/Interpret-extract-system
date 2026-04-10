from openpyxl import Workbook
import json

class Exporter():
    def __init__(self):
        pass

    def export_to_excel(self, data_to_enter: list) -> None:
        wb = Workbook()

        for i in range(len(data_to_enter)):
            if i == 0:
                ws = wb.active
            else:
                ws = wb.create_sheet()

            headers = ["Type", "Text", "Left", "Top", "Width", "Height"]
            ws.append(headers)

            for bbx in data_to_enter[i]:
                dt = bbx.area_domain()

                row = [dt['type'], dt['text'], dt['left'], dt['top'], dt['width'], dt['height']]

                ws.append(row)

        wb.save(r"C:/Users/697/Documents/output.xlsx")

    def export_to_json(self, data_to_enter: list) -> None:
        pass