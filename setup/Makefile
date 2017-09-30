temp/m.svg: temp/endpoints.json Makefile mk_svg.py
	python3 mk_svg.py $< > $@

temp/endpoints.json: temp/paths.json Makefile find_endpoints.py
	python3 find_endpoints.py $< > $@

temp/paths.json: temp/shapes.json Makefile find_paths.py
	python3 find_paths.py $< > $@

temp/shapes.json: temp/shapes.txt Makefile mk_json.py
	python3 mk_json.py $< > $@

temp/shapes.txt: ../app/src/main/res/raw/opendata_ttc_schedules.zip Makefile
	unzip -o $< shapes.txt -d temp
	touch temp/shapes.txt
