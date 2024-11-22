FROM ubuntu:rolling

# copy local files
ADD py-crawler.py requirements.txt /opt/

# install python
RUN apt update && \
	apt install -y python3.12 python3.12-dev && \
	apt clean

# virtual env
RUN pip install virtualenv && \
	python -m virtualenv /opt/.venv
ENV PATH="/opt/.venv/bin/:$PATH"

# install requirements
RUN pip install --no-cache-dir -r /opt/requirements.txt && \
	rm /opt/requirements.txt

CMD ["python", "/opt/py-crawler.py"]
