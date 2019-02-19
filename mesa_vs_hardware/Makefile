NETWORK_ADAPTER=wlp0s20f3

up: down
	docker-compose -f docker-compose.yaml up

down: network_reset
	docker-compose -f docker-compose.yaml down

network_reset:
	sudo tc qdisc delete dev ${NETWORK_ADAPTER} root

network_latency: network_reset
	# creates a delay of 300ms with a random 20ms variation
	sudo tc qdisc add dev ${NETWORK_ADAPTER} root netem delay 300ms 20ms

network_loss_and_corruption: network_reset
	# create loss and corruption
	sudo tc qdisc add dev ${NETWORK_ADAPTER} root netem loss 10% corrupt 5%

network_limit_bandwith: network_reset
	sudo tc qdisc add dev ${NETWORK_ADAPTER} root tbf rate 1mbit burst 32kbit latency 400ms

network_very_bad_conditions: network_reset
	sudo tc qdisc add dev ${NETWORK_ADAPTER} root tbf rate 1mbit burst 32kbit latency 400ms delay 300ms 20ms loss 10% corrupt 5%
