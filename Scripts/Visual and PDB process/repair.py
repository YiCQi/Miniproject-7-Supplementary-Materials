from pdbfixer import PDBFixer
from openmm.app import PDBFile

if not hasattr(fixer, 'missingResidues'):
    fixer.missingResidues = {}

fixer = PDBFixer(filename="3fie.pdb")
fixer.findMissingAtoms()
fixer.addMissingAtoms()
PDBFile.writeFile(fixer.topology, fixer.positions, open("3fie_fixed.pdb", "w"))
