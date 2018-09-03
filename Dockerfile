FROM ubuntu

RUN apt-get update && \
    apt-get -y install curl git gnupg gnupg2 gnupg1  && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    apt-get install -y nodejs

RUN npm install --save api-spec-transformer

COPY contrib/convert.sh /convert.sh
COPY contrib/raml2oas.js /raml2oas.js
