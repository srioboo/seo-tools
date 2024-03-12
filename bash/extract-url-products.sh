#!/bin/bash

set -euo pipefail # https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/

readonly url=$1     # get the first argument

# Main method
main() {

	if [ -z "$url" ]; then
		echo "Required url"
	else
		echo "parame $url"

		# crear el directorio
		mkdir -p output/data

		# obtener el robots.txt 
		curl -O $url/robots.txt

		# temporal sitemaps
		cat robots.txt | grep Sitemap > sitemaps.txt
		cat sitemaps.txt | grep products | sed 's/Sitemap: //'  >> temp-sitemap-product.txt 

		while IFS= read -r line; do
			# echo $line 
			curl -O $line
		done < temp-sitemap-product.txt # sitemaps.txt

		# lang=('es-es' 'it-it' 'pt-pt' 'de-de' 'pl-pl' 'us-es' 'us-en' 'gb-en' 'gr-el' 'be-fr' 'be-en' 'fr-fr' 'mx-es' 'ro-ro' 'ie-en' 'nl-en' 'at-de' 'bg-bg' 'fi-en' 'dk-en' 'se-en' )
		# for lang in "${lang[@]}"; do
			# obtenemos los sitemaps de cada tipo 
			# curl -O $url/sitemap-$lang-products.xml.gz
		# 	echo $url
		# done

		# descomprimir y obtener los enlaces limpios
		gzip -d sitemap*.xml.gz

		# obtener los enlaces limpios staticas
		# for tipo in "${tipos[@]}"; do
		#	cat sitemap-$ctrlang-$tipo.xml | grep loc | sed 's/<loc>//' | sed 's/<\/loc>//' | sed 's/ *//' > url-$tipo-$ctrlang.txt
		# done

		# obtiene todas las url de productos
		cat sitemap-*-products.xml | grep loc | sed 's/<loc>//' | sed 's/<\/loc>//' | sed 's/ *//' > products-url.txt

		# obtiene las que tienen ProductDisplay
		cat products-url.txt | grep ProductDisplay | sort | uniq > products-url-no-seo.txt

		# Obtiene los ids limpios
		cat products-url-no-seo.txt | sed -E "s/https:\/\/([a-z.-])*\/([a-z]{2})\/([a-z]{2})\/ProductDisplay_([0-9]{5})_-([0-9]{1,2})_/inicio-/g" > products-url-no-seo-id.txt
		sed -i -E "s/_([0-9]*)_([_0-9]{6})(-[0-9]{1,2})/-final/g" products-url-no-seo-id.txt
		cat products-url-no-seo-id.txt | sort | uniq > products-url-no-seo-id-sorted.txt

		# obtiene todas las url de categorias
		cat sitemap-*-categories.xml | grep loc | sed 's/<loc>//' | sed 's/<\/loc>//' | sed 's/ *//' > categories-url.txt

		# obtiene las que tienen Search
		cat categories-url.txt | grep Search | sort | uniq > categories-url-no-seo.txt

		mv products-url*.txt output/data
		mv categories-url*.txt output/data
		rm *.xml*
		rm *.txt

		echo "DONE"
	fi
}
main
