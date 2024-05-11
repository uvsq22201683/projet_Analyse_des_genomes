aa3to1={
   'ALA':'A', 'VAL':'V', 'PHE':'F', 'PRO':'P', 'MET':'M',
   'ILE':'I', 'LEU':'L', 'ASP':'D', 'GLU':'E', 'LYS':'K',
   'ARG':'R', 'SER':'S', 'THR':'T', 'TYR':'Y', 'HIS':'H',
   'CYS':'C', 'ASN':'N', 'GLN':'Q', 'TRP':'W', 'GLY':'G',
   'MSE':'M',
}

def pdb2seq(path):
    """Extraction de la sequence proteique du fichier .pdb"""
    seq = ""

    f =  open(path,'r')
    for line in f.readlines():
        if line.startswith("ENDMDL"): #fin du fichier
            break
        if line.startswith("SEQRES"): #lighes comportant la sequence proteique
            line_splited = line.split(' ')
            for l in line_splited:
                if l in list(aa3to1.keys()):
                    seq += aa3to1[l] #transformation du code de 3 lettes en code de 1 lettre
    f.close()
    return seq


"""test"""
if __name__ == '__main__':
    path = "xyls_wildtype.pdb"
    print(pdb2seq(path))