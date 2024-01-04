# flappy-bird-with-IA
Criação do jogo Flappy Bird utilizando a biblioteca pygame e aplicação de inteligencia artificial para aprender a jogar, 
a inteligência ultiliza o algoritmo de rede neural 'NEAT'

## Funcionalidades

- Jogar flappy bird com o teclado 
- Utilizar do algoritmo "NEAT" para ensinar uma rede neural a jogar

## Rede Neural Jogando

<img src="https://github.com/lucasarauj0h/flappy-bird-with-IA/blob/main/movies/learning.gif">

Usando uma população de 10 passáros por geração, foi necessário 8 gerações para que a rede neural aprende-se por completo a jogar.

 Quando alterada a população por geração (adicionando 100 passáros por geração, por exemplo) a rede neural aprende a zerar as vezes na 1º geral, mas geralmente aprende na 2º ou 3º geração.

Por se tratar de um jogo com uma mecânica simples, a rede neural consegue facilmente compreender e se adaptar ao padrão do jogo, uma vez que não há tantas váriaveis como obstáculo.
Portanto, algumas das ideias que futuramente será implementada no jogo é:

Mecânicas que dificulte o aprendizado da rede neural para melhorar seus parametros
- Aumentar velocidade do jogo a medida em que se progride.
- Variar a largura dos canos para que a rede neural se adapte
- Fazer com que os canos se movam também para cima e para baixo, fazendo com que a que a rede neural se adapte



## Aprendizados

Neste projeto me apronfudei em conceitos de POO-python e passo a entender alguns conceitos de redes neurais

## Instalação

Instale a biblioteca pygame e neat-python. Para jogar manualmente altere a variavel "ai_jogando = False" para false, localizado na linha 7 do código

```bash
  pip install pygame
  pip install neat-python
  ai_jogando = False # Para jogar manualmente
  ai_jogando = True # Para treinar a AI
```

## Rede Neural após aprender a jogar

<img src="https://github.com/lucasarauj0h/flappy-bird-with-IA/blob/main/movies/learned.gif">
    
