from __future__ import annotations
from utils.utilities import BasicUtils, FileType
import pymupdf
from datetime import datetime

class MetaDataCreator():
    def __init__(self, original_filepath: str | list[str]):
        self.original_filepath = original_filepath

    def get(self):
        """
        :return MetaDataBundle | list[MetaDataBundle]: returns a single MetaDataBundle object if a single filepath was given.
        returns a list of MetaDataBundle objects if a list of filepaths were given.
        """
        return self.__build()

    def __build(self) -> MetaDataBundle | list[MetaDataBundle]:
        if not self.original_filepath: return MetaDataBundle()

        batch = []
        if isinstance(self.original_filepath, list):
            for file in self.original_filepath:
                generated_data = self.__generate(file)
                batch.append(MetaDataBundle(**generated_data))
            return batch
        
        if isinstance(self.original_filepath, str):
            return MetaDataBundle(**self.__generate(self.original_filepath))

    def __generate(self, filepath):
        """
        This function generates the corresponding metadata information, from the given pdf.
        """
        invalid_file = {"title": None, "creator": None, "creationDate": None, "modDate": None,
                        "ISO216_A": "Unknown", "pdfWidth": 0, "pdfHeight": 0, "pdfWidth_mm": 0, "pdfHeight_mm": 0,
                        "pdfWidth_px": 0, "pdfHeight_px": 0, "scaled_height": 0, "scaled_width": 0}
        if BasicUtils.categorize_file_type(filepath) is not FileType.PDF: return invalid_file
        del invalid_file

        bundle = dict()
        key_check = ('title', 'creator', 'creationDate', 'modDate')
        try:
            doc = pymupdf.open(filepath)
            metadata = doc.metadata
            page = doc[0]

            page_width = page.rect.width
            page_height = page.rect.height

            page_width_mm = page_width * (25.4 / 72)
            page_height_mm = page_height * (25.4 / 72)

            dpi_scale = 96 / 72
            page_width_px = page_width * dpi_scale
            page_height_px = page_height * dpi_scale

            h, w = self.__adjusted_size_gen(page)
            f = self.__format_ISO216(round(page_height_mm), round(page_width_mm))

            for key in key_check:
                if key not in metadata:
                    bundle.update({key: None})
                else:
                    bundle.update({key: metadata[key]}) if metadata[key] else bundle.update({key: None}) 

            bundle['creationDate'] = self.__normalize_pdf_date(bundle['creationDate']) if self.__normalize_pdf_date(bundle['creationDate']) else None
            bundle['modDate'] = self.__normalize_pdf_date(bundle['modDate']) if self.__normalize_pdf_date(bundle['modDate']) else None

            bundle.update({"ISO216_A": f, "pdfWidth": round(page_width), "pdfHeight": round(page_height),
                           "pdfWidth_mm": round(page_width_mm), "pdfHeight_mm": round(page_height_mm),
                           "pdfWidth_px": round(page_width_px), "pdfHeight_px": round(page_height_px),
                           "scaled_height": h, "scaled_width": w})

            return bundle
        finally:
            doc.close()

    def __adjusted_size_gen(self, page):
        """
        This function calculates the size of the pdf in pixels,
        with a 300 dpi multiplier. 
        """
        zoom = 300 / 72
        
        w = int(round(page.rect.width * zoom))
        h = int(round(page.rect.height * zoom))

        return h, w
    
    def __format_ISO216(self, h, w):
        """
        This function returns the ISO216 format, depending on the given height and width.
        ISO216 = ('A1', 'A2', 'A3', etc.)
        """
        iso216_formats = {(1189, 841): 'A0', (594, 841): 'A1', (594, 420): 'A2', (297, 420): 'A3',
                          (297, 210): 'A4', (148, 210): 'A5', (148, 105): 'A6'}
        
        page_w_h = iso216_formats.get((int(w), int(h)), "Unknown")
        page_h_w = iso216_formats.get((int(h), int(w)), "Unknown")
        page_format = page_w_h if page_h_w == "Unknown" else page_h_w
        
        return page_format
    
    def __normalize_pdf_date(self, pdf_date: str):
        """
        This function normalizes the date from the pdf metadata
        """
        if pdf_date is None: return None

        if pdf_date.startswith("D:"):
            pdf_date = pdf_date[2:]

        formatted_str = pdf_date.replace("'", "")

        base_date_str = formatted_str[:14]
        dt_obj = datetime.strptime(base_date_str, "%Y%m%d%H%M%S")

        return dt_obj.strftime("%Y-%m-%d %H:%M:%S")

class MetaDataBundle():
    """
    This class is used as an object for the metadata of the pdf.
    """
    def __init__(self, **kwargs):
        self.__bundle = kwargs

    def _get(self):
        """
        :return dict: returns the dictionary of the MetaDataBundle
        """
        return self.__bundle