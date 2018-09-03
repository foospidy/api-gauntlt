#!/usr/bin/env bash

# https://github.com/mulesoft/oas-raml-converter/issues/33
cd oas-raml-converter && \
    sed -i "1s/ --harmony//" lib/bin/converter.js && \
    ./lib/bin/converter.js --from $FROM --to $TO /input/$SOURCE > /input/input.json
