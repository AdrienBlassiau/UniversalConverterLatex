 FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 RUN apt-get update
 RUN apt-get install -y texlive-full
 RUN apt-get install poppler-utils
 RUN apt-get install xzdec
 RUN tlmgr init-usertree
 RUN $(which tlmgr) install graphics chemfig luatex85 standalone tikz-cd pgf luatex simplekv latexmk
 ADD requirements.txt /code/
 RUN pip install --upgrade pip
 RUN pip install -r requirements.txt
 RUN pip install django-bootstrap4
 ADD . /code/