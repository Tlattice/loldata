.PHONY: fetch transform make_classify_model make_training_data visualize_classification tables normalize

export PYTHONPATH=lib:lib/growing_hierarchical_som:$PYTHONPATH

all: output/predictive_model.model

visualize_classification:
	python3 visualization/classification_model_stats.py

fetch:
	python3 extract/fetch.py

transform:
	python3 transform/collect_markers.py

make_classify_model:
	python3 train/data_classify.py

make_training_data:
	python3 train/make_data.py

train_model:
	python3 train/neural_network.py


output/results.json : input/markers.ini
	python3 transform/collect_markers.py

output/classify_model.model : output/results.json
	python3 train/data_classify.py

output/training_data.pkl : output/classify_model.model
	python3 train/make_data.py

output/predictive_model.model : output/training_data.pkl
	python3 train/neural_network.py

tables:
	python3 transform/tables.py

normalize:
	python3 transform/normalize.py
