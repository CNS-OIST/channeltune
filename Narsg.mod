TITLE resurgent sodium channel

COMMENT
Neuron implementation of a resurgent sodium channel (with blocking particle)
Based om updated kinetic parameters from Raman and Bean, Biophys.J. 80 (2001) 729  

Modified from Khaliq et al., J.Neurosci. 23(2003)4899
by qt-correction of all rate constants 

Laboratory for Neuronal Circuit Dynamics
RIKEN Brain Science Institute, Wako City, Japan
http://www.neurodynamics.brain.riken.jp

Reference: Akemann and Knoepfel, J.Neurosci. 26 (2006) 4602
Date of Implementation: May 2005
Contact: akemann@brain.riken.jp

ENDCOMMENT

NEURON {
  SUFFIX Narsg
  USEION na READ ena WRITE ina
  RANGE g, gbar, ina, Con, Coff, Oon, Ooff, alpha, beta, gamma, delta, epsilon, zeta, x1, x2, x3, x4, x5, x6, vshift

}

UNITS { 
	(mV) = (millivolt)
	(S) = (siemens)
}

CONSTANT {
	q10 = 3
}

PARAMETER {
	gbar = 0.016 (S/cm2)
	vshift = 0.0 (mV)
	celsius (degC)

	: kinetic parameters
	: Con = 0.005			(/ms)					: closed -> inactivated transitions
	: Coff = 0.5			(/ms)					: inactivated -> closed transitions
	: Oon = 0.75			(/ms)					: open -> Ineg transition
	: Ooff = 0.005		(/ms)					: Ineg -> open transition
	: alpha = 150			(/ms)					: activation
	: beta = 3			(/ms)					: deactivation
	: gamma = 150			(/ms)					: opening
	: delta = 40			(/ms)					: closing, greater than BEAN/KUO = 0.2
	: epsilon = 1.75		(/ms)					: open -> Iplus for tau = 0.3 ms at +30 with x5
	: zeta = 0.03			(/ms)					: Iplus -> open for tau = 25 ms at -30 with x6

	: Vdep
	: x1 = 20				(mV)								: Vdep of activation (alpha)
	: x2 = -20			(mV)								: Vdep of deactivation (beta)
	: x3 = 1e12			(mV)								: Vdep of opening (gamma)
	: x4 = -1e12			(mV)								: Vdep of closing (delta)
	: x5 = 1e12			(mV)								: Vdep into Ipos (epsilon)
	: x6 = -25			(mV)								: Vdep out of Ipos (zeta)

	Con         (1/ms)      : closed -> inactivated transitions
    Coff            (1/ms)      : inactivated -> closed transitions
    Oon             (1/ms)      : open -> Ineg transition
    Ooff        (1/ms)      : Ineg -> open transition
    alpha           (1/ms)      : activation
    beta            (1/ms)      : deactivation
    gamma           (1/ms)      : opening
    delta           (1/ms)      : closing, greater than BEAN/KUO = 0.2
    epsilon         (1/ms)      : open -> Iplus for tau = 0.3 ms at +30 with x5
    zeta            (1/ms)      : Iplus -> open for tau = 25 ms at -30 with x6
    
    : Vdep
    x1              (mV)                                : Vdep of activation (alpha)
    x2          (mV)                                : Vdep of deactivation (beta)
    x3          (mV)                                : Vdep of opening (gamma)
    x4          (mV)                                : Vdep of closing (delta) 
    x5          (mV)                                : Vdep into Ipos (epsilon)
    x6          (mV)                                : Vdep out of Ipos (zeta)


}

ASSIGNED {
	alfac   				: microscopic reversibility factors
	btfac				

	: rates
	f01  		(/ms)
	f02  		(/ms)
	f03 		(/ms)
	f04			(/ms)
	f0O 		(/ms)
	fip 		(/ms)
	f11 		(/ms)
	f12 		(/ms)
	f13 		(/ms)
	f14 		(/ms)
	f1n 		(/ms)
	fi1 		(/ms)
	fi2 		(/ms)
	fi3 		(/ms)
	fi4 		(/ms)
	fi5 		(/ms)
	fin 		(/ms)

	b01 		(/ms)
	b02 		(/ms)
	b03 		(/ms)
	b04		(/ms)
	b0O 		(/ms)
	bip 		(/ms)
	b11  		(/ms)
	b12 		(/ms)
	b13 		(/ms)
	b14 		(/ms)
	b1n 		(/ms)
	bi1 		(/ms)
	bi2 		(/ms)
	bi3 		(/ms)
	bi4 		(/ms)
	bi5 		(/ms)
	bin 		(/ms)
	
	v					(mV)
 	ena					(mV)
	ina 					(milliamp/cm2)
	g					(S/cm2)
	qt
}

STATE {
	C1 FROM 0 TO 1
	C2 FROM 0 TO 1
	C3 FROM 0 TO 1
	C4 FROM 0 TO 1
	C5 FROM 0 TO 1
	I1 FROM 0 TO 1
	I2 FROM 0 TO 1
	I3 FROM 0 TO 1
	I4 FROM 0 TO 1
	I5 FROM 0 TO 1
	O FROM 0 TO 1
	B FROM 0 TO 1
	I6 FROM 0 TO 1
}

BREAKPOINT {
	SOLVE activation METHOD sparse
 	g = gbar * O
 	ina = g * (v - vshift - ena)
}

INITIAL {
	qt = q10^((celsius-22 (degC))/10 (degC))
	rates(v - vshift)
	SOLVE seqinitial
}

KINETIC activation
{
	rates(v - vshift)
	~ C1 <-> C2					(f01,b01)
	~ C2 <-> C3					(f02,b02)
	~ C3 <-> C4					(f03,b03)
	~ C4 <-> C5					(f04,b04)
	~ C5 <-> O					(f0O,b0O)
	~ O <-> B					(fip,bip)
	~ O <-> I6					(fin,bin)
	~ I1 <-> I2					(f11,b11)
	~ I2 <-> I3					(f12,b12)
	~ I3 <-> I4					(f13,b13)
	~ I4 <-> I5					(f14,b14)
	~ I5 <-> I6					(f1n,b1n)
	~ C1 <-> I1					(fi1,bi1)
	~ C2 <-> I2					(fi2,bi2)
	~ C3 <-> I3					(fi3,bi3)
 	~ C4 <-> I4					(fi4,bi4)
 	~ C5 <-> I5					(fi5,bi5)

CONSERVE C1 + C2 + C3 + C4 + C5 + O + B + I1 + I2 + I3 + I4 + I5 + I6 = 1
}

LINEAR seqinitial { : sets initial equilibrium
 ~          I1*bi1 + C2*b01 - C1*(    fi1+f01) = 0
 ~ C1*f01 + I2*bi2 + C3*b02 - C2*(b01+fi2+f02) = 0
 ~ C2*f02 + I3*bi3 + C4*b03 - C3*(b02+fi3+f03) = 0
 ~ C3*f03 + I4*bi4 + C5*b04 - C4*(b03+fi4+f04) = 0
 ~ C4*f04 + I5*bi5 + O*b0O - C5*(b04+fi5+f0O) = 0
 ~ C5*f0O + B*bip + I6*bin - O*(b0O+fip+fin) = 0
 ~ O*fip + B*bip = 0

 ~          C1*fi1 + I2*b11 - I1*(    bi1+f11) = 0
 ~ I1*f11 + C2*fi2 + I3*b12 - I2*(b11+bi2+f12) = 0
 ~ I2*f12 + C3*fi3 + I4*bi3 - I3*(b12+bi3+f13) = 0
 ~ I3*f13 + C4*fi4 + I5*b14 - I4*(b13+bi4+f14) = 0
 ~ I4*f14 + C5*fi5 + I6*b1n - I5*(b14+bi5+f1n) = 0
 
 ~ C1 + C2 + C3 + C4 + C5 + O + B + I1 + I2 + I3 + I4 + I5 + I6 = 1
}

PROCEDURE rates(v(mV) )
{
 alfac = (Oon/Con)^(1/4)
 btfac = (Ooff/Coff)^(1/4) 
 f01 = 4 * alpha * exp(v/x1) * qt
 f02 = 3 * alpha * exp(v/x1) * qt
 f03 = 2 * alpha * exp(v/x1) * qt
 f04 = 1 * alpha * exp(v/x1) * qt
 f0O = gamma * exp(v/x3) * qt
 fip = epsilon * exp(v/x5) * qt
 f11 = 4 * alpha * alfac * exp(v/x1) * qt
 f12 = 3 * alpha * alfac * exp(v/x1) * qt
 f13 = 2 * alpha * alfac * exp(v/x1) * qt
 f14 = 1 * alpha * alfac * exp(v/x1) * qt
 f1n = gamma * exp(v/x3) * qt
 fi1 = Con * qt
 fi2 = Con * alfac * qt
 fi3 = Con * alfac^2 * qt
 fi4 = Con * alfac^3 * qt
 fi5 = Con * alfac^4 * qt
 fin = Oon * qt

 b01 = 1 * beta * exp(v/x2) * qt
 b02 = 2 * beta * exp(v/x2) * qt
 b03 = 3 * beta * exp(v/x2) * qt
 b04 = 4 * beta * exp(v/x2) * qt
 b0O = delta * exp(v/x4) * qt
 bip = zeta * exp(v/x6) * qt
 b11 = 1 * beta * btfac * exp(v/x2) * qt
 b12 = 2 * beta * btfac * exp(v/x2) * qt
 b13 = 3 * beta * btfac * exp(v/x2) * qt
 b14 = 4 * beta * btfac * exp(v/x2) * qt
 b1n = delta * exp(v/x4) * qt
 bi1 = Coff * qt
 bi2 = Coff * btfac * qt
 bi3 = Coff * btfac^2 * qt
 bi4 = Coff * btfac^3 * qt
 bi5 = Coff * btfac^4 * qt
 bin = Ooff * qt
}

