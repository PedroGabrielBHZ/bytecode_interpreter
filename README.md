# Interpretador Bytecode

Este é um interpretador para uma linguagem bytecode baseada em pilha, desenvolvido como trabalho prático da disciplina de Compiladores.

## Interface Gráfica (GUI)

O projeto inclui uma interface gráfica amigável para facilitar o uso do interpretador e otimizador.

### Como usar a GUI:
```bash
python bytecode_gui.py
```

### Funcionalidades da GUI:

- **Carregar arquivo .bc**: Abre um arquivo bytecode e exibe seu conteúdo em uma caixa de texto editável
- **Executar Otimizador**: Processa o código carregado através do otimizador e mostra o resultado
- **Comparar**: Abre uma janela para comparar lado a lado o código original e otimizado
- **Salvar Otimizado**: Salva o código otimizado em um novo arquivo
- **Executar Original**: Executa o programa original e mostra a saída
- **Executar Otimizado**: Executa o programa otimizado e mostra a saída
- **Campo de Entrada**: Permite fornecer entrada para programas que usam `READ`
- **Limpar Saídas**: Limpa a área de saída dos programas

A interface é dividida em três áreas principais:
- **Código Original** (editável)
- **Código Otimizado** (somente leitura)
- **Saída dos Programas** (com campo de entrada)

## Como usar (Linha de Comando)

### Executar a partir de arquivo:
```bash
python bytecode_interpreter.py test1.bc
```

### Executar a partir da entrada padrão:
```bash
python bytecode_interpreter.py < test1.bc
```

ou

```bash
cat test1.bc | python bytecode_interpreter.py
```

## Otimizador (Funcionalidade Extra - 4pts)

O projeto inclui um otimizador que remove instruções redundantes sem alterar a semântica:

### Como usar o otimizador:
```bash
python bytecode_optimizer.py input.bc output.bc
```

### Otimizações implementadas:

1. **Remoção de PUSH/POP redundantes**: Remove sequências `PUSH valor` seguidas imediatamente de `POP`
2. **Remoção de LOADs redundantes**: Remove LOADs consecutivos da mesma variável, substituindo por `DUP`
3. **Remoção de código morto**: Remove código após `HALT`, `RET` ou `JMP` incondicional
4. **Constant folding**: Calcula operações aritméticas com constantes em tempo de compilação

### Exemplo:
```bash
python bytecode_optimizer.py test_unoptimized.bc test_optimized.bc
```

## Arquivos do Projeto

- `bytecode_interpreter.py` - Interpretador principal
- `bytecode_optimizer.py` - Otimizador de código
- `bytecode_gui.py` - Interface gráfica
- `run_tests.py` - Script para executar todos os testes
- `tests/` - Diretório com arquivos de teste

## Resultados Esperados dos Testes

| Teste | Resultado Esperado |
|-------|-------------------|
| test1.bc | 20 |
| test2.bc | 1 |
| test3.bc | 5<br>4<br>3<br>2<br>1 |
| test4.bc | 7 |
| test5.bc | 10 |
| test_input.bc (entrada: 5) | 25 |

## Executar todos os testes

```bash
python run_tests.py
```

## Instruções suportadas

### Operações aritméticas e de pilha:
- `PUSH <val>` - Empilha um valor
- `POP` - Desempilha um valor
- `ADD` - Soma os dois valores do topo da pilha
- `SUB` - Subtrai os dois valores do topo da pilha
- `MUL` - Multiplica os dois valores do topo da pilha
- `DIV` - Divide os dois valores do topo da pilha
- `MOD` - Módulo dos dois valores do topo da pilha
- `NEG` - Nega o valor do topo da pilha
- `DUP` - Duplica o valor do topo da pilha

### Variáveis:
- `STORE <var>` - Armazena o valor do topo da pilha na variável
- `LOAD <var>` - Carrega o valor da variável para a pilha

### Fluxo de controle:
- `JMP <addr>` - Salta para o endereço/label
- `JZ <addr>` - Salta se o topo da pilha for zero
- `JNZ <addr>` - Salta se o topo da pilha for diferente de zero
- `HALT` - Para a execução

### Comparação:
- `EQ` - Verifica igualdade
- `NEQ` - Verifica desigualdade
- `LT` - Menor que
- `GT` - Maior que
- `LE` - Menor ou igual
- `GE` - Maior ou igual

### Funções e E/S:
- `CALL <addr>` - Chama função no endereço/label
- `RET` - Retorna da função
- `PRINT` - Imprime o valor do topo da pilha
- `READ` - Lê um valor da entrada padrão

### Labels:
- `LABEL:` - Define um rótulo para saltos e chamadas

## Exemplos de uso

### Teste básico:
```bash
python bytecode_interpreter.py test1.bc
```
Saída esperada: `20`

### Teste com condicional:
```bash
python bytecode_interpreter.py test2.bc
```
Saída esperada: `1`

### Teste com loop:
```bash
python bytecode_interpreter.py test3.bc
```
Saída esperada:
```
5
4
3
2
1
```
