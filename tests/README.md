# Testes do Interpretador Bytecode

Este diretório contém todos os arquivos de teste para o interpretador bytecode.

## Arquivos de Teste

### Testes Básicos (baseados na especificação):
- `test1.bc` - Operações básicas com variáveis (resultado: 20)
- `test2.bc` - Estrutura condicional if/else (resultado: 1) 
- `test3.bc` - Estrutura de repetição while (resultado: 5,4,3,2,1)
- `test4.bc` - Chamada de função com parâmetros (resultado: 7)
- `test5.bc` - Função com retorno (resultado: 10)

### Testes Especiais:
- `test_input.bc` - Teste com entrada do usuário (READ)
- `test_unoptimized.bc` - Código não otimizado para demonstrar otimizações
- `test_optimized.bc` - Resultado da otimização

### Scripts de Teste:
- `run_tests.py` - Script automatizado para executar todos os testes
- `test_input_example.py` - Exemplo de como testar entrada interativa

## Como Executar

### Executar um teste específico:
```bash
cd ..
python bytecode_interpreter.py tests/test1.bc
```

### Executar todos os testes:
```bash
cd tests
python run_tests.py
```

### Testar entrada interativa:
```bash
cd ..
echo "5" | python bytecode_interpreter.py tests/test_input.bc
```

### Testar otimizador:
```bash
cd ..
python bytecode_optimizer.py tests/test_unoptimized.bc tests/test_optimized_new.bc
```

## Resultados Esperados

| Teste | Resultado Esperado |
|-------|-------------------|
| test1.bc | 20 |
| test2.bc | 1 |
| test3.bc | 5<br>4<br>3<br>2<br>1 |
| test4.bc | 7 |
| test5.bc | 10 |
| test_input.bc (entrada: 5) | 25 |
