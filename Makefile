run:
	python3 -u manage.py run

migrate:
	if  [ -n '${POSTGRES_URL}' ];then \
			yoyo apply --database ${POSTGRES_URL}; \
	else \
			yoyo apply; \
	fi

