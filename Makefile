dev:
	fastapi dev src/app.py --port 8004

docker-build:
	docker buildx build --platform linux/amd64 -t custom-document-analyser:latest .

docker-run:
	docker run --env-file .env.development -it -p 8004:8080 custom-document-analyser:latest