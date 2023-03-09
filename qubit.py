# This code is from the given starter code for the QKD Project part 2 assignment.
# Many addition helper functions added for more gates (S, Sdg, Qdg, T, Tdg,...)
import random
import numpy as np


class InputError(Exception):
    def __int__(self, expression, message):
        self.expression = expression
        self.message = message


class Qubit:

    def __init__(self, Hcomp=0, Vcomp=0):
        self.alpha = Hcomp
        self.beta  = Vcomp

    # __str__ added by Rocco Perciavalle
    def __str__(self):
        return self.toString()

    # This is for debugging purposes only!
    def toString(self):
        if np.isreal(self.alpha):
            string = str(self.alpha) + "|H> "
        else:
            string = str(self.alpha) + "|H> "
        if np.isreal(self.beta):
            if self.beta >= 0:
                string += "+ " + str(self.beta) + "|V>"
            else:
                string += "- " + str(-self.beta) + "|V>"
        else:
            string += "+ " + str(self.beta) + "|V>"
        return string

    def prepareVacuum(self):
        energyPerMode = 0.5; # in units of hbar*omega
        x0 = np.sqrt(energyPerMode)*random.gauss(0,1)/np.sqrt(2)
        y0 = np.sqrt(energyPerMode)*random.gauss(0,1)/np.sqrt(2)
        x1 = np.sqrt(energyPerMode)*random.gauss(0,1)/np.sqrt(2)
        y1 = np.sqrt(energyPerMode)*random.gauss(0,1)/np.sqrt(2)
        self.alpha = complex(x0, y0)
        self.beta  = complex(x1, y1)

    def prepare(self, alpha, beta, avgPhotonNumber):
        if avgPhotonNumber < 0:
            raise InputError()
        vac = Photon()
        vac.prepareVacuum()
        self.alpha = alpha * np.sqrt(avgPhotonNumber) + vac.alpha
        self.beta  = beta  * np.sqrt(avgPhotonNumber) + vac.beta

    def prepareH(self, avgPhotonNumber):
        self.prepare(1, 0, avgPhotonNumber)

    def prepareV(self, avgPhotonNumber):
        self.prepare(0,1, avgPhotonNumber)

    def prepareD(self, avgPhotonNumber):
        self.prepare(1/np.sqrt(2),  1/np.sqrt(2), avgPhotonNumber)

    def prepareA(self, avgPhotonNumber):
        self.prepare(1/np.sqrt(2), -1/np.sqrt(2), avgPhotonNumber)

    def prepareR(self, avgPhotonNumber):
        self.prepare(1/np.sqrt(2),  1j/np.sqrt(2), avgPhotonNumber)

    def prepareL(self, avgPhotonNumber):
        self.prepare(1/np.sqrt(2), -1j/np.sqrt(2), avgPhotonNumber)

    def measureHV(self, probDarkCount):
        if probDarkCount < 0 or probDarkCount > 1:
            raise InputError
        threshold  = -0.5*np.log(1 - np.sqrt(1-probDarkCount))
        intensityH = abs(self.alpha)**2
        intensityV = abs(self.beta)**2
        # The photon is absorbed by the detector:
        self.prepareVacuum()
        # The outcome is determined by threshold exceedances:
        if intensityH <= threshold and intensityV <= threshold:
            return "N" # no detection (invalid measurement)
        elif intensityH > threshold and intensityV <= threshold:
            return "H" # single H photon detected
        elif intensityH <= threshold and intensityV > threshold:
            return "V" # single V photon detected
        else:
            return "M" # multiple detections (invalid measurement)

    def measureDA(self, probDarkCount):
        a = self.alpha
        b = self.beta
        self.alpha = (a+b)/np.sqrt(2)
        self.beta  = (a-b)/np.sqrt(2)
        outcome = self.measureHV(probDarkCount)
        if outcome == "H": return "D"
        if outcome == "V": return "A"
        else: return outcome

    def measureRL(self, probDarkCount):
        a = self.alpha
        b = self.beta
        self.alpha = (a-b*1j)/np.sqrt(2)
        self.beta  = (a+b*1j)/np.sqrt(2)
        outcome = self.measureHV(probDarkCount)
        if outcome == "H": return "R"
        if outcome == "V": return "L"
        else: return outcome

    def applyPolarizer(self, theta, phi):
        # Apply a polarizing filter according to the input parameters.
        # theta=0,    phi=0:     H polarizer
        # theta=pi/2, phi=0:     V polarizer
        # theta=pi/4, phi=0:     D polarizer
        # theta=pi/4, phi=pi:    A polarizer
        # theta=pi/4, phi=+pi/2: R polarizer
        # theta=pi/4, phi=-pi/2: L polarizer
        z = np.exp(1j*phi)
        a = self.alpha
        b = self.beta
        self.alpha = a*(1+np.cos(2*theta))/2 + b*np.sin(2*theta)/2*np.conj(z)
        self.beta  = a*np.sin(2*theta)/2*z + b*(1-np.cos(2*theta))/2
        # Now add an extra vacuum component.
        vac = Qubit()
        vac.prepareVacuum()
        a = vac.alpha
        b = vac.beta
        self.alpha = self.alpha + a*np.sin(theta)**2 + b*(-np.sin(2*theta)/2)*np.conj(z)
        self.beta  = self.beta  + a*(-np.sin(2*theta)/2)*z + b*np.cos(theta)**2

    def applyUnitaryGate(self, theta, phi, lamb):
        U = [[0,0],[0,0]]
        z1 = np.exp(1j*phi)
        z2 = -np.exp(1j*lamb)
        z3 = np.exp(1j*(lamb+phi))
        U[0][0] = np.cos(theta/2)
        U[1][0] = np.sin(theta/2)*z1
        U[0][1] = np.sin(theta/2)*z2
        U[1][1] = np.cos(theta/2)*z3
        a = self.alpha
        b = self.beta
        self.alpha = U[0][0]*a + U[0][1]*b
        self.beta  = U[1][0]*a + U[1][1]*b

    def applyXGate(self):
        # Applies the Pauli X gate
        self.applyUnitaryGate(np.pi, 0, np.pi)

    def applyYGate(self):
        # Applies the Pauli Y gate
        self.applyUnitaryGate(np.pi, np.pi/2, np.pi/2)

    def applyZGate(self):
        # Applies the Pauli X gate
        self.applyUnitaryGate(0, np.pi, 0)

    def applyHGate(self):
        # Applied the Hadamard (half-wavelength) gate
        self.applyUnitaryGate(np.pi/2, 0, np.pi)

    def applySGate(self):
        # Applied the S gate
        self.applyUnitaryGate(0, 0, np.pi/2)

    def applySdgGate(self):
        # Applied the S dagger gate
        self.applyUnitaryGate(0, 0, -np.pi/2)

    def applyTGate(self):
        # Applied the T gate
        self.applyUnitaryGate(0, 0, np.pi/4)

    def applyTdgGate(self):
        # Applied the T dagger gate
        self.applyUnitaryGate(0, 0, -np.pi/4)
    def applyQGate(self):
        # Applies the SH (quarter-wavelength) gate
        self.applyUnitaryGate(np.pi/2, np.pi/2, np.pi)

    def applyQdgGate(self):
        # Applies the SH (quarter-wavelength) gate
        self.applyUnitaryGate(np.pi/2, 0, np.pi/2)

    def applyNoisyGate(self, p):
        # This operation acts as a depolarizing channel.
        # p = 0 leaves the photon unchanged.
        # p = 1 yields a completely random photon.
        # 0 < p < 1 yields a partially random photon.
        if p < 0 or p > 1:
            raise InputError
        theta = np.arccos(1 - 2*random.uniform(0,1)*p)
        phi   = p*(2*random.uniform(0,1) - 1)*np.pi
        lamb  = p*(2*random.uniform(0,1) - 1)*np.pi
        self.applyUnitaryGate(theta, phi, lamb)

    def applyAttenuation(self, r):
        # This operation acts as a partially reflecting beam splitter.
        # r = 0 leaves the photon unchanged.
        # r = 1 completely absorbs the photon, leaving a vacuum state.
        # 0 < r < 1 partially attenuates the photon and adds some vacuum.
        # r is the reflectivity.
        if r < 0 or r > 1:
            raise InputError
        t = np.sqrt(1-r*r) # t is the transmissivity.
        vac = Qubit()
        vac.prepareVacuum()
        self.alpha = (self.alpha)*t + (vac.alpha)*r
        self.beta  = (self.beta )*t + (vac.beta)*r