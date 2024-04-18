include .env
SELDON_NAMESPACE?=$(SELDON_NAMESPACE)
KUBECONFIG_FILE=--kubeconfig=cluster-admin-config.txt

# Connect to kubectl
# kubectl --kubeconfig=cluster-admin-config.txt get pods -n seldon-mesh

run-ui:
	streamlit run streamlit/app.py
deploy:
	kubectl $(KUBECONFIG_FILE) create -f deployment/models.yaml -n $(SELDON_NAMESPACE)
	kubectl $(KUBECONFIG_FILE) wait --for condition=ready --timeout=300s model --all -n $(SELDON_NAMESPACE)
	kubectl $(KUBECONFIG_FILE) apply -f deployment/pipeline.yaml -n $(SELDON_NAMESPACE)
	kubectl $(KUBECONFIG_FILE) wait --for condition=ready --timeout=300s pipeline --all -n $(SELDON_NAMESPACE)

upload_deploy:
	kubectl $(KUBECONFIG_FILE) delete -f deployment/models.yaml -n $(SELDON_NAMESPACE)
	kubectl $(KUBECONFIG_FILE) apply -f deployment/pipeline.yaml -n $(SELDON_NAMESPACE)

undeploy:
	kubectl $(KUBECONFIG_FILE) delete -f deployment/models.yaml -n $(SELDON_NAMESPACE)
	kubectl $(KUBECONFIG_FILE) delete -f deployment/pipeline.yaml -n $(SELDON_NAMESPACE)

delete_models:
	kubectl $(KUBECONFIG_FILE) delete -f deployment/models.yaml -n $(SELDON_NAMESPACE)

delete_pipeline:
	kubectl $(KUBECONFIG_FILE) delete -f deployment/pipeline.yaml -n $(SELDON_NAMESPACE)

create-secret:
	kubectl $(KUBECONFIG_FILE) delete secret artifact-registry -n $(SELDON_NAMESPACE) || echo "image pull secret does not exist - will create"
	kubectl $(KUBECONFIG_FILE) create secret docker-registry artifact-registry \
	--docker-server=europe-west2-docker.pkg.dev \
	--docker-email=dev-athorne@dev-athorne.iam.gserviceaccount.com \
	--docker-username=_json_key \
	--docker-password="$$(cat ../../setup/gcloud-application-credentials.artifact-registry.json)" \
	-n $(SELDON_NAMESPACE)

release-job:
	docker build deployment/jobs/create_vdb -t joshsgoldstein/create-vdb-job:latest
	docker push joshsgoldstein/create-vdb-job:latest

create-jobs:
	kubectl $(KUBECONFIG_FILE) apply -f ./deployment/jobs/create_vdb/job.yml -n $(SELDON_NAMESPACE)

delete-jobs:
	kubectl $(KUBECONFIG_FILE) delete -f deployment/jobs/create_vdb/job.yml -n $(SELDON_NAMESPACE)

pack:
	sh make-state-env.sh
