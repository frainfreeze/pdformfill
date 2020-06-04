import os
from pathlib import Path
import filecmp
import pdformfill

TEST_DATA_DIR = Path(__file__).resolve().parent / 'data'

def test_form_fill():
    fields = [('a1', '01'),
              ('a2', '01'),
              ('a3', '31'),
              ('a4', '12'),
              ('a5', '2020'),
              ('oib', '66089976432'),
              ('ime_prezime', 'Ivo Sivo'),
              ('adresa', 'Ulica kneza Ljudevita Posavskog 53, 10410 Velika Gorica'),
              ('djelatnost', '6201, Racunalno programiranje'),
              ('adresa_djelatnosti',
               'Ulica kneza Ljudevita Posavskog 53, 10410 Velika Gorica'),
              ('b1', ''),
              ('b2', ''),
              ('b3', ''),
              ('b4', ''),
              ('b5', ''),
              ('b6', ''),
              ('b7', ''),
              ('b8', ''),
              ('b9', ''),
              ('b10', ''),
              ('gotovinski_primici', '10,121.00'),
              ('bezgotovinski_primici', '30,000.00'),
              ('ukupno_primici', '40,121.00'),
              ('c1', '40,121.00'),
              ('c2', '12'),
              ('d1', '0.00'),
              ('d2', '0'),
              ('e1', '40,121.00'),
              ('e2', ''),
              ('vii_1', '1,530,00'),
              ('prirez_porezu', '18,00'),
              ('vii_2', '275,40'),
              ('vii_3', '1,805.40'),
              ('vii_4', '0.00'),
              ('vii_5', '1,805.40'),
              ('vii_6', ''),
              ('vii_7', '1,805.40'),
              ('vii_8', '150.40'),
              ('nadnevak', '1.1.2021.'),
              ('potpis', 'SivoIvo')]

    in_file = os.path.join(TEST_DATA_DIR, "PO-SD2020_da.pdf")
    out_file = os.path.join(TEST_DATA_DIR, "new_output.pdf")
    pdformfill.fill_pdf(fields, in_file, out_file)
    print(os.getcwd())
    assert filecmp.cmp(os.path.join(TEST_DATA_DIR, "output.pdf"), out_file) == True