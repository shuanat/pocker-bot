task=help

.PHONY: help
help:
	@cat $(MAKEFILE_LIST) | grep -e "^[a-zA-Z_\-]*: *.*## *" | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

download_data: ## Download pets dataset
	wget http://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz
	wget http://www.robots.ox.ac.uk/~vgg/data/pets/data/annotations.tar.gz
	tar -xvf images.tar.gz
	tar -xvf annotations.tar.gz

create_tf_record: ## Create tf record train and validation files
	mkdir -p data && \
	PYTHONPATH=$(PYTHONPATH):$(pwd):$(pwd)/slim python3 object_detection/dataset_tools/create_pet_tf_record.py \
		--label_map_path=object_detection/data/pet_label_map.pbtxt \
		--data_dir=`pwd` \
		--output_dir=`pwd` && \
	cp pet_train_with_masks.record data/pet_train.record && \
	cp pet_val_with_masks.record data/pet_val.record && \
	cp object_detection/data/pet_label_map.pbtxt data/

download_model: ## Download COCO-pretrained model for transfer learning
	wget http://storage.googleapis.com/download.tensorflow.org/models/object_detection/faster_rcnn_resnet101_coco_11_06_2017.tar.gz && \
	tar -xvf faster_rcnn_resnet101_coco_11_06_2017.tar.gz && \
	cp faster_rcnn_resnet101_coco_11_06_2017/model.ckpt.* data/

configure_pipeline: ## Configure object detection pipeline
	cp object_detection/samples/configs/faster_rcnn_resnet101_pets.config data/faster_rcnn_resnet101_pets.config && \
	sed -i "s|PATH_TO_BE_CONFIGURED|data|g" data/faster_rcnn_resnet101_pets.config

run_train: ## Start training
	mkdir -p train && \
	CUDA_VISIBLE_DEVICES=0 PYTHONPATH=$(PYTHONPATH):$(pwd):$(pwd)/slim python3 object_detection/train.py \
		--logtostderr \
		--train_dir=train \
		--pipeline_config_path=data/faster_rcnn_resnet101_pets.config

run_eval: ## Run evaluation
	mkdir -p eval && \
	CUDA_VISIBLE_DEVICES="" PYTHONPATH=$(PYTHONPATH):$(pwd):$(pwd)/slim python3 object_detection/eval.py \
		--logtostderr \
		--checkpoint_dir=train \
		--eval_dir=eval \
		--pipeline_config_path=data/faster_rcnn_resnet101_pets.config

export_model: ## Export a model
	mkdir -p exported_graphs && \
	PYTHONPATH=$(PYTHONPATH):$(pwd):$(pwd)/slim python3 object_detection/export_inference_graph.py \
		--input_type image_tensor \
		--pipeline_config_path data/faster_rcnn_resnet101_pets.config \
		--trained_checkpoint_prefix train/model.ckpt-${checkpoint} \
		--output_directory exported_graphs

notebook: ## Run jupyter notebook with python protobuf backend
	PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python jupyter notebook
