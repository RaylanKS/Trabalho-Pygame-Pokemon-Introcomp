# Os efeitos serão comparados:
def compare_effects(effect1, effect2, priority):
    # Compara os efeitos pelo id e prioridade:
    return True if effect1["id"] == effect2["id"] and effect1["priority"] == priority else False


class Effect:
    @property
    def leech_seed(self):
        # {id, quantos turnos precisa passar antes do efeito começar a funcionar,
        # para_depois de quantos turnos, prioridade (True = antes do seu movimento, False = depois do seu movimento)}
        # sem dicionários seria: return [0, -1, None, True]
        # usar dicionários é melhor:
        return {"id": 0,
                "offset": 0,  # logo quando pegar o efeito começará a funcionar
                "stops": None,  # None: dura para "sempre"
                "priority": True}  # Antes do movimento dele

    @property
    def wrap(self):
        return {"id": 1,
                "offset": -1,  # Quantos turnos precisa passar antes de começar (NOTA: precisa ser negativo)
                "stops": [2, 3, 4, 5],  # De 2 a 5 turnos (todas as possibilidades)
                "priority": False}  # Depois do movimento dele

    @property
    def curse(self):
        return {"id": 2,
                "offset": -1,
                "stops": None,  # Nunca
                "priority": False}  # Depois do movimento dele
