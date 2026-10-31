"""Jal-Netra physics: sound speed in water, transit-time difference, flow profile correction, geometry of the Z-body spool.
All numbers assumptions are labelled; every formula is the textbook transit-time relation  dt = 2 L v / c^2  for an axial path."""
import math
def c_water(T):
    """speed of sound in pure water, Marczak (1997) polynomial, T in deg C (0-95): about 1482 m/s at 20 C"""
    return 1.402385e3 + 5.038813 * T - 5.799136e-2 * T ** 2 + 3.287156e-4 * T ** 3 - 1.398845e-6 * T ** 4 + 2.787860e-9 * T ** 5
def nu_water(T):
    """kinematic viscosity of water in m2/s (Vogel-type fit, 0-60 C)"""
    mu = 2.414e-5 * 10 ** (247.8 / (T + 273.15 - 140.0)); rho = 1000.0 * (1 - (T + 288.9414) / (508929.2 * (T + 68.12963)) * (T - 3.9863) ** 2)
    return mu / rho
class Spool:
    """Z-body ultrasonic spool: two inline transducers facing each other over an axial measuring tube of bore d and length L; flow enters/leaves through side ports."""
    def __init__(self, d=0.012, L=0.060):
        self.d, self.L = d, L; self.A = math.pi * d * d / 4
    def tof(self, T): return self.L / c_water(T)
    def dt(self, v_axis, T):
        """upstream minus downstream transit time for a line-averaged axial velocity v_axis (m/s)"""
        c = c_water(T); return 2 * self.L * v_axis / (c * c - v_axis ** 2)
    def v_from_dt(self, dt, T):
        c = c_water(T); return dt * c * c / (2 * self.L + dt * 0)           # small-v approximation (error v^2/c^2 ~ 1e-10)
    def Q_Lpm(self, v_line, T):
        Re = max(v_line * self.d / nu_water(T), 1.0); return 1000 * 60 * self.A * v_line * kprofile(Re) * 1.0
def kprofile(Re):
    """ratio of area-mean velocity to line-averaged (diametral path) velocity. Laminar parabolic profile: 0.75 (path samples the centre line, mean = 0.5 vmax, line mean = 2/3 vmax... = 0.75);
    turbulent: about 0.95 at Re 1e4 rising to 0.97 at 1e5 (power-law profile n = 6..8). Transition 2000-4000 is blended. ASSUMED model: the real factor must be calibrated on a flow rig."""
    if Re <= 2000: return 0.75
    n = 6.0 + 2.0 * min(max((math.log10(Re) - 3.3) / 1.7, 0), 1)                   # power-law exponent grows with Re
    k_t = 2 * n * n / ((n + 1) * (2 * n + 1)) / (n / (n + 1))                       # (area mean)/(line mean) for u = umax (1-r/R)^(1/n)
    if Re >= 4000: return k_t
    w = (Re - 2000) / 2000; return 0.75 * (1 - w) + k_t * w
if __name__ == "__main__":
    s = Spool(); print("c(20C) =", round(c_water(20), 1), "m/s; ToF =", round(s.tof(20) * 1e6, 2), "us; nu(20C) =", nu_water(20))
    for Q in (0.05, 0.2, 1, 5, 20, 40):
        v = Q / 60000 / s.A; print(f"Q {Q:6.2f} L/min  v_mean {v*1000:7.1f} mm/s  dt {s.dt(v / kprofile(max(v*s.d/nu_water(20),1)), 20)*1e9:7.3f} ns")
