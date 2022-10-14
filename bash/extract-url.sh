#!/bin/bash

# obtener el robots.txt
curl -O https://www.mayoral.com/robots.txt

# obtener un sitemap
curl -O https://www.mayoral.com/sitemaps/ata1/sitemap-de-ata1-static.xml.gz

# descomprimir y obtener los enlaces limpios
gzip.exe -d sitemap-de-ata1-static.xml.gz

# obtener los enlaces limpios
cat sitemap-de-ata1-static.xml | grep loc | sed 's/<loc>//' | sed 's/<\/loc>//' | sed 's/ *//' > url.txt


