INSTALL_VER="beta 1.0-4"
DISPLAY_VER=$(echo $INSTALL_VER | sed "s|~alpha||g" | sed "s|~beta||g")
	echo
	echo ' __  __   ____   _______   ____   _____   ______   _____             __  __            ______  ____   _   _             _____ '
	echo '|  \/  | / __ \ |__   __| / __ \ |  __ \ |  ____| / ____|     /\    |  \/  |    /\    |___  / / __ \ | \ | |    /\     / ____|'
	echo '| \  / || |  | |   | |   | |  | || |__) || |__   | (___      /  \   | \  / |   /  \      / / | |  | ||  \| |   /  \   | (___  '
	echo '| |\/| || |  | |   | |   | |  | ||  _  / |  __|   \___ \    / /\ \  | |\/| |  / /\ \    / /  | |  | || . ` |  / /\ \   \___ \ '
	echo '| |  | || |__| |   | |   | |__| || | \ \ | |____  ____) |  / ____ \ | |  | | / ____ \  / /__ | |__| || |\  | / ____ \  ____) |'
    echo '|_|  |_| \____/    |_|    \____/ |_|  \_\|______||_____/  /_/    \_\|_|  |_|/_/    \_\/_____| \____/ |_| \_|/_/    \_\|_____/ '
	echo "                                                                        "
	echo "                                                  LOVELETTER INSTALLER                       "
	if [[ "$INSTALL_VER" =~ "beta" ]]; then
	    echo "                                                      BETA RELEASE                       "
	fi
	if [[ "$INSTALL_VER" =~ "alpha" ]]; then
		echo "                                                  DEVELOPMENT SNAPSHOT                      "
		echo "                                             OT INTENDED FOR PRODUCTION USE                 "
		echo "                                                  USE AT YOUR OWN RISK                      "
	fi
	echo "                                                       ${INSTALL_VER}                           "

echo "$(git ls-remote --tags https://github.com/KaraSolar/loveletter.git)"