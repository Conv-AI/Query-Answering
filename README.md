# Google-Custom-Search-API-Experiment
Experiments on API

##Commands:
build the image :
sudo docker build -t query_ans .

create+run the container :
sudo docker run --name query_ans_api -p 9010:9050 query_ans

sudo docker build -t query_ans . && sudo docker run --name query_ans_api -p 9010:9600 query_ans

sudo docker run -it query_ans bash