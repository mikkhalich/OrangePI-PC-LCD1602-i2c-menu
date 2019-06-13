#!/usr/bin/env bash

sudo ifconfig | grep Bcast | awk '{print $2}'
