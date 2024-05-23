README
porque utilizei multiprocessing ao invez de threadgind no codigo do mock:
Vamos refazer a implementação utilizando `multiprocessing` em vez de `threading`. A principal razão para escolher `multiprocessing` sobre `threading` é que o Python possui o GIL (Global Interpreter Lock), que pode limitar a eficiência dos threads em algumas situações. O `multiprocessing` cria processos separados, cada um com sua própria memória, permitindo uma melhor utilização de múltiplos núcleos de CPU, o que pode resultar em melhor desempenho em algumas tarefas.

Aqui está a versão atualizada usando `multiprocessing`:

```python
# mock_daq.py
import time
import multiprocessing

class MockDAQDevice:
    def __init__(self):
        self.manager = multiprocessing.Manager()
        self.pins = self.manager.dict()
        self.toggled_pins = self.manager.dict()

    def configure_digital_channel(self, pin, direction):
        self.pins[pin] = {
            'direction': direction,
            'state': False
        }

    def write_digital_pin(self, pin, state):
        if pin in self.pins and self.pins[pin]['direction'] == 'output':
            self.pins[pin]['state'] = state
        else:
            raise ValueError("Pin not configured as output or does not exist.")

    def read_digital_pin(self, pin):
        if pin in self.pins and self.pins[pin]['direction'] == 'input':
            return self.pins[pin]['state']
        else:
            raise ValueError("Pin not configured as input or does not exist.")

    def toggle_pin(self, pin, interval=1):
        if pin not in self.pins:
            raise ValueError("Pin does not exist.")
        if self.pins[pin]['direction'] != 'input':
            raise ValueError("Pin is not configured as input.")

        def toggle(pins, toggled_pins, pin, interval):
            while True:
                current_state = pins[pin]['state']
                pins[pin]['state'] = not current_state
                toggled_pins[pin] = pins[pin]['state']
                time.sleep(interval)

        process = multiprocessing.Process(target=toggle, args=(self.pins, self.toggled_pins, pin, interval))
        process.daemon = True
        process.start()
```

### Explicação

- **`multiprocessing.Manager`**: Usamos `Manager` para criar dicionários compartilhados (`pins` e `toggled_pins`) entre processos.
- **`multiprocessing.Process`**: Substitui `threading.Thread`, criando um novo processo que executa a função `toggle`.
- **Argumentos**: Passamos `self.pins`, `self.toggled_pins`, `pin`, e `interval` como argumentos para garantir que o processo filho tenha acesso às variáveis necessárias.

### Benefícios do `multiprocessing`

1. **Melhor Utilização de CPU**: `multiprocessing` pode utilizar múltiplos núcleos de CPU, permitindo um melhor desempenho em tarefas que podem ser paralelizadas.
2. **Isolamento de Processos**: Cada processo tem seu próprio espaço de memória, o que pode reduzir o risco de condições de corrida e outros problemas de concorrência associados ao compartilhamento de memória.
3. **Superação do GIL**: O GIL pode limitar a execução simultânea de threads Python, mas não afeta processos separados. Com `multiprocessing`, cada processo tem seu próprio interpretador Python e seu próprio GIL, o que pode melhorar o desempenho em tarefas computacionalmente intensivas.

### Considerações

- **Overhead de Processos**: Criar novos processos pode ter mais overhead do que criar novos threads, especialmente para tarefas que não são computacionalmente intensivas.
- **Comunicação entre Processos**: A comunicação entre processos é mais complexa e mais lenta do que a comunicação entre threads, que compartilham o mesmo espaço de memória.

Para este caso, como estamos simulando a alternância de pinos, o uso de `multiprocessing` é mais adequado se estivermos preocupados com o desempenho em um ambiente com múltiplos núcleos de CPU.

Embora `multiprocessing` possa ter benefícios significativos em termos de desempenho e isolamento de processos, ele também apresenta algumas desvantagens em comparação com `threading`:

### Desvantagens do `multiprocessing` em relação ao `threading`

1. **Overhead de Criação de Processos**: A criação de novos processos é mais custosa em termos de recursos do sistema (tempo e memória) do que a criação de novas threads.
2. **Comunicação entre Processos**: A comunicação entre processos (IPC - Inter-Process Communication) é mais complexa e geralmente mais lenta do que a comunicação entre threads, pois os processos não compartilham o mesmo espaço de memória.
3. **Consumo de Memória**: Cada processo tem seu próprio espaço de memória, o que pode levar a um maior consumo de memória em comparação com threads que compartilham o mesmo espaço de memória.
4. **Complexidade**: Manipular múltiplos processos pode ser mais complexo e exigir mais código para coordenar as ações entre processos, especialmente quando se necessita de compartilhamento de dados entre eles.
