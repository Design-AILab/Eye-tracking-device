#!/bin/bash

openssl genrsa -des3 -passout pass:x -out server.pass.key 2048
openssl rsa -passin pass:x -in server.pass.key -out cert/server.key
rm server.pass.key
openssl req -new -key cert/server.key -out cert/server.csr \
    -subj "/C=TP/ST=NewTaipei/L=Taiwan/O=Vizly/OU=Vizly/CN=vizly.io@gmail.com"
openssl x509 -req -days 365 -in cert/server.csr -signkey cert/server.key -out cert_test/server.crt

# openssl genrsa -des3 -passout pass:x -out server.pass.key 1024

# openssl req -new -key server.key -out server.csr \
#     -subj "/C=Taipei/ST=Taiwan/L=Taiwan/O=Vizly/OU=Vizly/CN=vizly.io@gmail.com"

# cp server.key server.key.org 
# openssl rsa -in server.key.org -out server.key
# openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

