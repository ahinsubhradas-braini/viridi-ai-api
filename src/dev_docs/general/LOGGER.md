1.Our FastAPI code logs with logging → stdout (JSON lines).

2.Docker captures stdout as container logs.

3.Promtail discovers containers via Docker socket, decodes the Docker JSON, parses your JSON log line, and attaches labels.

4.Loki stores the logs.

5.Grafana queries Loki and renders them.

6.docker-compose logs -f loki

docker-compose logs -f promtail

Go to grafana dashboard go to explore add loki in data source > url: http://loki:3100 > In grafana explore: {job="fastapi-app",level:"INFO"}