# The census as an MCP server, for hosts that run servers from an image
# (Glama's listing check among them). Standard library only, so the base
# image is the whole dependency list. The index is read from the published
# copy on GitHub at first use, which keeps the image small and the answers
# as fresh as the last daily run.
FROM python:3.12-slim
WORKDIR /app
COPY mcp_server.py .
ENV AGENT_VITALS_REMOTE=1
ENTRYPOINT ["python3", "mcp_server.py"]
