class U_inf(object):
    def __init__(self, z_mast, z_0, perfil):
        self.z_mast = z_mast
        self.z_0 = z_0
        self.perfil = perfil
        self.u_mast = None
        self.u_perfil = None


    def perfil_flujo_base(self, coord):
        if self.perfil == 'log':
            from math import log
            self.u_perfil = self.u_mast * (log(coord.z / self.z_0) / log(self.z_mast / self.z_0))

        elif self.perfil == 'cte':
            self.u_perfil = self.u_mast

