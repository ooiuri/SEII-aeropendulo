from numpy import pi, sin, sqrt, arange, floor, array, append
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Variaveis auxiliares
rad2deg = 180/pi
deg2rad = pi/180

b = 0.006856
m = 0.1182
g = 9.81
I = 0.0164
kh = 2.12829e-5
LH = 0.32

class AirPendulum():
    # Definindo dinamica da planta
    # Parametros da planta

    def __init__(self, theta_b=40, ta=1e-2):
        super(AirPendulum, self).__init__()

        self.theta_register = array([])
        self.theta = 0

        self.theta_p_register = array([])
        self.theta_p = 0

        self.theta_p_b = 0*deg2rad
        self.theta_b = theta_b*deg2rad
        self.ta = ta

        self.omega_register = array([])
        self.omega = 0
        self.omega_b = sqrt(m*g*sin(self.theta_b)/kh)

        self.lastError = 0
        self.lastError_register = array([])

        self.lastError_I = 0

        self.theta_b_register = array([])

        self.P = 0
        self.I = 0
        self.D = 0

    def dynamic(self, omega):
        # Evoluindo a din. da planta
        x0 = [self.theta,
              self.theta_p]   # condicao inicial
        omega = min(omega,2500/9.55)
        omega = max(omega,0)

        sol = odeint(self.model, x0, [0.0, self.ta],
                     args=(omega,))
        
        self.omega = min(self.omega,2500/9.55)
        self.omega = max(self.omega,0)

        # if self.omega > 1000/9.55:
        #     self.omega = 1000/9.55
        
        self.theta = sol[:, 0][-1]
        self.theta_p = sol[:, 1][-1]

        self.omega_register= append(self.omega_register, self.omega)
        self.theta_register= append(self.theta_register, self.theta)
        self.theta_p_register= append(self.theta_p_register, self.theta_p)
        self.theta_b_register= append(self.theta_b_register, self.theta_b)

        return [self.theta, self.theta_p]

    def model(self, y, _, omega):
        # Definindo estados
        x1, x2 = y
        # Dinamica do pendulo
        x1p = x2
        x2p = (LH*kh/I)*omega**2
        x2p -= (LH*m*g/I)*sin(x1)
        x2p -= (b/LH)*x2
        return [x1p, x2p]

    def calc_pid(self):
        kp = 100
        ki = 40
        kd = 4.7

        error = (self.theta_b - self.theta)
        self.P = error * kp 
        self.I = self.lastError_I + error * ki * self.ta
        self.D = (error - self.lastError) * kd / self.ta

        self.lastError = error
        self.lastError_I = self.I
        self.lastError_register = append(self.lastError_register, self.lastError)
        return (self.P + self.I + self.D)
    
    def control_simulation(self):
        for k in range(3000):
            # Entrada da planta
            if k*self.ta > 1:
                self.omega = self.calc_pid()
            
            self.dynamic(self.omega)
        
        self.plot_air_pendulum_result()

    def update_reference(self, new_theta_b):
        self.theta_b = new_theta_b*deg2rad
        
    def plot_air_pendulum_result(self):

        # Plotando resultados
        plt.figure()
        plt.plot(arange(0, self.theta_register.size)*self.ta, (self.theta_register) *
                 rad2deg, lw=2, label=r'$\theta$ (deg)')
        plt.xlabel('Tempo (s)')
        plt.legend()
        plt.grid(True)
        plt.savefig("airpendulum_theta_tempo.png")

        plt.figure()
        plt.plot(arange(0, self.theta_p_register.size)*self.ta, (self.theta_p_register) *
                 rad2deg, lw=2, label=r'$\theta_d$ (deg)')
        plt.xlabel('Tempo (s)')
        plt.legend()
        plt.grid(True)
        plt.savefig("airpendulum_theta_p_tempo.png")

        plt.figure()
        plt.plot(arange(0,self.omega_register.size)*self.ta,
                 self.omega_register*9.55, 'r--', lw=2, label=r'$\omega$ (rpm)')
        plt.xlabel('Tempo (s)')
        plt.legend()
        plt.grid(True)

        plt.show()
        plt.savefig("airpendulum_omega_tempo.png")

        plt.figure()
        plt.plot(arange(0,self.lastError_register.size)*self.ta,
                 self.lastError_register, 'r--', lw=2, label=r'lastError (rad)')
        plt.xlabel('Tempo (s)')
        plt.legend()
        plt.grid(True)

        plt.figure()
        plt.plot(arange(0,self.theta_b_register.size)*self.ta,
                 self.theta_b_register, 'r--', lw=2, label=r'theta_b (rad)')
        plt.xlabel('Tempo (s)')
        plt.legend()
        plt.grid(True)

        plt.show()
        plt.savefig("airpendulum_lastError_tempo.png")

        print(self.theta_b - self.theta)

pendulo = AirPendulum()
pendulo.control_simulation()