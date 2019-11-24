db_up:
	docker-compose -f docker-compose.db.yml up -d

db_stop:
	docker-compose -f docker-compose.db.yml stop

db_status:
	docker-compose -f docker-compose.db.yml ps
