# tripartiteSynpase

Main files for different simulation settings are in different directories:
- **ryr** : Control (SERCAPumps and RyR)
- **ns** : SERCA Blocked (none)
- **serca** : SERCA without receptors (SERCAPumps)
- **ip3** : IP3R SERCA Pumps and IP3R
- **recon-ns** : SERCA Blocked (none) for simulations in reconstruction geometry
- **recon-ryr** : Control (SERCAPumps and RyR) for simulations in reconstruction geometry
- **small-ns** : SERCA Blocked (none) for simulations in small canonical geometry
- **small-ryr** : Control (SERCAPumps and RyR) for simulations in small canonical geometry

Examples main mdl files (the files that needs to be run by MCell) are:
- RS20p20hz.mdl
- RSI20V100.mdl

**I20V80** is short for "**I**nterspike interval of **20** ms and **80** **V**DCC" for a paired pulse stimulus.

**20p20hz** is short for "**20** pulses at **10hz** for a train stimulus.

Run these mdl files through terminal (linux) or command prompt (windows) with following command:
```
mcell RSI20V80.mdl
```

Visit the [MCell Webpage](http://www.mcell.org/) for documentation, installation and tutorial on MCell. Due to major changes in mcell, this model is not compatible with latest version of mcell. Use mcell v3.3 instead.
