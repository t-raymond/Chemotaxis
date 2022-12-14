## REAL WORLD PARAMETERS:

### Current device channel dimensions:

Length: 11mm

Height: 1mm

Width: 1mm

### Initial Chemoattractant concentration:

C0 = 100 nanomolar

### Buffer Solution: Basically water

### Chemoattractant protein:

TGF-Beta

Approximate diffusion constant from particle size 

#### 

r = (1.9)*(1/1000000000) #m 
Radius of spherical particle --> https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3055910/ AND https://www.abcam.com/recombinant-human-tgf-beta-1-protein-active-ab50036.html#:~:text=TGF%2Dbeta1%20is%20a%2025.0,peptide%20and%20latency%2Dassociated%20peptide.

D = (k*T)(6pi*mu*r)

Where k is boltzmann constant (1.380649 * 10^-23 J/K), T is temperature (K), mu is dynamic visc of water (.0006922 Pa * s),
and r is particle radius


## Simulation data for existing product IBIDI Mu-Slide Chemotaxis Chamber

### IBIDI device channel dimensions:

Length: 1mm

Width: 2mm

Height: .07mm

### IBIDI Device does not have any nanofibers, disregard adsoprtion

Ibidi device time to linearize = 26 hours

All other parameters (chemoattractant, buffer, C0) should be same