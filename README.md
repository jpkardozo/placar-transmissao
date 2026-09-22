cat << 'EOF' > README.md
# 🏆 Placar Pro para Transmissões - Natorcida

Um sistema de placar moderno, leve e em tempo real desenvolvido em **Python (Flask)**, criado sob medida para transmitir partidas e eventos esportivos com qualidade profissional (estilo TV). 

O sistema conta com um painel de controle web responsivo (para gerenciar por celular, tablet ou PC) e uma interface transparente otimizada para integração direta com o **OBS Studio**.

---

## ✨ Funcionalidades Principais

* **⏱️ Cronômetro Automático:** Controle total de início, pausa e zeragem direto pelo painel.
* **⌨️ Atalhos de Teclado (Hotkeys):** Altere os gols rapidamente sem tirar a mão do teclado (`G`/`H` para a Casa e `K`/`L` para Fora).
* **💥 Animação de Gol:** Destaque visual automático e efeitos dinâmicos na tela do OBS sempre que um gol é marcado.
* **🔄 Rotação de Patrocinadores:** Exibição rotativa automática de marcas e parceiros na barra inferior.
* **📱 Acesso Remoto:** Controle o placar de qualquer lugar (inclusive pelo celular) com atualizações instantâneas na live.

---

## 🔗 Links de Acesso

* **🎛️ Painel de Controle (Gerenciamento):**  
  https://placartransmissao.onrender.com
* **📺 Overlay para a Live (OBS Studio):**  
  https://placartransmissao.onrender.com/obs

---

## 🛠️ Como colocar no OBS Studio

Para exibir o placar transparente na sua transmissão, siga os passos abaixo:

1. Abra o **OBS Studio** na sua cena de transmissão.
2. Na caixa de **Fontes**, clique no botão **`+`** e selecione **Navegador** (Browser Source).
3. Dê um nome para a fonte (ex: *Placar da Partida*) e clique em OK.
4. Preencha as configurações da fonte:
   * **URL:** `https://placartransmissao.onrender.com/obs`
   * **Largura (Width):** `500`
   * **Altura (Height):** `150`
5. Clique em **OK**. Pronto! O placar aparecerá na sua tela com fundo transparente e atualizará em tempo real conforme você gerencia pelo painel.

---

## 📄 Licença

Este projeto é distribuído sob a licença **MIT**. Sinta-se livre para usar, estudar e modificar conforme necessário.
EOF