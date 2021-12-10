#!/bin/bash
lektor build --output-path build

python renametocfm.py
