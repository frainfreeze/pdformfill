# -*- coding: utf-8 -*-
"""
Port of the PHP forge_fdf library by Sid Steward
(http://www.pdfhacks.com/forge_fdf/)

Anders Pearson <anders@columbia.edu> at Columbia Center For New Media Teaching
and Learning <http://ccnmtl.columbia.edu/>

Copyright (c) 2010-2017 Anders Pearson. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the
   distribution.
3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived
   from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

__author__ = "Anders Pearson <anders@columbia.edu>"
__credits__ = ("Sébastien Fievet <zyegfryed@gmail.com>",
               "Brandon Rhodes <brandon@rhodesmill.org>",
               "Robert Stewart <https://github.com/rwjs>",
               "Evan Fredericksen <https://github.com/evfredericksen>")

import codecs
import sys

if sys.version_info[0] < 3:
    bytes = str


def smart_encode_str(s):
    """Create a UTF-16 encoded PDF string literal for `s`."""
    try:
        utf16 = s.encode('utf_16_be')
    except AttributeError:  # ints and floats
        utf16 = str(s).encode('utf_16_be')
    safe = utf16.replace(b'\x00)', b'\x00\\)').replace(b'\x00(', b'\x00\\(')
    return b''.join((codecs.BOM_UTF16_BE, safe))


def handle_hidden(key, fields_hidden):
    if key in fields_hidden:
        return b"/SetF 2"
    else:
        return b"/ClrF 2"


def handle_readonly(key, fields_readonly):
    if key in fields_readonly:
        return b"/SetFf 1"
    else:
        return b"/ClrFf 1"


class FDFIdentifier(object):
    """A PDF value, such as /Yes or /Off that should be passed through with the / and without parenthesis (which would indicate it was a value, not an identifier)
    This allows for different checkbox checked/unchecked names per checkbox!
    """
    def __init__(self, value):
        # make sure value is str right away, to avoid TypeError in startswith 
        if isinstance(value, bytes):
            value = value.decode('utf-8')
            
        if value.startswith('/'):
            value = value[1:]

        value = u'/%s' % value
        value = value.encode('utf-8')

        self._value = value

    @property
    def value(self):
        return self._value
        

def handle_data_strings(fdf_data_strings, fields_hidden, fields_readonly,
                        checkbox_checked_name):
    if isinstance(fdf_data_strings, dict):
        fdf_data_strings = fdf_data_strings.items()

    for (key, value) in fdf_data_strings:
        if value is True:
            value = FDFIdentifier(checkbox_checked_name).value
        elif value is False:
            value = FDFIdentifier('Off').value
        elif isinstance(value, FDFIdentifier):
            value = value.value
        else:
            value = b''.join([b'(', smart_encode_str(value), b')'])

        yield b''.join([
            b'<<',
            b'/T(',
            smart_encode_str(key),
            b')',
            b'/V',
            value,
            handle_hidden(key, fields_hidden),
            b'',
            handle_readonly(key, fields_readonly),
            b'>>',
        ])


def handle_data_names(fdf_data_names, fields_hidden, fields_readonly):
    if isinstance(fdf_data_names, dict):
        fdf_data_names = fdf_data_names.items()

    for (key, value) in fdf_data_names:
        yield b''.join([b'<<\x0a/V /', value.encode("utf-8"), b'\x0a/T (',
                        smart_encode_str(key), b')\x0a',
                        handle_hidden(key, fields_hidden), b'\x0a',
                        handle_readonly(key, fields_readonly), b'\x0a>>\x0a'])


def forge_fdf(pdf_form_url=None, fdf_data_strings=[], fdf_data_names=[],
              fields_hidden=[], fields_readonly=[],
              checkbox_checked_name=b"Yes"):
    """Generates fdf string from fields specified

    * pdf_form_url (default: None): just the url for the form.
    * fdf_data_strings (default: []): array of (string, value) tuples for the
      form fields (or dicts). Value is passed as a UTF-16 encoded string,
      unless True/False, in which case it is assumed to be a checkbox
      (and passes names, '/Yes' (by default) or '/Off').
    * fdf_data_names (default: []): array of (string, value) tuples for the
      form fields (or dicts). Value is passed to FDF as a name, '/value'
    * fields_hidden (default: []): list of field names that should be set
      hidden.
    * fields_readonly (default: []): list of field names that should be set
      readonly.
    * checkbox_checked_value (default: "Yes"): By default means a checked
      checkboxes gets passed the value "/Yes". You may find that the default
      does not work with your PDF, in which case you might want to try "On".

    The result is a string suitable for writing to a .fdf file.

    """
    fdf = [b'%FDF-1.2\x0a%\xe2\xe3\xcf\xd3\x0d\x0a']
    fdf.append(b'1 0 obj\x0a<</FDF')
    fdf.append(b'<</Fields[')
    fdf.append(b''.join(handle_data_strings(fdf_data_strings,
                                            fields_hidden, fields_readonly,
                                            checkbox_checked_name)))
    fdf.append(b''.join(handle_data_names(fdf_data_names,
                                          fields_hidden, fields_readonly)))
    if pdf_form_url:
        fdf.append(b''.join(b'/F (', smart_encode_str(pdf_form_url), b')\x0a'))
    fdf.append(b']\x0a')
    fdf.append(b'>>\x0a')
    fdf.append(b'>>\x0aendobj\x0a')
    fdf.append(b'trailer\x0a\x0a<<\x0a/Root 1 0 R\x0a>>\x0a')
    fdf.append(b'%%EOF\x0a\x0a')
    return b''.join(fdf)