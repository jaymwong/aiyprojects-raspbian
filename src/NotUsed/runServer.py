#!/usr/bin/env
import json

from bottle import run, post, request, response

def main():
	print('Running...')


run(host='localhost', port=8080, debug=True)

if __name__ == '__main__':
    main()
