#!/bin/bash

set -euo pipefail # https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/

readonly url=$1 # get the first argument

# Main method
main() {

	if [ -z "$url" ]; then
		echo "Required url"
	else
		echo "parame $url"

    # obtener el robots.txt
    curl -O $url/robots.txt
    
    # obtener un sitemap
    curl -O $url/sitemap-es-es-statics.xml.gz

    # descomprimir y obtener los enlaces limpios
    gzip.exe -d sitemap-es-es-statics.xml.gz
    
    # obtener los enlaces limpios
    cat sitemap-es-es-statics.xml | grep loc | sed 's/<loc>//' | sed 's/<\/loc>//' | sed 's/ *//' > url.txt

		echo "DONE"
	fi
}
main




