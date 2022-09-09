# HTTPBin

[![Issues](https://img.shields.io/github/issues/X3NNY/requestbin)](https://img.shields.io/github/issues/X3NNY/requestbin)
[![Stars](https://img.shields.io/github/stars/X3NNY/requestbin)](https://img.shields.io/github/stars/X3NNY/requestbin)
![License](https://img.shields.io/github/license/X3NNY/requestbin)

* HTTPBin is a network tool provides request record service and custom route responses.

    You can public service that we deployed on the internet, but not at now.

    **Site**: [http://httpbin.icu/](http://httpbin.icu/) (future)

## Intro

1. HTTPBin support multi-user use online as the same time.
2. You can turn on/off recording manually.
3. It can automatically analyze data parameters and dump to disk.
4. It can filter and batch export raw content.
5. It supports custom multiple specified route response content.

## Usage

* You can clone this repo and build it on local machine via docker, another way to get simple is by following the command

    ```bash
    docker pull xenny/httpbin
    ```

* Next, you need complete some necessary pre-steps before running it.

    1. Prepare a VPS with docker server
    2. Prepare a domain with full DNS control
    3. Add a new DNS **A** record to bind the VPS IP (e.g. httpbin.icu ----> xxx.xxx.xxx.xxx)
    4. Add an **A** record for all subdomain (e.g. *.httpbin.icu ----> xxx.xxx.xxx.xxx)

* Finally, just run with next command.

    ```bash
    docker run -it -p 80:80 -e HOST=your.domain xenny/httpbin
    ```

* As it, you can also running it natively when you DNS record is right done.(Remember to modify the host in `settings.py`)

    ```bash
    pip install -r requirements.txt
    python main.py
    ```

## Future

1. IP Mode support
2. DNS log support
3. Custom response headers
4. Your issues:)

## Feedback&BUG&Contribute

* If you have any other idea/problem in usage, you can create an issues or pull-request and describe it in much detail.

## Thanks

* Test: [@Airrudder](https://github.com/Airrudder)