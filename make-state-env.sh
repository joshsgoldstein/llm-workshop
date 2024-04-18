python3 -m venv state-venv
. state-venv/bin/activate
pip install qdrant-client redis venv-pack
venv-pack -o deployment/models/vdb/state-env.tar.gz
cp deployment/models/vdb/state-env.tar.gz deployment/models/update_state/state-env.tar.gz
rm -rf state-venv
