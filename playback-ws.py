import argparse
import asyncio
import json

import pandas as pd
import websockets

prev_ts = None


def load_data(path):
    if args.time_format == "ms":
        data = pd.read_csv(path, index_col=0)
    else:
        data = pd.read_csv(path, index_col=0, parse_dates=True)
    data = data.iterrows()
    return data


def delta(ts):
    global prev_ts
    delay = None

    if prev_ts is not None:
        if args.time_format == "ms":
            delay = (ts - prev_ts) / 1000
        else:
            delay = (ts - prev_ts).total_seconds()
    prev_ts = ts
    return delay


async def stream_handler(websocket, path):
    while True:
        message = await stream_data()
        await websocket.send(message)


async def stream_data():
    row = next(data)
    ts = row[0]
    sensor_data = json.dumps(row[1].to_dict())

    delay = delta(ts)
    #print(f'> {delay}')

    if delay is not None:
        await asyncio.sleep(delay)

    #print(f'> {sensor_data}')
    return sensor_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=None,
                        help="Data file")
    parser.add_argument("--time_format", default="ms",
                        help="Timestamp format"),
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip of the server")
    parser.add_argument("--port", type=int, default=8081,
                        help="The port the server is listening on")
    args = parser.parse_args()

    data = load_data(args.data)

    start_server = websockets.serve(stream_handler, args.ip, args.port)
    asyncio.get_event_loop().run_until_complete(start_server)

    # Start websocket server.
    asyncio.get_event_loop().run_forever()
