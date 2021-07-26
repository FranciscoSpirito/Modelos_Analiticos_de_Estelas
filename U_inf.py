class U_inf(object):
    def __init__(self):
        self.coord = None
        self.coord_mast = None
        self.perfil = None

    def perfil_flujo_base(self, z_mast, z_0):
        if self.perfil == 'log':
            from math import log
            self.coord = self.coord_mast * (log(self.coord.z / z_0) / log(z_mast / z_0))

        elif self.perfil == 'cte':
            self.coord = self.coord_mast
