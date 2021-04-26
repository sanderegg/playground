#!/bin/bash
doit() {
    curl -s -o /dev/null -w "%{http_code} - %{time_total}s\n" 'http://127.0.0.1:9081/v0/projects?type=all&state=active' \
    -H 'Connection: keep-alive' \
    -H 'Pragma: no-cache' \
    -H 'Cache-Control: no-cache' \
    -H 'sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"' \
    -H 'accept: application/json' \
    -H 'sec-ch-ua-mobile: ?0' \
    -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36' \
    -H 'Sec-Fetch-Site: same-origin' \
    -H 'Sec-Fetch-Mode: cors' \
    -H 'Sec-Fetch-Dest: empty' \
    -H 'Referer: http://127.0.0.1:9081/dev/doc' \
    -H 'Accept-Language: en-US,en;q=0.9' \
    -H 'Cookie: adminer_key=f70327f90dbb00a8c697c933a32bbd24; _ga=GA1.1.1164697573.1596089800; _pk_id.1.dc78=3bc4017fe41ce1b3.1598967593.; _xsrf=2|c9c1015c|4cc66909cafefb2882de969e58f09aa4|1613982430; osparc.WEBAPI_SESSION="gAAAAABgTyx35utztzbL4WHmBhDAhjnMOz4FbTBKDiWHcCB97Q6ScucrxGveO39zaoXq4Av4i6iaDKnw1lIXtMTF6gStAZ7_cBTB7pGebXYKfmk7QaeBkEhU1QZjwnQr_kDldrLlROEC_0Ix2ntS2jQK3oHg3qZz_QMHNm5Ri_nwIR-Lwwm7eNY="; user=anderegg@itis.swiss; adminer_sid=f091b10a4383a59dc8593c5de85ecdaa; adminer_permanent=cGdzcWw%3D-cG9zdGdyZXM%3D-YWRtaW4%3D-dGVzdA%3D%3D%3Aa7x8OoLd3eqJCAKu%2BcGdzcWw%3D-cG9zdGdyZXM%3D-c2N1-c2ltY29yZWRi%3AwLJfeCwqtZqCaXHsyuXFxQ%3D%3D%2BcGdzcWw%3D-cG9zdGdyZXM%3D-c2N1-c2ltY29yZWRi%3AwLJfeCwqtZqCaXHsyuXFxQ%3D%3D%2BcGdzcWw%3D-cG9zdGdyZXM%3D-c2N1-c2ltY29yZWRi%3AwLJfeCwqtZqCaXHsyuXFxQ%3D%3D+cGdzcWw%3D-cG9zdGdyZXM%3D-c2N1-c2ltY29yZWRi%3AMPBAMB4Ev%2F998eSTpbMe3A%3D%3D; _pk_ses.1.dc78=1; io=72b46316ea2a4bd2b2b06af5fdccb380' \
    --compressed
}
export -f doit

while true; do
echo $(date +"%H:%M:%S.%N") $(doit)
# seq 10 | parallel --progress -n0 doit
done
