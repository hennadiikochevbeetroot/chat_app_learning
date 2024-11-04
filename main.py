from core.server.server import run_server


import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--server', action='store_true', help='Run Chat Server')
parser.add_argument('-c', '--client', action='store_true', help='Run Chat client')

args = parser.parse_args()

if args.server:
    run_server()
elif args.client:
    print('Client!!')
