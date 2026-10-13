# Cine R36S

App de catálogo de filmes para o **R36S / consoles com ArkOS + PortMaster**, feito em Python + SDL2.
Mostra informações de filmes pela API do [TMDB](https://www.themoviedb.org/) e toca vídeos de fontes que **você** configura.

Sem nenhuma configuração extra, o app toca o **trailer oficial** (TMDB/YouTube, via `yt-dlp`).
Você também pode apontar para uma fonte própria, como filmes em **domínio público**, conteúdo **Creative Commons** ou a sua **biblioteca pessoal** (por exemplo um servidor Jellyfin ou Plex).

> Projeto derivado de um app de YouTube para PortMaster, adaptado para filmes.
> Este produto usa a API do TMDB mas não é endossado nem certificado pelo TMDB.

## Recursos

- Busca, favoritos e histórico
- Capas, notas e sinopses em português (fallback para inglês)
- Trailers oficiais do TMDB/YouTube por padrão
- Fonte de vídeo própria, opcional (veja a seção de configuração)
- Configurações: idioma (6), qualidade, tela cheia, altura do vídeo, itens por busca, carregar início automático
- **ID enviado à fonte**: escolha mandar o id do **TMDB** ou do **IMDb** (fica salvo)

## Instalação

1. Tenha o [PortMaster](https://portmaster.games/) instalado.
2. Copie para o cartão SD:
```
   /roms/ports/Cine.sh
   /roms/ports/cine/        (pasta inteira deste repositório)
```
3. Baixe o **yt-dlp** para ARM64 em <https://github.com/yt-dlp/yt-dlp/releases> (arquivo `yt-dlp_linux_aarch64`), renomeie para `yt-dlp` e coloque em `/roms/ports/cine/yt-dlp`.
4. Em `/roms/ports/cine/`, copie `config.example.txt` para `config.txt` e coloque sua chave do TMDB.
5. Reinicie o EmulationStation. O **Cine** aparece em *Ports*.

## Configuração (`config.txt`)

| Chave | Descrição |
|-------|-----------|
| `TMDB_API_KEY` | Sua chave gratuita do TMDB (obrigatória) |
| `TRAILER_API_URL` | Fonte de vídeo própria (opcional). Use `{tmdb_id}` ou `{imdb_id}` onde entra o id |

Se `TRAILER_API_URL` ficar vazio, o app usa os trailers oficiais.
Se você configurar uma fonte, ela deve responder:

```json
{"success": true, "sources": [{"file": "link", "label": "Opção 1", "type": "mp4"}]}
```

Em **Configurações > ID do Trailer** você escolhe se o app envia o id do TMDB ou do IMDb.

## Controles

Direcional para navegar, **A** seleciona, **B** volta, esquerda/direita altera opções nas Configurações.

## Estrutura

```
Cine.sh                  launcher do PortMaster
cine/cine.py             aplicação
cine/sdl2/               pysdl2 (incluído para facilitar)
cine/config.example.txt  modelo de configuração
```
