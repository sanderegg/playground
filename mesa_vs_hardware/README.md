# Mesa vs Hardware demo

## installation

```bash
git clone https://github.com/sanderegg/playground.git
```

## configuration

1. Edit Makefile and define HOST variable to the external IP of computer serving paraviewweb
2. On server run

```bash
cd playground/mesa_vs_hardware
make up
```

3. On client open browser at [nvidia powered browser](http://HOST:8888/visualizer)
4. On client open browser at [mesa powered browser](http://HOST:8889/visualizer)

## add delay, bandwidth limitations

1. On server open a terminal and run

```bash
cd playground/mesa_vs_hardware
# to set a latency in ms
make network_latency latency=100
# to set a bandwidth limitation
make network_limit_bandwidth bandwidth=1mbit
# to set both latency and bandwidth
make network_very_bad_conditions latency=100 bandwidth=1mbit
# to reset the limitations
make netowrk_reset
```