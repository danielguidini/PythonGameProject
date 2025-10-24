# Capybara Go !

`Capybara Go!` é um jogo de plataforma 2D simples criado com a biblioteca Pygame Zero (pgzrun) em Python.

Neste jogo, você controla uma capivara que deve pular entre plataformas para coletar todas as estrelas do nível, tudo isso enquanto desvia dos temíveis esqueletos "Mr. Bones" que patrulham a área.

## Funcionalidades

  * **Menu Principal:** Um menu inicial com opções para "Começar o Jogo", "Ligar/Desligar Som" e "Sair".
  * **Animação de Sprites:** O jogador (Capivara) e os inimigos (Mr. Bones) possuem animações de sprite para os estados de "parado" (idle) e "caminhando".
  * **Inimigos com Patrulha:** Os inimigos patrulham um território definido, movendo-se de um lado para o outro.
  * **Mundo com Câmera:** O mundo do jogo é maior que a tela, e a câmera segue o jogador lateralmente.
  * **Áudio:** O jogo inclui música de fundo e efeitos sonoros para pulo, coleta de itens, vitória e derrota.
  * **Física Simples:** Implementa gravidade básica, pulo e detecção de colisão com plataformas.

## Como Jogar

### Objetivo

O objetivo é simples: **colete todas as estrelas** espalhadas pelo nível.
Cuidado\! Se você tocar em um inimigo (Mr. Bones), o jogo acaba.

### Controles

  * **Seta Esquerda:** Mover para a esquerda
  * **Seta Direita:** Mover para a direita
  * **Seta Cima** ou **Barra de Espaço:** Pular

## Requisitos e Instalação

Para rodar este projeto, você precisará do Python e da biblioteca `pgzero`.

1.  **Instale o Pygame Zero:**

    ```bash
    pip install pgzrun
    ```

2.  **Clone ou baixe este repositório:**
    Certifique-se de que o arquivo `capybara-go.py` esteja no mesmo diretório que as pastas `images/`, `sounds/` e `music/`.

3.  **Execute o jogo:**
    Use o `pgzrun` para iniciar o arquivo principal:

    ```bash
    pgzrun capybara-go.py
    ```

## Estrutura do Projeto

```
/
|-- capybara-go.py       # O código principal do jogo
|-- images/              # Contém todos os sprites (capivara, mrbones, estrela)
|-- sounds/              # Contém os efeitos sonoros (.wav)
|-- music/               # Contém a música de fundo (.mp3)
|-- License.txt          # Informações de licença dos assets
`-- README.md            # Este arquivo
```

## Créditos dos Assets

  * Sprites (Capivara, Mr. Bones, Star): (Microsoft Copilot)
  * Sons (parcial): Kenney (www.kenney.nl)
  * Som de Game Over: deleted\_user\_877451 (via Freesound)
  * Som de Vitória: LittleRobotSoundFactory (via Freesound)

Consulte o arquivo `License.txt` para mais detalhes sobre as licenças dos assets de áudio.
