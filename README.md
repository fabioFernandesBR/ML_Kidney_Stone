# ML_Kidney_Stone
Sprint Engenharia de Sistemas de Software Inteligentes - Modelo ML embarcado em full stack para Predição de Pedra nos Rins

Este repositório contém códigos, dados e outros materiais referentes ao projeto de modelo de machine learning embarcado em backend para predição da existência de pedra nos rins (litíase renal) a partir de um conjunto de medidas disponíveis em exame de urina. O projeto contém diretórios para o seguinte conteúdo:
- 1 dataset com as seguintes características: 6 atributos + 1 variável target (0 = não tem pedra, 1 = tem pedra), 79 instâncias. O dataset neste repositório é uma cópia do dataset disponível em https://www.kaggle.com/datasets/harshghadiya/kidneystone.
- 1 link para o notebook Google Colab onde o modelo de machine learning foi criado. 4 modelos de classificação foram utilizados: KNN, Naive Bayes, Árvore de Decisão e SVM. O modelo com melhor acurácia foi o SVM com dados padronizados. O modelo SVM com hiperparâmetros otimizados e o scaler de padronização dos dados foram exportados para utilização no back-end de forma embarcada.
- 1 front-end para entrada de dados e recebimento de resposta.
- 1 back-end em flask que incorpora o modelo SVM e o respectivo scaler. Para este backend foi implementada também uma rotina de testes automatizados.

Os diretórios acima mencionados contém arquivos readme específicos.
