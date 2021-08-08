FROM python:3.8

RUN pip3 install pandas
RUN pip3 install datetime
RUN pip3 install dash
RUN pip3 install dash_auth
RUN pip3 install dash_core_components
RUN pip3 install dash_html_components
RUN pip3 install dash_bootstrap_components
RUN pip3 install dash_table
RUN pip3 install plotly
RUN pip3 install flask
RUN pip3 install flask_login
RUN pip3 install flask_sqlalchemy
RUN pip3 install psycopg2
RUN pip3 install sqlalchemy
RUN pip3 install waitress
RUN pip3 install boto3


COPY / /

EXPOSE 8050

CMD [ "python", "/index.py" ]