#!/usr/bin/env node

var transformer = require('api-spec-transformer');

var ramlToSwagger = new transformer.Converter(transformer.Formats.RAML10, transformer.Formats.SWAGGER);

ramlToSwagger.loadFile('/input/test.raml', function(err) {
  if (err) {
    console.log(err.stack);
    return;
  }

  ramlToSwagger.convert('yaml')
    .then(function(convertedData) {
      // convertedData is swagger YAML string
      console.log(convertedData);
    })
    .catch(function(err){
      console.log(err);
    });
});