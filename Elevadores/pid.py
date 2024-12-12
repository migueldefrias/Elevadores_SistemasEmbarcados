
class PID:
    def __init__(self):
        self.saida_medida = 0.0
        self.sinal_de_controle = 0.0
        self.referencia = 0.0
        self.Kp = 0.0  # Ganho Proporcional
        self.Ki = 0.0  # Ganho Integral
        self.Kd = 0.0  # Ganho Derivativo
        self.T = 1.0  # Período de Amostragem (ms)
        self.last_time = 0
        self.erro_total = 0.0
        self.erro_anterior = 0.0
        self.sinal_de_controle_MAX = 100.0
        self.sinal_de_controle_MIN = -100.0

    def pid_atualiza_referencia(self, referencia_):
        self.referencia = referencia_

    def pid_controle(self, saida_medida):
        erro = self.referencia - saida_medida

        self.erro_total += erro  # Acumula o erro (Termo Integral)

        if self.erro_total >= self.sinal_de_controle_MAX:
            self.erro_total = self.sinal_de_controle_MAX
        elif self.erro_total <= self.sinal_de_controle_MIN:
            self.erro_total = self.sinal_de_controle_MIN

        delta_error = erro - self.erro_anterior  # Diferença entre os erros (Termo Derivativo)

        # PID calcula sinal de controle
        self.sinal_de_controle = self.Kp * erro + (self.Ki * self.T) * self.erro_total + (self.Kd / self.T) * delta_error 
        

        if self.sinal_de_controle >= self.sinal_de_controle_MAX:
            self.sinal_de_controle = self.sinal_de_controle_MAX
        elif self.sinal_de_controle <= self.sinal_de_controle_MIN:
            self.sinal_de_controle = self.sinal_de_controle_MIN

        self.erro_anterior = erro

        return self.sinal_de_controle