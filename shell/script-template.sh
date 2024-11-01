#!/usr/bin/env bash

set -euo pipefail # https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/

readonly dirDestino=$1 # get the first argument

# Main method
main() {

	if [ -z "$dirDestino" ]; then
		echo "Required parameter"
	else
		echo "parame $dirDestino"

		echo "DONE"
	fi
}
main
