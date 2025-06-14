clear

repo=https://github.com/KaraSolar/loveletter.git
repo_crons=https://github.com/KaraSolar/Rpi_Crons.git
repo_extraction=https://github.com/KaraSolar/LoveLetterExtraction

tags=($(git ls-remote --tags $repo | awk -F'/' '{print $NF}'))
tag=$(git ls-remote --tags --sort="v:refname" $repo_crons | tail -n1 | awk -F'/' '{print $NF}')
extract_tag=$(git ls-remote --tags --sort="v:refname" $repo_extraction | tail -n1 | awk -F'/' '{print $NF}')

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
        sudo rm -r -f "$dest_dir"
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
	sudo cp $(pwd)/Rpi_Crons/loveletter.service /etc/systemd/system/
	sudo cp $(pwd)/Rpi_Crons/daily_restart.service /etc/systemd/system/
	sudo cp $(pwd)/Rpi_Crons/daily_restart.timer /etc/systemd/system/
	sudo cp $(pwd)/Rpi_Crons/loveletter_extraction.service /etc/systemd/system/
	sudo cp $(pwd)/Rpi_Crons/loveletter_extraction.timer /etc/systemd/system/
	add_or_replace_variable "WorkingDirectory" "$(pwd)/loveletter" "/etc/systemd/system/loveletter.service"
	add_or_replace_variable "ExecStart" "$(pwd)/loveletter/start.sh" "/etc/systemd/system/loveletter.service"
	add_or_replace_variable "WorkingDirectory" "$(pwd)/LoveLetterExtraction" "/etc/systemd/system/loveletter_extraction.service"
	add_or_replace_variable "ExecStart" "$(pwd)/LoveLetterExtraction/run.sh" "/etc/systemd/system/loveletter_extraction.service"

	sudo systemctl daemon-reload
	sudo systemctl enable loveletter.service
	sudo systemctl start loveletter.service
 	sudo systemctl enable daily_restart.timer
  	sudo systemctl start daily_restart.timer
	sudo systemctl enable loveletter_extraction.timer
	sudo systemctl start loveletter_extraction.timer

	clean_dir "$repo_crons"
	rm -rf "install.sh"
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

        # Upgrade pip first
        #echo "Upgrading pip to the latest version..."
        if python3 -m pip install --upgrade pip &>/tmp/pip_install_log; then
            echo "✅ pip successfully upgraded."
        else
            echo "❌ Failed to upgrade pip."
            echo "Error log:"
            #cat /tmp/pip_install_log
            return 1
        fi

		#deactivate
    else
        echo "Error: $requirements_file not found."
        return 1
    fi
}

repo_install(){
	clean_dir "$repo"
	clone_repo $INSTALL_VER $repo
	cd loveletter
	chmod +x $(pwd)/start.sh
	
	echo -e "\n__________ Python version Avalaible: $(python3 --version)  ________"
	
	python3 -m venv env
	source env/bin/activate

	install_requirements "requirements.txt"
	cd ..
}

clines(){
	local lines_to_clear=$1
    for ((j=0; j<lines_to_clear; j++)); do
        tput cuu1
        tput el
    done
}


pendrive_check(){
	if [ -d "$(pwd)/loveletter" ]; then
		mountpoint=$(df "$(pwd)/loveletter" | tail -1 | awk '{print $1}')
		if grep -q "$mountpoint" /proc/mounts && grep -q "/media/" <<< "$(pwd)"; then
			echo "Se detectó una instalacion en un dispositivo externo."
			echo "Mountpoint: $mountpoint"
			echo "Configurando RPI y service files..."
			#echo "PARTUUID=$(sudo blkid | grep 'LABEL=\"pollen\"' | sed -n 's/.*PARTUUID=\"\([^\"]*\)\".*/\1/p') /media/pi/pollen ext3 defaults,noatime 0 0" | sudo tee -a /etc/fstab
			if grep -q '/media/pi/pollen' /etc/fstab; then
				#sudo sed -i "\|/media/pi/pollen|c\PARTUUID=$(sudo blkid | grep 'LABEL=\"pollen\"' | sed -n 's/.*PARTUUID=\"\([^\"]*\)\".*/\1/p') /media/pi/pollen ext3 defaults,noatime 0 0" /etc/fstab
				#sudo sed -i "\|/media/pi/pollen|c\PARTUUID=$(sudo blkid | grep 'LABEL=\"pollen\"' | sed -n 's/.*PARTUUID=\"\([^\"]*\)\".*/\1/p') /media/pi/pollen ext3 defaults,noatime,nofail,x-systemd.automount 0 0" /etc/fstab
				sudo sed -i "\|/media/pi/pollen|c\PARTUUID=$(sudo blkid | grep 'LABEL=\"pollen\"' | sed -n 's/.*PARTUUID=\"\([^\"]*\)\".*/\1/p') /media/pi/pollen ext3 nofail,x-systemd.device-timeout=1 0 2" /etc/fstab
			else
				#echo "PARTUUID=$(sudo blkid | grep 'LABEL=\"pollen\"' | sed -n 's/.*PARTUUID=\"\([^\"]*\)\".*/\1/p') /media/pi/pollen ext3 defaults,noatime 0 0" | sudo tee -a /etc/fstab
				#echo "PARTUUID=$(sudo blkid | grep 'LABEL=\"pollen\"' | sed -n 's/.*PARTUUID=\"\([^\"]*\)\".*/\1/p') /media/pi/pollen ext3 defaults,noatime,nofail,x-systemd.automount 0 0" | sudo tee -a /etc/fstab
				echo "PARTUUID=$(sudo blkid | grep 'LABEL=\"pollen\"' | sed -n 's/.*PARTUUID=\"\([^\"]*\)\".*/\1/p') /media/pi/pollen ext3 nofail,x-systemd.device-timeout=1 0 2" | sudo tee -a /etc/fstab
			fi
			add_or_replace_variable "WantedBy" "media-pi-pollen.mount" "/etc/systemd/system/loveletter.service"
			#ConditionPathExists=/media/pi/pollen/loveletter/start.sh
			grep -q 'ConditionPathExists' /etc/systemd/system/loveletter.service && sudo sed -i "s|^ConditionPathExists.*|ConditionPathExists=$(pwd)/loveletter/start.sh|" /etc/systemd/system/loveletter.service || sudo sed -i "/^After=graphical.target$/a ConditionPathExists=$(pwd)/loveletter/start.sh" /etc/systemd/system/loveletter.service
			sudo systemctl daemon-reexec
			sudo systemctl daemon-reload
			sudo systemctl enable loveletter.service
			sudo systemctl start loveletter.service
			echo 'ACTION=="add", SUBSYSTEM=="block", KERNEL=="sd[a-z][0-9]", RUN+="/usr/bin/systemctl restart loveletter.service"' | sudo tee /etc/udev/rules.d/99-usb-restart-loveletter.rules > /dev/null
			sudo udevadm control --reload-rules
		else
			echo ""
		fi
	else
		echo "Se detectó un problema en la instalación"
	fi
	# Previa solucion para ocultar las notificaicones de Unidad externa montada"
	#dconf write /org/gnome/desktop/media-handling/automount false
	#dconf write /org/gnome/desktop/media-handling/automount-open false
}

eth0_config(){
	sudo nmcli con mod "Wired connection 1"   ipv4.method manual   ipv4.addresses 169.254.1.3/24   ipv4.gateway 169.254.1.1
	sudo nmcli con mod "Wired connection 1" ipv4.route-metric 800
	sudo nmcli connection down "Wired connection 1" && sudo nmcli connection up "Wired connection 1"
}

loveletter_extraction(){
	#sudo hostnamectl set-hostname "$Boat"
 	clean_dir "$repo_extraction"
	clone_repo $extract_tag $repo_extraction
	cd LoveLetterExtraction
	sudo apt install sqlite3 -y
	sudo apt install gawk -y
	sqlite3 extraction_log.db < dates.sql
	mkdir keys
	python3 -m venv env
	source env/bin/activate
	install_requirements "requirements.txt"
	chmod +x $(pwd)/run.sh
	cd ..
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
	#read -p 'Por favor, ingrese el nombre del Barco: ' Boat

	if [[ "$response" -gt "$i" ]]; then
    	echo -e "    Tag selected: ($response) no exist"
	elif [[ "$response" -eq 0 ]]; then
		response=i
		INSTALL_VER=${tags[response-1]}
		log_stated_install
		repo_install
		loveletter_service
		pendrive_check
		loveletter_extraction
		eth0_config
	else
		INSTALL_VER=${tags[response-1]}
		log_stated_install
		repo_install
		loveletter_service
		pendrive_check
		loveletter_extraction
		eth0_config
	fi
fi

echo -e "\e[34m\nInstall completed successfully (Branch/Tag: $INSTALL_VER)\e[0m"
tput civis
read -p "" input
tput cnorm
