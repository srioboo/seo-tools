#!/bin/bash

set -euo pipefail # https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/

readonly url=$1     # get the first argument
readonly ctrlang=$2 # get contry-language pair

# Main method
main() {

	if [ -z "$url" ]; then
		echo "Required url"
	else
		echo "parame $url"

		# crear el directorio
		mkdir -p output

		# obtener el robots.txt
		curl -O $url/robots.txt

		# temporal sitemaps
		cat robots.txt | grep Sitemap >sitemaps-$ctrlang.txt

		while IFS= read -r line; do
			echo $line
		done <sitemaps-$ctrlang.txt

		# mapfile robots.txt -- solo version 5
		# mapfile -t urlSitemap < sitemaps.txt
		# for value in "${urlSitemap[@]}"
		# do
		#  echo "Value for sitemaps array is: $value"
		# done

		tipos=('statics' 'images' 'products' 'categories')
		for tipo in "${tipos[@]}"; do
			# obtenemos los sitemaps de cada tipo
			curl -O $url/sitemap-$ctrlang-$tipo.xml.gz
		done

		# descomprimir y obtener los enlaces limpios
		gzip -d sitemap*.xml.gz

		# obtener los enlaces limpios staticas
		for tipo in "${tipos[@]}"; do
			cat sitemap-$ctrlang-$tipo.xml | grep loc | sed 's/<loc>//' | sed 's/<\/loc>//' | sed 's/ *//' >url-$tipo-$ctrlang.txt
		done

		mv *.txt output
		mv *.xml* output

		echo "DONE"
	fi
}
main
