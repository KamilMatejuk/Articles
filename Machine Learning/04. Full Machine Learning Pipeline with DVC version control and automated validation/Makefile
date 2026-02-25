NAME=pipeline

build:
	docker compose -p $(NAME) build

mlflow:
	docker compose -p $(NAME) up mlflow

dvc_init:
	CMD="dvc init" \
	docker compose -p $(NAME) up main

dvc_remote:
	CMD=" \
		dvc remote add -d -f drive gdrive://1TZ7rrf8RBINIh9Z6byJ6r3518_FixOtg && \
		dvc remote default drive" \
	docker compose -p $(NAME) up main

dvc_deinit:
	CMD=" \
		mv dvc.yaml dvc.yaml.temp && \
		rm dvc.lock && \
		dvc destroy -f && \
		mv dvc.yaml.temp dvc.yaml" \
	docker compose -p $(NAME) up main

dvc_status:
	CMD="dvc status" \
	docker compose -p $(NAME) up main

dvc_reproduce:
	CMD="rm -f .dvc/tmp/rwlock && dvc repro --no-run-cache" \
	docker compose -p $(NAME) up main

dvc_exp_compare_model:
	CMD='\
		dvc experiments run -f --name classifier-strategy-1 --set-param "dummy_classifier.strategy=most_frequent" && \
		dvc experiments run -f --name classifier-strategy-2 --set-param "dummy_classifier.strategy=uniform" && \
		dvc experiments show --only-changed' \
	docker compose -p $(NAME) up


dvc_exp_data_usage_for_train:
	CMD='\
		dvc experiments run -f --name train-cols-all --set-param "train_use_cross_validation=True" --set-param "dataset_train_usage=all" && \
		dvc experiments run -f --name train-cols-text --set-param "train_use_cross_validation=True" --set-param "dataset_train_usage=text" && \
		dvc experiments run -f --name train-cols-numeric --set-param "train_use_cross_validation=True" --set-param "dataset_train_usage=numeric" && \
		dvc experiments show --only-changed' \
	docker compose -p $(NAME) up

dvc_exp_model:
	CMD='\
		dvc experiments run -f --name model-svm   --set-param "train_use_cross_validation=True" --set-param "selected_model=svm" && \
		dvc experiments run -f --name model-rf    --set-param "train_use_cross_validation=True" --set-param "selected_model=random_forest" && \
		dvc experiments run -f --name model-dummy --set-param "train_use_cross_validation=True" --set-param "selected_model=dummy" && \
		dvc experiments show --only-changed' \
	docker compose -p $(NAME) up

dvc_exp_dimention_reduction:
	CMD='\
		dvc experiments run -f --name red-pca-3   --set-param "dataset_train_reduction=pca"  --set-param "dataset_train_reduction_dim=3" && \
		dvc experiments run -f --name red-pca-9   --set-param "dataset_train_reduction=pca"  --set-param "dataset_train_reduction_dim=9" && \
		dvc experiments run -f --name red-umap-3  --set-param "dataset_train_reduction=umap" --set-param "dataset_train_reduction_dim=3" && \
		dvc experiments run -f --name red-umap-9  --set-param "dataset_train_reduction=umap" --set-param "dataset_train_reduction_dim=9" && \
		dvc experiments show --only-changed' \
	docker compose -p $(NAME) up

dvc_exp_grid_search:
	CMD='\
		dvc experiments run -f --name gs-random         --set-param "grid_search.engine=RandomSearch" && \
		dvc experiments run -f --name gs-grid           --set-param "grid_search.engine=GridSearch" && \
		dvc experiments run -f --name gs-halving-random --set-param "grid_search.engine=HalvingRandomSearch" && \
		dvc experiments run -f --name gs-halving-grid   --set-param "grid_search.engine=HalvingGridSearch" && \
		dvc experiments show --only-changed' \
	docker compose -p $(NAME) up

dvc_exp_vectorization:
	CMD='\
		dvc experiments run -f --name vect-bow      --set-param "preprocessing.vectorization=bow" && \
		dvc experiments run -f --name vect-tfidf    --set-param "preprocessing.vectorization=tf-idf" && \
		dvc experiments run -f --name vect-word2vec --set-param "preprocessing.vectorization=word2vec" && \
		dvc experiments show --only-changed' \
	docker compose -p $(NAME) up

dvc_push:
	CMD="dvc push" \
	docker compose -p $(NAME) up main

dvc_pull:
	CMD="dvc pull" \
	docker compose -p $(NAME) up main

jupyter:
	CMD="./start_jupyter.sh" \
	docker compose -p $(NAME) up main
