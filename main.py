import random
import pygame
import janela
import pokemon
import arquivos as arq
import cores as cor
import cena
from mensagem import Mensagem
from condicao import Condicao
from acoes import Acao
from math import ceil, floor

def main():
    menu = cena.Menu()
    sub_menu = cena.Submenu()
    
    mensagem = Mensagem("TESTE")

    escala = arq.escala
    # menu espaçamento:
    
    menu_espacamento = (200,50)
    # tamanho menu:
    #menu_tamanho = 2*escala
    # tamanho seta:
    tamanho_cursor = 11*escala

    # Pokémon selecionado (tela de seleção de pokémon):
    sel_s = 0
    
    pos = [0,0]
    distanciamento = (50*escala,15*escala)
    generos = ["F", "M"]

    clock = pygame.time.Clock()
    count = 0

    condicao = Condicao()

    pk_pikachu = pokemon.Pokemon("Pikachu",35,55,40,90,50,50,9,random.choice(generos), arq.carregar_imagem_pokemon(25))
    pk_charmander = pokemon.Pokemon("Charmander",39,52,43,65,60,50,9, random.choice(generos),arq.carregar_imagem_pokemon(4))
    pk_bulbasaur = pokemon.Pokemon("Bulbasaur",45,49,49,45,65,65,9, random.choice(generos),arq.carregar_imagem_pokemon(1))
    pk_squirtle = pokemon.Pokemon("Squirtle",44,48,65,43,50,64, 9,random.choice(generos),arq.carregar_imagem_pokemon(7))
    pk_rhydon = pokemon.Pokemon("Rhydon",105,130,120,40,45,45,9,random.choice(generos),arq.carregar_imagem_pokemon(112))
    pk_gengar = pokemon.Pokemon("Gengar",60,65,60,110,130,75,9,random.choice(generos),arq.carregar_imagem_pokemon(94))
    pk_dragonite = pokemon.Pokemon("Dragonite",91,134,95,80,100,100,9, random.choice(generos),arq.carregar_imagem_pokemon(149))
    pk_mewtwo = pokemon.Pokemon("Mewtwo",106,110,90,130,154,90,9,random.choice(generos),arq.carregar_imagem_pokemon(150))
    
    pokemons_pode_escolher = [pk_pikachu, pk_charmander, pk_bulbasaur, pk_squirtle, pk_rhydon, pk_gengar, pk_dragonite, pk_mewtwo]
    cores_pode_escolher = [cor.AMARELO, cor.LARANJA, cor.VERDE, cor.AZUL, cor.CIANO, cor.ROXO, cor.ROSA, cor.CINZA]


    pokemons = [None, None]
    pk_pikachu.atacar(pk_rhydon)

    def texto_multilinha(texto):
        x = 0
        y = 0
        # s = onde está o último espaço " " 
        s = 0
        i = 0
        t = []
        while i < len(texto):
            t_local = arq.fonte_txt.render(texto[i], True, cor.BRANCO)
            
            t_rect = t_local.get_rect()
            coordenada_x = 0 + 12*escala + t_rect.width*x

            if texto[i] == " ":
                s = i

            if coordenada_x > janela.tamanho[0]/2 - t_rect.width:
                x = 0
                y -= 1
                for _ in range(i, s, -1):
                    if s < len(t): 
                        t.pop(s)
                
                i = s + 1 
                s = 0
                coordenada_x = 0 + 12*escala + t_rect.width*x
                t_local = arq.fonte_txt.render(texto[i], True, cor.BRANCO)

            t_rect.left = coordenada_x
            t_rect.bottom = janela.tamanho[1] - 28*escala - y*t_rect.height
            
            t.append([t_local, t_rect])

            x += 1
            i += 1
        for i in range(len(t)):
            janela.tela.blit(t[i][0], t[i][1])

    pygame.mixer.music.play()
    
    barra_width = arq.img_vida_vermelha.get_width() * 5.34

    def tocar_sons():
        #Musica entrada:
        if menu.atual == menu.escolhendo_pokemon:
            #arq.som_Batalha.stop()
            #arq.som_fire_red_abertura.play()
            pass
        if menu.atual == menu.batalhando:
            #arq.som_fire_red_abertura.stop()
            #arq.som_Batalha.play()
            pass
        if condicao.atual == condicao.vitoria:
            arq.som_vitoria.play()
        if condicao.atual == condicao.derrota:
            arq.som_derrota.play()
    def desenhar_graficos():
        
        #menu inicio:
        txt = "Escolha o seu pokémon" #Choose your pokémon
        
        #limpar a tela:
        janela.tela.fill(cor.PRETO)
        
        if menu.no_menu(menu.escolhendo_pokemon):
            # Fonte:
            superf = arq.fonte.render(txt, True, cor.BRANCO)
            superf_rect = superf.get_rect()
            superf_rect.center =(janela.tamanho[0]/2, 100)
            janela.tela.blit(superf, superf_rect)

            # posicao do nome que está sendo selecionado:
            

            # espacamento entre os nomes:
            e_n = 32
            # posicao y da seta dentro do retangulo:
            li = 100-e_n + (e_n*sel_s)

            # espaçamento x na esquerda da seta:
            e_s_x = 16

            # seta de seleção:
            pygame.draw.polygon(janela.tela, cor.VERMELHO, ( (menu_espacamento[0] + e_s_x, menu_espacamento[1] + li), (menu_espacamento[0] + e_s_x,menu_espacamento[1] + tamanho_cursor + li), (menu_espacamento[0] + e_s_x+ tamanho_cursor/2, menu_espacamento[1] + tamanho_cursor/2 + li) ) )
            
            # loop que vai percorrer a lista com os nomes dos pokemons:
            for i in range( len(pokemons_pode_escolher) ):
                # aqui vamos criar um texto com o pokemon "i" (o "i" que vai até o range do loop):
                superf = arq.fonte.render(pokemons_pode_escolher[i].nome, True, cores_pode_escolher[i])
                # Pegaremos as dimensões do texto que criamos acima:
                superf_rect = superf.get_rect()
                # Colocaremos no centro, e pegamos o espaçamento e multiplicamos por "i", para os nomes dos pokemons irem para baixo e não ficarem um em cima do outro:
                superf_rect.center =(janela.tamanho[0]/2, 100 + e_n + i*e_n)
                # Por fim, mostraremos na tela o texto:
                janela.tela.blit(superf, superf_rect)
            
            
            #pygame.draw.rect(tela, BRANCO, ( m_e , ((m_e[0]-janela.tamanho[0]),(m_e[1]-janela.tamanho[1]) ) ))
            pygame.draw.rect(janela.tela, cor.BRANCO, ((menu_espacamento[0],menu_espacamento[1]),(janela.tamanho[0]-(menu_espacamento[0]*2),janela.tamanho[1]-(menu_espacamento[1]*2))), 5)
        elif menu.no_menu(menu.batalhando):
            # Cena de batalha:
            #tela.blit(imagem, (x, y))
            janela.tela.blit(arq.img_fundo_pokemon,(0,0))
            
            
            # (x, y)
            
            # img_pokemons[n_do_pokemon][0 = frente, 1 = costas]
            # pokemon inimigo:
            janela.tela.blit(pokemons[1].imagem_frente, (janela.tamanho[0] - 100*escala,20*escala))
            # seu pokemon:
            janela.tela.blit(pokemons[0].imagem_costas, (25*escala,janela.tamanho[1] - 95*escala))
            
            # Menus:
            janela.tela.blit(arq.img_text_bar, (0, janela.tamanho[1] - 48*escala))
            if sub_menu.no_submenu(sub_menu.principal):
                janela.tela.blit(arq.img_opcoes_batalha, (janela.tamanho[0] - 120*escala, janela.tamanho[1] - 48*escala))
                pygame.draw.rect(janela.tela, cor.VERMELHO, ((janela.tamanho[0] - 107.5*escala + (pos[0]*distanciamento[0]), janela.tamanho[1] - 37.5*escala + (pos[1]*distanciamento[1])), (50*escala,15*escala)), int(1*escala))
            elif sub_menu.no_submenu(sub_menu.escolhendo_ataque):
                janela.tela.blit(arq.img_pp_bar, (0, janela.tamanho[1] - 48*escala))
            

            janela.tela.blit(arq.img_barra1, (15*escala, 18*escala))
            janela.tela.blit(arq.img_barra2, (janela.tamanho[0] - 110*escala,janela.tamanho[1] - 88*escala))

            # nomes dos pokemons renderizados na barra:
            poke_2 = arq.fonte.render(pokemons[1].nome, True, cor.PRETO)
            poke_2_rect = poke_2.get_rect()
            poke_2_rect.center =(48.5*escala, 25*escala)
            janela.tela.blit(poke_2, poke_2_rect)

            poke_1 = arq.fonte.render(pokemons[0].nome, True, cor.PRETO)
            poke_1_rect = poke_1.get_rect()
            poke_1_rect.center =((janela.tamanho[0] - 68*escala), janela.tamanho[1] - 77.5*escala)
            janela.tela.blit(poke_1, poke_1_rect)

            texto = ""
            a_cor = cor.PRETO

            if pokemons[0].genero == "F":
                texto, a_cor = "♀", cor.ROSA
            elif pokemons[1].genero == "M":
                texto, a_cor = "♂", cor.AZUL
            simb_1 = arq.fonte.render(texto, True, a_cor)
            simb_1_rect = simb_1.get_rect()
            simb_1_rect.left = poke_1_rect.width + poke_1_rect.x
            simb_1_rect.top = poke_1_rect.y
            janela.tela.blit(simb_1, simb_1_rect)

            
            texto = ""
            a_cor = cor.PRETO

            if pokemons[1].genero == "F":
                texto, a_cor = "♀", cor.ROSA
            elif pokemons[1].genero == "M":
                texto, a_cor = "♂", cor.AZUL
            simb_2 = arq.fonte.render(texto, True, a_cor)
            simb_2_rect = simb_2.get_rect()
            simb_2_rect.left = poke_2_rect.width + poke_2_rect.x
            simb_2_rect.top = poke_2_rect.y
            janela.tela.blit(simb_2, simb_2_rect)            

            # Barras de vida:
            
            #arq.img_vida_vermelha

            

            img_vida_vermelha_esticada = pygame.transform.scale(arq.img_vida_vermelha, (int(arq.img_vida_vermelha.get_width() + (escala*39)), arq.img_vida_vermelha.get_height()))
            janela.tela.blit(img_vida_vermelha_esticada,(55*escala, 34*escala))
            
            img_vida_vermelha_esticada = pygame.transform.scale(arq.img_vida_vermelha, (int(arq.img_vida_vermelha.get_width()  + (escala*39)), arq.img_vida_vermelha.get_height()))
            janela.tela.blit(img_vida_vermelha_esticada,(janela.tamanho[0] - 62*escala,janela.tamanho[1] - 69*escala))
            
            img_vida_amarela_esticada = pygame.transform.scale(arq.img_vida_amarela, (int(arq.img_vida_amarela.get_width()  + (escala*39)), arq.img_vida_vermelha.get_height()))
            janela.tela.blit(img_vida_amarela_esticada,(int(55*escala), int(34*escala)))

            img_vida_amarela_esticada = pygame.transform.scale(arq.img_vida_amarela, (int(arq.img_vida_amarela.get_width()  + (escala*39)), arq.img_vida_vermelha.get_height()))
            janela.tela.blit(img_vida_amarela_esticada,(janela.tamanho[0] - 62*escala,janela.tamanho[1] - 69*escala))
            #print((pokemons[0].vida_maxima - pokemons[0].vida)/pokemons[0].vida_maxima)
            img_barra_sem_vida_esticada = pygame.transform.scale(arq.img_barra_sem_vida, (floor((arq.img_barra_sem_vida.get_width() + (escala*39)) * (pokemons[0].vida_maxima - pokemons[0].vida)/pokemons[0].vida_maxima), arq.img_barra_sem_vida.get_height()))
            janela.tela.blit(img_barra_sem_vida_esticada,(ceil(55*escala + barra_width * (pokemons[0].vida/pokemons[0].vida_maxima)), 34*escala))

            img_barra_sem_vida_esticada = pygame.transform.scale(arq.img_barra_sem_vida, (floor((arq.img_barra_sem_vida.get_width() + (escala*39)) * (pokemons[1].vida_maxima - pokemons[1].vida)/pokemons[1].vida_maxima    ), arq.img_barra_sem_vida.get_height()))
            janela.tela.blit(img_barra_sem_vida_esticada,(ceil(janela.tamanho[0] - 62*escala + barra_width * (pokemons[1].vida/pokemons[1].vida_maxima)),janela.tamanho[1] - 69*escala))
            
            # Mostrando o nível do pokémon
            nivel = arq.fonte_txt.render(str(pokemons[0].nivel), True, cor.PRETO)
            nivel_rect = nivel.get_rect()
            nivel_rect.left = 96*escala
            nivel_rect.top = 18.5*escala
            janela.tela.blit(nivel, nivel_rect)
            nivel = arq.fonte_txt.render(str(pokemons[1].nivel), True, cor.PRETO)
            nivel_rect = nivel.get_rect()
            nivel_rect.left = janela.tamanho[0] - 21*escala
            nivel_rect.top = janela.tamanho[1] - 84.5*escala
            janela.tela.blit(nivel, nivel_rect)

            texto_multilinha(mensagem.texto)
            #janela.tela.blit(batalha_nome, batalha_rect)

        pygame.display.update()


    def escolher_pokemon(menu, sub_menu, mensagem):
        menu.atual = menu.batalhando
        sub_menu.atual = sub_menu.principal
        # seu pokémon:
        pokemons[0] = pokemons_pode_escolher[sel_s].copy()
        # pokémon inimigo:
        pokemons[1] = pokemons_pode_escolher[random.randrange(0,len(pokemons_pode_escolher)-1)].copy()
        mensagem.texto = "O que {} deve fazer?".format(pokemons[0].nome)
        
    def escolher_acao_batalha(mensagem):
        if pos == [0,0]:
            sub_menu.atual = sub_menu.escolhendo_ataque
        elif pos == [1,1]:
            tentar_fugir(pokemons[0], pokemons[1], mensagem)
    def tentar_fugir(pokemon_tentando_fugir, pokemon_inimigo, mensagem):
        fugiu = pokemon_tentando_fugir.fugir_de(pokemon_inimigo)
        if fugiu:
            mensagem.texto = "{} conseguiu fugir com sucesso!".format(pokemons[0].nome)
        else:
            mensagem.texto = "{} não conseguiu fugir!".format(pokemons[0].nome)
    
    turnos = []

    def randomizar_acao():
        return random.randrange(0,2)

    def acao_atacar(sub_menu, mensagem):
        vez = random.randrange(1,2)
        if pokemons[0].velocidade > pokemons[1].velocidade:
           vez = 1
        elif pokemons[0].velocidade < pokemons[1].velocidade:
            vez = 2

        if vez == vez:
            turnos.append([pokemons[0], pokemons[1], Acao.ataque_simples])
            turnos.append([pokemons[1], pokemons[0], randomizar_acao()])
        else:
            turnos.append([pokemons[1], pokemons[0], randomizar_acao()])
            turnos.append([pokemons[0], pokemons[1], Acao.ataque_simples])

        sub_menu.atual = sub_menu.principal
        processar_turnos(turnos, mensagem)
        #pokemon_2 = pokemon_1.atacar(pokemon_2)
        #pokemon_2.atacar(pokemon_1)
    
    

    def processar_logica():
        pass
    
    def processar_turnos(turnos, mensagem):
        
        print(turnos[1][2])
        for _ in range(len(turnos)):
            pokemon_a_fazer = turnos[0][0]
            pokemon_a_tomar = turnos[0][1]
            acao = turnos[0][2]

            
            if acao == Acao.ataque_simples:
                mensagem.texto = "{} ataca!".format(pokemon_a_fazer.nome)
                pokemon_a_fazer.atacar(pokemon_a_tomar)
            elif acao == Acao.fugir:
                pokemon_a_fazer.fugir_de(pokemon_a_tomar)

            turnos.pop(0)

        

    rodando_o_jogo = True

    mouse_pos = (0,0)

    # Loop do jogo:
    while rodando_o_jogo:

        if count > 59:
            count = 0

        delta = clock.tick(60)
        #count += 1

        # Eventos:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando_o_jogo = False
            
            # Eventos do mouse:
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
            
            # Eventos do teclado:
            if event.type == pygame.KEYDOWN:
                if menu.no_menu(menu.batalhando):
                    if sub_menu.no_submenu(sub_menu.principal):
                        if event.key == pygame.K_UP:
                            pos[1] = 0
                        elif event.key == pygame.K_DOWN:
                            pos[1] = 1
                        elif event.key == pygame.K_LEFT:
                            pos[0] = 0
                        elif event.key == pygame.K_RIGHT:
                            pos[0] = 1
                        
                        elif event.key == pygame.K_ESCAPE:
                            menu.atual = menu.escolhendo_pokemon
                        

                        if event.key == pygame.K_RETURN:
                            escolher_acao_batalha(mensagem)
                        

                    elif sub_menu.no_submenu(sub_menu.escolhendo_ataque):
                        if event.key == pygame.K_ESCAPE:
                            sub_menu.atual = sub_menu.principal
                        if event.key == pygame.K_RETURN:
                            acao_atacar(sub_menu, mensagem)
                    
                elif menu.no_menu(menu.escolhendo_pokemon):
                    if event.key == pygame.K_UP:
                        sel_s = sel_s - 1
                        if sel_s < 0:
                            sel_s = len(pokemons_pode_escolher) - 1
                    elif event.key == pygame.K_DOWN:
                        sel_s = sel_s + 1
                        if sel_s > len(pokemons_pode_escolher) - 1:
                            sel_s = 0
                    elif event.key == pygame.K_RETURN:
                        # escolheu o pokémon
                        arq.som_fire_red_abertura.stop()
                        escolher_pokemon(menu, sub_menu, mensagem)
                    elif event.key == pygame.K_ESCAPE:
                        rodando_o_jogo = False
        pygame.event.poll()
        desenhar_graficos()
        processar_logica()
        tocar_sons()
        #
    # Sair do pygame:
    pygame.quit()

if __name__ == "__main__":
    main()
