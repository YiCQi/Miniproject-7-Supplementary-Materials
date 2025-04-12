# Miniproject 7 Supplementary Materials
This repository includes code, document, and supplementary figures/tables for miniproject: Investigating the Temperature Effect on the Stability of the VAMP–BoNT F Complex Using Molecular Dynamics Simulations.

General Process:
<img width="349" alt="1744479065518" src="https://github.com/user-attachments/assets/af548b7a-b9c2-451e-b6b6-f4eb3dd98dec" />

**Remove H2O**
```
grep -v HOH 3fie.pdb > 3FIE_clean.pdb
```

**Generate topol**
```
/software/gromacs-2024.3/build/bin/gmx_mpi pdb2gmx -f 3FIE_clean_rename.pdb -o 3FIE_processed.gro -water spce -missing
```

**Define Box**
```
/software/gromacs-2024.3/build/bin/gmx_mpi editconf -f 3FIE_processed.gro -o 3FIE_newbox.gro -c -d 1.0 -bt cubic
```

**Add Sol**
```
/software/gromacs-2024.3/build/bin/gmx_mpi solvate -cp 3FIE_newbox.gro -cs spc216.gro -o 3FIE_solv.gro -p topol.top
```

**Add ion**
```
/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f ions.mdp -c 3FIE_solv.gro -p topol.top -o ions.tpr
/software/gromacs-2024.3/build/bin/gmx_mpi genion -s ions.tpr -o 3FIE_solv_ions.gro -p topol.top -pname NA -nname CL -neutral
```

**Energy Minimization**
```
/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f minim.mdp -c 3FIE_solv_ions.gro -p topol.top -o em.tpr
/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -v -deffnm em -nb gpu -ntomp 8 -gpu_id 1
/software/gromacs-2024.3/build/bin/gmx_mpi energy -f em.edr -o potential.xvg
```

**Temperature/Pressure Blance**
Temperature
```
/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr
/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -deffnm nvt -nb gpu -ntomp 8 -gpu_id 1
/software/gromacs-2024.3/build/bin/gmx_mpi energy -f nvt.edr -o temperature.xvg

/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f nvt_280.mdp -c em.gro -r em.gro -p topol.top -o nvt_280.tpr
/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -deffnm nvt_280 -nb gpu -ntomp 8 -gpu_id 1
/software/gromacs-2024.3/build/bin/gmx_mpi energy -f nvt_280.edr -o temperature_280.xvg

/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f nvt_300.mdp -c em.gro -r em.gro -p topol.top -o nvt_300.tpr
/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -deffnm nvt_300 -nb gpu -ntomp 8 -gpu_id 1
/software/gromacs-2024.3/build/bin/gmx_mpi energy -f nvt_300.edr -o temperature_300.xvg

/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f nvt_320.mdp -c em.gro -r em.gro -p topol.top -o nvt_320.tpr
/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -deffnm nvt_320 -nb gpu -ntomp 8 -gpu_id 1
/software/gromacs-2024.3/build/bin/gmx_mpi energy -f nvt_320.edr -o temperature_320.xvg
```

Pressure
```
/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -o npt.tpr
/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -deffnm npt -nb gpu -ntomp 8 -gpu_id 1
/software/gromacs-2024.3/build/bin/gmx_mpi energy -f npt.edr -o pressure.xvg
/software/gromacs-2024.3/build/bin/gmx_mpi energy -f npt.edr -o density.xvg

/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f npt_280.mdp -c nvt_280.gro -r nvt_280.gro -t nvt_280.cpt -p topol.top -o npt_280.tpr 
/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -deffnm npt_280 -nb gpu -ntomp 8 -gpu_id 1 
/software/gromacs-2024.3/build/bin/gmx_mpi energy -f npt_280.edr -o pressure_280.xvg 
/software/gromacs-2024.3/build/bin/gmx_mpi energy -f npt_280.edr -o density_280.xvg

/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f npt_300.mdp -c nvt_300.gro -r nvt_300.gro -t nvt_300.cpt -p topol.top -o npt_300.tpr 
/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -deffnm npt_300 -nb gpu -ntomp 8 -gpu_id 1 
/software/gromacs-2024.3/build/bin/gmx_mpi energy -f npt_300.edr -o pressure_300.xvg 
/software/gromacs-2024.3/build/bin/gmx_mpi energy -f npt_300.edr -o density_300.xvg

/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f npt_320.mdp -c nvt_320.gro -r nvt_320.gro -t nvt_320.cpt -p topol.top -o npt_320.tpr 
/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -deffnm npt_320 -nb gpu -ntomp 8 -gpu_id 1 
/software/gromacs-2024.3/build/bin/gmx_mpi energy -f npt_320.edr -o pressure_320.xvg 
/software/gromacs-2024.3/build/bin/gmx_mpi energy -f npt_320.edr -o density_320.xvg
```
### **MD**! 
```
/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f 280K_50ns.mdp -c npt.gro -t npt.cpt -p topol.top -o 280K_50ns.tpr
/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f 300K_50ns.mdp -c npt.gro -t npt.cpt -p topol.top -o 300K_50ns.tpr
/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f 320K_50ns.mdp -c npt.gro -t npt.cpt -p topol.top -o 320K_50ns.tpr

/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f 280K_50ns.mdp -c npt_280.gro -t npt_280.cpt -p topol.top -o 280K_50ns.tpr
/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f 300K_50ns.mdp -c npt_300.gro -t npt_300.cpt -p topol.top -o 300K_50ns.tpr
/software/gromacs-2024.3/build/bin/gmx_mpi grompp -f 320K_50ns.mdp -c npt_320.gro -t npt_320.cpt -p topol.top -o 320K_50ns.tpr

/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -v -deffnm 280K_50ns -nb gpu -ntomp 8 -gpu_id 1
/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -v -deffnm 300K_50ns -nb gpu -ntomp 8 -gpu_id 1
/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -v -deffnm 320K_50ns -nb gpu -ntomp 8 -gpu_id 1

/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -v -s 280K_50ns.tpr -deffnm rep_280K_50ns -nb gpu -ntomp 8 -gpu_id 1
/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -v -s 300K_50ns.tpr -deffnm rep_300K_50ns -nb gpu -ntomp 8 -gpu_id 1
/software/gromacs-2024.3/build/bin/gmx_mpi mdrun -v -s 320K_50ns.tpr -deffnm rep_320K_50ns -nb gpu -ntomp 8 -gpu_id 1
```

**Analysis**
```
 ’‘1 0
/software/gromacs-2024.3/build/bin/gmx_mpi trjconv -s 280K_50ns.tpr -f 280K_50ns.xtc -o 280K_50ns_noPBC.xtc -pbc mol -center
/software/gromacs-2024.3/build/bin/gmx_mpi trjconv -s 300K_50ns.tpr -f 300K_50ns.xtc -o 300K_50ns_noPBC.xtc -pbc mol -center
/software/gromacs-2024.3/build/bin/gmx_mpi trjconv -s 320K_50ns.tpr -f 320K_50ns.xtc -o 320K_50ns_noPBC.xtc -pbc mol -center
```
```
/software/gromacs-2024.3/build/bin/gmx_mpi trjconv -s 320K_50ns.tpr -f 320K_50ns.xtc -o 320K_50ns_noPBC_10.xtc -pbc mol -center -ndec 10
```


RMSD ’‘4 4
```
/software/gromacs-2024.3/build/bin/gmx_mpi rms -s 280K_50ns.tpr -f 280K_50ns_noPBC.xtc -o 280K_50ns_rmsd.xvg -tu ns
/software/gromacs-2024.3/build/bin/gmx_mpi rms -s 300K_50ns.tpr -f 300K_50ns_noPBC.xtc -o 300K_50ns_rmsd.xvg -tu ns
/software/gromacs-2024.3/build/bin/gmx_mpi rms -s 320K_50ns.tpr -f 320K_50ns_noPBC.xtc -o 320K_50ns_rmsd.xvg -tu ns
```
RMSF 1
```
/software/gromacs-2024.3/build/bin/gmx_mpi rmsf -s 280K_50ns.tpr -f 280K_50ns.xtc -o 280K_50ns_rmsf.xvg -b 0 -e 50 -res 
/software/gromacs-2024.3/build/bin/gmx_mpi rmsf -s 300K_50ns.tpr -f 300K_50ns.xtc -o 300K_50ns_rmsf.xvg -b 0 -e 50 -res 
/software/gromacs-2024.3/build/bin/gmx_mpi rmsf -s 320K_50ns.tpr -f 320K_50ns.xtc -o 320K_50ns_rmsf.xvg -b 0 -e 50 -res
```

’‘4 4
```
/software/gromacs-2024.3/build/bin/gmx_mpi rms -s em.tpr -f 280K_50ns_noPBC.xtc -o 280K_50ns_rmsd_xtal.xvg -tu ns
/software/gromacs-2024.3/build/bin/gmx_mpi rms -s em.tpr -f 300K_50ns_noPBC.xtc -o 300K_50ns_rmsd_xtal.xvg -tu ns
/software/gromacs-2024.3/build/bin/gmx_mpi rms -s em.tpr -f 320K_50ns_noPBC.xtc -o 320K_50ns_rmsd_xtal.xvg -tu ns
```

’‘1
```
/software/gromacs-2024.3/build/bin/gmx_mpi gyrate -s 280K_50ns.tpr -f 280K_50ns_noPBC.xtc -o 280K_50ns_gyrate.xvg
/software/gromacs-2024.3/build/bin/gmx_mpi gyrate -s 300K_50ns.tpr -f 300K_50ns_noPBC.xtc -o 300K_50ns_gyrate.xvg
/software/gromacs-2024.3/build/bin/gmx_mpi gyrate -s 320K_50ns.tpr -f 320K_50ns_noPBC.xtc -o 320K_50ns_gyrate.xvg
```

```
/software/gromacs-2024.3/build/bin/gmx_mpi editconf -f 280K_50ns.gro -o 280K_50ns_converted.pdb
/software/gromacs-2024.3/build/bin/gmx_mpi editconf -f 300K_50ns.gro -o 300K_50ns_converted.pdb
/software/gromacs-2024.3/build/bin/gmx_mpi editconf -f 320K_50ns.gro -o 320K_50ns_converted.pdb
```

Count Hydrogen bonds
```
/software/gromacs-2024.3/build/bin/gmx_mpi hbond -f 280K_50ns_noPBC.xtc -s 280K_50ns.tpr -num hbond_280K.xvg 
/software/gromacs-2024.3/build/bin/gmx_mpi hbond -f 300K_50ns_noPBC.xtc -s 300K_50ns.tpr -num hbond_300K.xvg 
/software/gromacs-2024.3/build/bin/gmx_mpi hbond -f 320K_50ns_noPBC.xtc -s 320K_50ns.tpr -num hbond_320K.xvg
```

dssp Stats
```
/software/gromacs-2024.3/build/bin/gmx_mpi dssp -f 280K_50ns_noPBC.xtc -s 280K_50ns.tpr -num dssp_280K.xvg
/software/gromacs-2024.3/build/bin/gmx_mpi dssp -f 300K_50ns_noPBC.xtc -s 300K_50ns.tpr -num dssp_300K.xvg 
/software/gromacs-2024.3/build/bin/gmx_mpi dssp -f 320K_50ns_noPBC.xtc -s 320K_50ns.tpr -num dssp_320K.xvg 
```

Results:
![image](https://github.com/user-attachments/assets/5b333578-3546-4742-b620-02467c3bd183)
![image](https://github.com/user-attachments/assets/0de59508-16dd-4ba7-91c6-9f8511b0c8f7)
![image](https://github.com/user-attachments/assets/b33b8264-199a-4f5b-8fd0-eebb75326603)
![image](https://github.com/user-attachments/assets/6491111a-2254-406e-95c3-2250d4b2e4e7)

