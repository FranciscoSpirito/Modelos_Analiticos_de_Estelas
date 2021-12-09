class U_inf(object):
    def __init__(self):
        self.perfil = None
        self.coord = None
        self.u_mast = None
        self.u_perfil = None

    def perfil_flujo_base(self, z_mast, z_0):
        if self.perfil == 'log':
            from math import log
            self.u_perfil = self.u_mast * (log(self.coord.z / z_0) / log(z_mast / z_0))

        elif self.perfil == 'cte':
            self.u_perfil = self.u_mast
