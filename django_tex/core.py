import os
from subprocess import Popen, PIPE
import tempfile

from django_tex.engine import engine
from django.conf import settings

from pdf2image import convert_from_path, convert_from_bytes

DEFAULT_INTERPRETER = 'lualatex'

class TexError(Exception):
    pass

def run_tex(source):
    with tempfile.TemporaryDirectory() as tempdir:
        latex_interpreter = getattr(settings, 'LATEX_INTERPRETER', DEFAULT_INTERPRETER)
        latex_command = [latex_interpreter, '-output-directory', tempdir]
        process = Popen(latex_command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        process.communicate(source.encode('utf-8'))
        if process.returncode == 1:
            raise TexError(source)
        filepath = os.path.join(tempdir, 'texput.pdf')
        compile_pdf_to_image(filepath)
        with open(filepath, 'rb') as pdf_file:
            pdf = pdf_file.read()
    return pdf

def compile_template_to_pdf(template_name, context):
    source = render_template_with_context(template_name, context)
    return run_tex(source)

def render_template_with_context(template_name, context):
    template = get_template(template_name)
    return template.render(context)

def get_template(template_name):
    return engine.get_template(template_name)

def compile_pdf_to_image(pdf):
    pages = convert_from_path(pdf)
    for page in pages:
        page.save('/code/app/static/app/out.jpg', 'JPEG')