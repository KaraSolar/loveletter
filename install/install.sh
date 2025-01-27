clear

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
    local variable="$1"
    local value="$2"
    local file="$3"

    if grep -q "^$variable=" "$file"; then
        sudo sed -i "s|^$variable=.*|$variable=$value|" "$file"
    else
        echo "$variable=$value" >> "$file"
    fi
}

clean_dir() {
    local repo_url="$1"
    local dest_dir=$(basename -s .git "$repo_url")
    if [[ -d $dest_dir ]]; then
        echo "Directory '$dest_dir' already exists. Deleting it..."
        rm -rf "$dest_dir"
    fi
}

clone_repo() {
    local tag="$1"
    local repo_crons="$2"

    echo "------------------------------------------------------------"

    git clone --branch "$tag" --single-branch "$repo_crons" --progress 2>&1 | \
        sed '/You are in '\''detached HEAD'\''/,$d' | \
        while IFS= read -r line; do
            echo -e "\e[32m✔ $line\e[0m"  # Green for progress logs
        done

    # Check if the clone was successful
    if [[ ${PIPESTATUS[0]} -eq 0 ]]; then
        echo "------------------------------------------------------------"
    else
        echo "------------------------------------------------------------"
        echo -e "\e[31m❌ Clone failed for repository: $repo_crons\e[0m"
        return 1
    fi
}


loveletter_service(){
	echo -e "\nInstalling Cron Jobs Services ..."
	clean_dir "$repo_crons"
	clone_repo $tag $repo_crons
	#git clone --branch $tag --single-branch $repo_crons --progress 2>&1 | sed '/You are in '\''detached HEAD'\''/,$d'
	sudo cp $(pwd)/Rpi_Crons/loveletter.service /etc/systemd/system/
	sudo cp $(pwd)/Rpi_Crons/daily_restart.service /etc/systemd/system/
	sudo cp $(pwd)/Rpi_Crons/daily_restart.timer /etc/systemd/system/
	add_or_replace_variable "WorkingDirectory" "$(pwd)" "/etc/systemd/system/loveletter.service"
	add_or_replace_variable "ExecStart" "$(pwd)/start.sh" "/etc/systemd/system/loveletter.service"

	sudo systemctl daemon-reload
	sudo systemctl enable loveletter.service
	sudo systemctl start loveletter.service

}

python_upgrade(){
	sudo apt install python3 -y
	sudo apt install python3-pip -y
	sudo apt install python3-tk -y
	sudo apt install python3.12-venv -y
	#sudo apt install python3-xyz -y
}

packages_update(){
	sudo apt update && sudo apt upgrade -y && sudo apt dist-upgrade -y && sudo apt full-upgrade -y
	apt list --upgradable
	sudo apt -o APT::Get::Always-Include-Phased-Updates=true full-upgrade -y
	sudo apt update && sudo apt upgrade -y
}

install_requirements() {
    local requirements_file="$1"

    if [[ -f "$requirements_file" ]]; then
        echo "Installing requirements from $requirements_file..."

        while read -r package; do
            if pip install "$package" &>/tmp/pip_install_log; then
                echo "✅ Successfully installed: $package"
            else
                echo "❌ Failed to install: $package"
                echo "Error log:"
                cat /tmp/pip_install_log
            fi
        done < "$requirements_file"
    else
        echo "Error: $requirements_file not found."
        return 1
    fi
}

repo_install(){
	clean_dir "$repo"
	clone_repo $INSTALL_VER $repo
	#git clone --branch $INSTALL_VER --single-branch $repo --progress 2>&1 | sed '/You are in '\''detached HEAD'\''/,$d'
	cd loveletter
	chmod +x $(pwd)/start.sh
	
	echo -e "\n__________ Python version Avalaible: $(python3 --version)  ________"
	
	python3 -m venv env
	source env/bin/activate

	: 'pip3 install Pillow
	pip3 install pyModbusTCP
	pip3 install pyserial
	pip3 install PyYAML
	pip3 install six
	pip3 install ttkbootstrap
	pip3 install pymodbus==2.5.3'

	install_requirements "requirements.txt"

	#rm -rf "install.sh"
}

clines(){
	local lines_to_clear=$1
    for ((j=0; j<lines_to_clear; j++)); do
        tput cuu1
        tput el
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
		loveletter_service
	else
		INSTALL_VER=${tags[response-1]}
		log_stated_install
		repo_install
		loveletter_service
	fi
fi

bash start.sh
echo -e "\e[34m\nInstall completed successfully (Branch/Tag: $INSTALL_VER)\e[0m"
tput civis
read -p "" input
tput cnorm



: '
coment 
multi
lines'
