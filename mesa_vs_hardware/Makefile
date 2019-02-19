NETWORK_ADAPTER=wlp0s20f3
export HOST="10.43.105.150"

up: down
	docker-compose -f docker-compose.yaml up

down: network_reset
	docker-compose -f docker-compose.yaml down

network_reset:
	sudo tc qdisc delete dev ${NETWORK_ADAPTER} root || true

network_latency: network_reset
	@echo "Usage: make network_latency latency=200"
	# creates a delay of 300ms with a random 20ms variation
	sudo tc qdisc add dev ${NETWORK_ADAPTER} root netem delay ${latency}ms 5ms 25% distribution normal

network_loss_and_corruption: network_reset
	# create loss and corruption
	sudo tc qdisc add dev ${NETWORK_ADAPTER} root netem loss 10% corrupt 5%

network_limit_bandwidth: network_reset
	@echo "Usage: make network_limit_bandwith bandwidth=1mbit"
	sudo tc qdisc add dev ${NETWORK_ADAPTER} root handle 1:0 htb default 10
	sudo tc class add dev ${NETWORK_ADAPTER} parent 1:0 classid 1:10 htb rate ${bandwidth}

network_very_bad_conditions: network_reset
	@echo "Usage: make network_limit_bandwith bandwidth=1mbit latency=20"
	sudo tc qdisc add dev ${NETWORK_ADAPTER} root handle 1:0 htb default 10
	sudo tc class add dev ${NETWORK_ADAPTER} parent 1:0 classid 1:10 htb rate ${bandwidth}
	sudo tc qdisc add dev ${NETWORK_ADAPTER} parent 1:10 handle 10:0 netem delay ${latency}ms 5ms 25% distribution normal
