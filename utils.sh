DM_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
WO_DIR=/opt/google-trends-wrapper
DK_IMG=google-trends-wrapper-env

while :
	do
    echo "1. Build image"
	echo "2. Cheatsheet"
	echo "3. Get data"
	echo "4. EXIT"
	echo -n "Choose one option [1 - 3]: "
	read opcion

function build_dev_image () {
	docker build -t "${DK_IMG}" "${DM_DIR}"/Docker/
}

function show_cheatsheet () {
	docker run --rm -it -v  "${DM_DIR}":"${WO_DIR}" --network host "${DK_IMG}" Rscript "${WO_DIR}"/generate_design.R run
}

function get_data () {
    sudo nano ./conf/conf.json
	docker run -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 --rm -it -v  "${DM_DIR}":"${WO_DIR}" --network host "${DK_IMG}" python3 "${WO_DIR}"/pytrends_wrapper.py run
}

case $opcion in
	1)
		build_dev_image
		;;
	2)
		show_cheatsheet
		;;
	3)
		get_data
		;;
	4)
		echo "bye";
		exit 1
		;;
esac
done