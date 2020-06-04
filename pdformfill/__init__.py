# -*- coding: utf-8 -*-
__author__ = "Tomislav Kucar <kucar.tomislav@gmail.com>"

import os
import uuid

from pdformfill.fdf import forge_fdf


def fill_pdf(fields, in_file, out_file):
    fdf = forge_fdf(fdf_data_strings=fields)
    fdf_file_name = str(uuid.uuid4())
    with open(fdf_file_name, "wb") as fdf_file:
        fdf_file.write(fdf)

    os.system("pdftk " + in_file + " fill_form " +
              fdf_file_name + " output " + out_file + " flatten")

    try:
        os.remove(fdf_file_name)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
