#!/usr/bin/env python

import sys
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer, OFFSET_BEGINNING
from datetime import datetime
import datetime as dt
import json
import pandas as pd
import streamlit as st

if __name__ == '__main__':
    # Parse the command line.
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('-t', '--ticker', action='append', default=[])
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    # Parse the configuration.
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['consumer'])

    tickers = args.ticker
    print('Tickers: ', tickers)

    if len(tickers) == 0:
        print("No tickers selected")
        exit()

    # Create Consumer instance
    consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)

    # Subscribe to topic
    consumer.subscribe(tickers, on_assign=reset_offset)

    tick_list = []

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = consumer.poll(0.1)
            if msg is None:
                continue
            if msg.error():
                print("ERROR: %s" % (msg.error()))

            ticker = msg.topic()
            timestamp = msg.key().decode('utf-8')
            tick = json.loads(msg.value().decode('utf-8'))

            print("Got Tick: {topic}\nKey = {key:12}\nValue = {value:12}\n\n".format(topic=ticker, key=timestamp, value=str(tick)))
            tick_list.append({"Ticker": ticker, "Timestamp": timestamp, "High": tick["High"], "Low": tick["Low"], "Open": tick["Open"], "Close": tick["Close"], "Volume": tick["Volume"]})

            if len(tick_list) >= 100:
                df = pd.DataFrame(tick_list)
                df.to_csv("stock_ticks.csv", mode='a', header=False, index=False)  # Append to the CSV
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()

