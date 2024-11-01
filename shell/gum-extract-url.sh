#!/bin/sh

# This script is used to write a conventional commit message.
# It prompts the user to choose the type of commit as specified in the
# conventional commit spec. And then prompts for the summary and detailed
# description of the message and uses the values provided. as the summary and
# details of the message.
#
# If you want to add a simpler version of this script to your dotfiles, use:
#
# alias gcm='git commit -m "$(gum input)" -m "$(gum write)"'

# if [ -z "$(git status -s -uno | grep -v '^ ' | awk '{print $2}')" ]; then
#     gum confirm "Stage all?" && git add .
# fi

create_dirs() {
  mkdir -p
}

download_robots() {
  curl -O $1/robots.txt
}

extract_sitemaps() {
    # temporal sitemaps
    cat robots.txt | grep Sitemap | sed 's/Sitemap: //' >> sitemaps.txt
    cat robots.txt | grep index | sed 's/Sitemap: //'  >> sitemaps-index.txt
}

download_sitemaps() {
  		while IFS= read -r line; do
  			echo $line
  			curl $line   -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
                        -H 'accept-language: es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7' \
                        -H 'cache-control: no-cache' \
                        -H 'pragma: no-cache' \
                        -H 'priority: u=0, i' \
                        -H 'sec-ch-ua: "Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"' \
                        -H 'sec-ch-ua-mobile: ?0' \
                        -H 'sec-ch-ua-platform: "Windows"' \
                        -H 'sec-fetch-dest: document' \
                        -H 'sec-fetch-mode: navigate' \
                        -H 'sec-fetch-site: none' \
                        -H 'sec-fetch-user: ?1' \
                        -H 'upgrade-insecure-requests: 1' \
                        -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36' \
                        -O

  		done < sitemaps-index.txt # sitemaps.txt
}

unzip_sitemap() {
  gzip -d sitemap*.xml
}

move_to_output() {
  		mkdir -p output/
  		mv *.txt output/
  		mv *.xml output/
  		# rm *.xml*
  		# rm *.txt
}

URL=$(gum choose "https://www.url1.com" "https://www.url1.de" "https://www.url3.cz")

# Since the scope is optional, wrap it in parentheses if it has a value.
test -n "$URL"

# Pre-populate the input with the type(scope): so that the user may change it
# SUMMARY=$(gum input --value "$URL: " --placeholder "add language")

# Commit these changes if user confirms
gum confirm "Download robots?" && download_robots $URL

# extract sitemaps
extract_sitemaps

# download sitemaps
download_sitemaps

# move to output
move_to_output


