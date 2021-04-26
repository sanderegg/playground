# original docker socket on host

```console
rw-rw---- 1 root docker 0 mar 23 08:10 /var/run/docker.sock
```

## change mod on docker.sock

```console
chmod 777 /var/run/docker.sock
```

looks like this afterwards

```console
srwxrwxrwx 1 root docker 0 mar 23 08:10 /var/run/docker.sock
```

need to add this to the docker-compose in order for dockeroperator to work

original access rights
```console
srw-rw---- 1 root docker 0 Apr  9 16:37 /var/run/docker.sock
```


```yaml
AIRFLOW__CORE__ENABLE_XCOM_PICKLING: 'true'
```