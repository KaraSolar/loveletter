clear
#repo=https://github.com/PPUC/ZeDMD.git
repo=https://github.com/KaraSolar/loveletter.git
repo_crons=https://github.com/KaraSolar/Rpi_Crons.git

tags=($(git ls-remote --tags $repo | awk -F'/' '{print $NF}'))
tag=$(git ls-remote --tags --sort="v:refname" $repo_crons | tail -n1 | awk -F'/' '{print $NF}')

log_stated_install(){
	DISPLAY_VER=$(echo $INSTALL_VER | sed "s|~alpha||g" | sed "s|~beta||g")
	echo '   ___  ___  ___  ______  ___  ____  ____ __     ___ ___  ___ ___ ____  ___  __  __ ___  __ '
	echo '   ||\\//|| // \\ | || | // \\ || \\||   (( \   // \\||\\//||// \\  // // \\ ||\ ||// \\(( \'
	echo '   || \/ ||((   ))  ||  ((   ))||_//||==  \\    ||=|||| \/ ||||=|| // ((   ))||\\||||=|| \\ '
	echo '   ||    || \\_//   ||   \\_// || \\||___\_))   || ||||    |||| ||//__ \\_// || \|||| ||\_))'
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
	echo ""
}

add_or_replace_variable() {
    local variable="$1"  # The variable name
    local value="$2"     # The value to set
    local file="$3"      # The target file

    if grep -q "^$variable=" "$file"; then
        # Replace the existing variable line
        sed -i "s|^$variable=.*|$variable=$value|" "$file"
    else
        # Append the variable to the end of the file
        echo "$variable=$value" >> "$file"
    fi
}

loveletter_service(){
	echo -e "Installing Cron Jobs Services ...\n"
	dest_dir=$(basename -s .git "$repo_crons")
	if [[ -d $dest_dir ]]; then
		echo "Directory '$dest_dir' already exists. Deleting it..."
		rm -rf "$dest_dir"
	fi
	git clone --branch $tag --single-branch $repo_crons --progress 2>&1 | sed '/You are in '\''detached HEAD'\''/,$d'
	sudo cp ~/Rpi_Crons/loveletter.service /etc/systemd/system/
	auxdir=$(pwd)/loveletter
	add_or_replace_variable "WorkingDirectory" "${auxdir}" "/etc/systemd/system/loveletter.service"
	auxdir=$(pwd)/loveletter/start.sh
	add_or_replace_variable "ExecStart" "${auxdir}" "/etc/systemd/system/loveletter.service"

	sudo systemctl daemon-reload
	sudo systemctl enable loveletter.service
	sudo systemctl start loveletter.service

}

repo_install(){
	dest_dir=$(basename -s .git "$repo")
	if [[ -d $dest_dir ]]; then
		echo "Directory '$dest_dir' already exists. Deleting it..."
		rm -rf "$dest_dir"
	fi
	git clone --branch $INSTALL_VER --single-branch $repo --progress 2>&1 | sed '/You are in '\''detached HEAD'\''/,$d'
	cd loveletter
	sudo apt update && sudo apt upgrade -y && sudo apt dist-upgrade -y && sudo apt full-upgrade -y
	apt list --upgradable
	sudo apt -o APT::Get::Always-Include-Phased-Updates=true full-upgrade -y
	sudo apt install python3 -y
	sudo apt install python3-pip -y
	sudo apt install python3-tk -y
	sudo apt install python3.12-venv -y
	#sudo apt install python3-xyz -y
	python3 --version
	sudo apt update && sudo apt upgrade -y
	python3 -m venv env
	source env/bin/activate

	pip3 install Pillow
	pip3 install pyModbusTCP
	pip3 install pyserial
	pip3 install PyYAML
	pip3 install six
	pip3 install ttkbootstrap
	pip3 install pymodbus==2.5.3

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
		loveletter_service
		#repo_install

		#echo "You selected: ${tags[((response-1))]}"
	else
		INSTALL_VER=${tags[response-1]}
		log_stated_install
		loveletter_service
		#repo_install
		
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
