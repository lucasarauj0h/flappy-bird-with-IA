import pygame
import os
import random


# Definindo a nossa janela de game
TELA_LARGURA = 500
TELA_ALTURA = 800

# Definindo as imagens do game

# Aumentando a escala da imagem em 2x e abrindo a pasta "imgs" com a biblioteca os.
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

# Definindo a fonte do jogo
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('Arial', 50)

# Criação dos objetos 
class Passaro:
    # Criação dos atributos
    # Informações fixas do passáro
    IMGS = IMAGENS_PASSARO
    # Animações da rotação:
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5 # Definindo frames
    
    # Informações que o passaro tem que ter (posição X, Y, velocidade)
    
    def __init__(self, x, y):
        # Caracteristicas do passaro
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]
    
    def pular(self):
        # Quando o passáro pular ele terá uma velocidade inicial.
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y
        
    def mover(self):
        # Calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade*self.tempo

        # Restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2 # Testar mudanças nesse topico
            
        self.y += deslocamento
        
        # Angulo do passáro
        # Usado apenas para animação, self.altura recebe a altura de quando ele pulou
        # Colocamos um "delay" para que o passaro não mude o angulo diretamente quando
        # começar a cair, e sim após um tempinho
        if deslocamento < 0 or self.y < (self.altura+50): # Animação
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO
        
    def desenhar(self, tela):
        # Definir qual imagem do passáro vai usar
        self.contagem_imagem += 1 # A cada frame, a contagem_img aumenta
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*5 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0
    
        # Se o passáro estiver caindo, não irei bater asa (imagem fixa)
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2 
    
        # Desenhar a imagem    
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x,self.y)).center
        retangulo = imagem_rotacionada .get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)
    
    # Pegando a mascara do passaro - tempo 53:00 da aula 2
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem) 
         
class Cano:
    # Criação dos atributos
    # Distancia fixa dos canos (espaço entre eles)
    DISTANCIA = 200 #PIXEIS  
    VELOCIDADE = 5 #velocidade dos canos
    
    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO        
        self.passou = False # Verificar se o passáro já passou do cano
        self.definir_altura()
        
    # Definindo altura do cano
    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA
        
    def mover(self):
        self.x -= self.VELOCIDADE
        
    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))
        
    # Verificando se a mascára do cano está colidindo com o passáro
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)
        
        # Pegando as distancia da mascara do passaro, pro cano do topo
        # e do passaro, pro cano da base
        # x do cano - x do passaro, y do cano (pos do cano no topo) - y do passaro
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))
        
        # Verificando o ponto de colisão
        # Verifica se existe um ponto de colisão entre a mascara do cano, e a distancia
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)
        
        if base_ponto or topo_ponto:
            return True
        else: 
            return False
        

class Chao:
    # Criação dos atributos
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO
    
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA
        
    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE
        
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA
        
    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))
        
def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()    
    
def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    # Taxa de atualização de tela por segundo
    relogio = pygame.time.Clock()
    
    rodando = True
    while rodando:
        # Definindo para atualizar 30 frames por segundo.
        relogio.tick(30)
        # Fazendo o pygame identificar se você está interagindo com o jogo (por ex: apertar space)
        # Interação com o usuário
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
            
        # Fazendo as coisas se mover!
        for passaro in passaros:
            passaro.mover()
        chao.mover()
        
        adicionar_cano = False
        # Para cada cano dentro do jogo, vou percorrer varios passaros
        remover_canos = []
        for cano in canos:
            # Irei pegar a lista de passaros, contendo seu ID e seu OBJ
            for i, passaro in enumerate(passaros):
                # Se o passaro colidir, ele será removido.
                if cano.colidir(passaro):
                    passaros.pop(i) 
                    # pygame.quit()
                    # quit()
                # Verificando se o passaro passou do cano
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
                    
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)         
        
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
                
        
        desenhar_tela(tela,passaros,canos,chao,pontos)
        
if __name__ == "__main__":
    main()
        
    