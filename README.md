# 🧑‍💻 Compilador de C Simplificado para Assembly SAM (Stack-based Assembly Machine)

Este projeto é um compilador didático implementado em Python que traduz um subconjunto simplificado da linguagem C para código Assembly para uma Máquina de Endereço Único baseada em Pilha (SAM). Após a geração do código, o próprio programa `main.py` atua como um simulador simples para executar as instruções SAM geradas.

## 🌟 Visão Geral do Projeto

O compilador segue as etapas tradicionais de um processo de compilação:

1.  **Análise Léxica:** Quebra o código-fonte em *tokens* (léxicos).
2.  **Análise Sintática:** Verifica a estrutura do programa usando uma gramática formal.
3.  **Geração de Código:** Traduz as construções da linguagem de alto nível para instruções da máquina alvo (Assembly SAM).
4.  **Simulação:** Executa o código SAM gerado em um interpretador embutido.

## ⚙️ Tecnologias e Componentes

* **Linguagem de Implementação:** Python
* **Lexer (Análise Léxica):** Implementado usando a biblioteca `PLY` (Python Lex-Yacc).
* **Parser (Análise Sintática):** Implementado como um parser Preditivo Recursivo Descendente, com base em uma **Gramática LL(1)**.
    * **Algoritmos de Análise de Gramática:** O projeto inclui implementações manuais dos algoritmos para calcular os conjuntos **FIRST**, **FOLLOW** e **PREDICT**, essenciais para o parser LL(1).
* **Geração de Código e Simulação:** Funções de tradução e o interpretador SAM estão embutidos em `main.py`.

## 🔤 Linguagem de Entrada (C Simplificado)

O compilador suporta as seguintes construções da linguagem C (apenas para o tipo `int`):

| Categoria | Construções Suportadas | Exemplo |
| :--- | :--- | :--- |
| **Estrutura** | Função principal (`main`) e escopo com chaves (`{}`) | `int main(){ ... }` |
| **Variáveis** | Declaração de `int`, atribuição (`=`) | `int x; x = 10;` |
| **Aritmética** | Adição (`+`), Subtração (`-`), Multiplicação (`*`), Divisão (`/`) | `z = x + y;` |
| **Controle** | Laço de repetição `while` | `while (a <= b) { ... }` |
| **Controle** | Condicional `if`, `else`, `endif` | `if (x < 10) { ... } else { ... } endif` |
| **Lógica** | Operadores Relacionais (`<`, `>`, `<=`, `>=`, `==`, `!=`) | `(i <= n)`, `(x >= 0)` |
| **Saída** | Impressão de variáveis inteiras (`printf`) | `printf(z);` |

## 💻 Linguagem de Saída (Assembly SAM)

O código é traduzido para um conjunto de instruções simples de máquina de pilha (Stack-based Assembly Machine - SAM).

| Instrução SAM | Descrição |
| :--- | :--- |
| `ADDSP n` | Aloca/Desaloca `n` espaços na pilha (usado para variáveis locais). |
| `PUSHIMM n` | Coloca o valor imediato `n` no topo da pilha. |
| `PUSHABS n` | Coloca o valor da variável localizada na posição absoluta `n` no topo da pilha. |
| `STOREABS n` | Retira o valor do topo da pilha e armazena-o na posição absoluta `n` (atribuição). |
| `ADD`/`SUB`/`TIMES`/`DIV` | Operações aritméticas com os dois elementos no topo da pilha. |
| `GREATER`/`LESS`/`EQUAL` | Operadores relacionais. |
| `JUMPC LABEL` | Desvio Condicional: pula para `LABEL` se o valor no topo da pilha for falso (0). |
| `JUMP LABEL` | Desvio Incondicional: pula para `LABEL`. |
| `STOP` | Encerra a execução do programa. |

**Labels Suportados:** `WHILE`, `ENDWHILE`, `ELSE`, `ENDIF`.

## 🚀 Como Executar

Para executar o compilador e o simulador, siga os seguintes passos:

1.  **Pré-requisitos:** Certifique-se de ter o Python instalado. A biblioteca `ply` é necessária para a análise léxica.
    ```bash
    pip install ply
    ```
2.  **Preparação:** O arquivo `main.py` está configurado para ler o código-fonte do arquivo `codigo.c` por padrão. Certifique-se de que o código-fonte C simplificado esteja nesse arquivo.

3.  **Compilação e Simulação:** Execute o `main.py`. Ele irá realizar a análise, gerar o código SAM em `output.sam` e, em seguida, simular sua execução.

    ```bash
    python main.py
    ```

### Exemplo de Saída

Ao executar o compilador com o código em `codigo.c`:

```c
int main(){
    int z;
    int x;
    int y;

    x = 10;
    y = 20;
    z = x + y;

    printf(z);
}
