FROM python:3-slim

COPY ./src/ /app

WORKDIR /app

# China 
RUN sed -i 's#http://deb.debian.org#https://mirrors.ustc.edu.cn#g' /etc/apt/sources.list && \
    sed -i 's|security.debian.org/debian-security|mirrors.ustc.edu.cn/debian-security|g' /etc/apt/sources.list && \
    mkdir ~/.pip && \
    echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple/" > ~/.pip/pip.conf

RUN pip install -r requirements.txt

COPY run.sh /

RUN chmod +x /run.sh

ENV HOST=httpbin.icu

EXPOSE 80

CMD ["/run.sh"]
