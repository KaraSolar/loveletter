clear

repo=https://github.com/KaraSolar/loveletter.git
#repo=https://github.com/PPUC/ZeDMD.git
tags=($(git ls-remote --tags $repo | awk -F'/' '{print $NF}'))

log_stated_install(){
	DISPLAY_VER=$(echo $INSTALL_VER | sed "s|~alpha||g" | sed "s|~beta||g")
	echo '___  ___  ___  ______  ___  ____  ____ __     ___ ___  ___ ___ ____  ___  __  __ ___  __ '
	echo '||\\//|| // \\ | || | // \\ || \\||   (( \   // \\||\\//||// \\  // // \\ ||\ ||// \\(( \'
	echo '|| \/ ||((   ))  ||  ((   ))||_//||==  \\    ||=|||| \/ ||||=|| // ((   ))||\\||||=|| \\ '
	echo '||    || \\_//   ||   \\_// || \\||___\_))   || ||||    |||| ||//__ \\_// || \|||| ||\_))'
	echo "                                                                        "
	echo "                                        LOVELETTER INSTALLER                       "
	if [[ "$INSTALL_VER" =~ "beta" ]]; then
	    echo "                                            BETA RELEASE                       "
	fi
	if [[ "$INSTALL_VER" =~ "alpha" ]]; then
		echo "                                        DEVELOPMENT SNAPSHOT                      "
		echo "                                   OT INTENDED FOR PRODUCTION USE                 "
		echo "                                        USE AT YOUR OWN RISK                      "
	fi
	echo "                                             ${INSTALL_VER}                           "
}

repo_install(){
	dest_dir=$(basename -s .git "$repo")
	if [[ -d $dest_dir ]]; then
		echo "Directory '$dest_dir' already exists. Deleting it..."
		rm -rf "$dest_dir"
	fi
	git clone --branch $INSTALL_VER --single-branch $repo --progress 2>&1 | sed '/You are in '\''detached HEAD'\''/,$d'
	#rm -rf "install.sh"
}

clines(){
	local lines_to_clear=$1
    for ((j=0; j<lines_to_clear; j++)); do
        tput cuu1  # Mueve el cursor una línea hacia arriba
        tput el    # Limpia la línea actual
    done
}

echo "Repo Installing: $repo"
echo -e "________________________Avalaible Tags_________________________\n"
for i in "${!tags[@]}"; do
    echo "$((i + 1)). ${tags[$i]}"
done
((i++))
echo "_______________________________________________________________"

if [[ ${#tags[@]} -eq 0 ]]; then
    echo "No exist a valid TAG avalaible"
else
	echo -e '\nSelect a tag version to Install, or type "0" to defaul install'
    read -p "->  Select betwen (1-$i): " response

	clines 4

	if [[ "$response" -gt "$i" ]]; then
    	echo -e "    Tag selected: ($response) no exist"
	elif [[ "$response" -eq 0 ]]; then
		response=i
		INSTALL_VER=${tags[response-1]}
		log_stated_install
		repo_install
		#echo "You selected: ${tags[((response-1))]}"
	else
		INSTALL_VER=${tags[response-1]}
		log_stated_install
		repo_install
		#echo "You selected: ${tags[((response-1))]}"
	fi
fi

tput civis
read -p "" input
tput cnorm



: '
coment 
multi
lines'
