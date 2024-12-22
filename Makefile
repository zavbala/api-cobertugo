dev:
	uvicorn app.main:app --reload

build:
	docker build -t cobertugo .

docker:
	docker run -p 8000:8000 cobertugo