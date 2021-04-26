OUTPUT_PDF?=report.pdf
GF_DASHBOARD_UID?=j3-z2TRMz
GF_API_TOKEN?=eyJrIjoiejNXUUlRbTFrdjZFbVd4NjJBNFREZjI3VG9jTUdwYTMiLCJuIjoicmVwb3J0ZXIiLCJpZCI6MX0=
GF_HOST?=https://osparc01.speag.com/grafana
GF_PROTO?=https

report:  ## create pdf report
	docker run \
		-v "$(realpath $(CURDIR)):/output" \
		izakmarais/grafana-reporter \
		-cmd_enable=1 \
		-cmd_apiKey="$(GF_API_TOKEN)"
		-ip $(GF_HOST) \
		-proto $(GF_PROTO) \
		-grid-layout=1 \
		-cmd_dashboard $(GF_DASHBOARD_UID) \
		-cmd_ts from=now-1y \
		-cmd_apiVersion v5 \
		-cmd_o /output/$(OUTPUT_PDF)
