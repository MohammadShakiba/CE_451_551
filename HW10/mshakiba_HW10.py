#!/usr/bin/env python
# coding: utf-8

# In[10]:


import numpy as np
import time


# In[3]:


def read_cp2k_tddfpt_log_file( params ):
    """
    This function reads log files generated from TD-DFPT calculations using CP2K and returns the TD-DFPT
    excitation energies, Slater determinent states in terms of the Kohn-Sham orbital indicies, 
    and the Slater determinent coefficients that comprise the multi-configurational electronic states
    
    Args:
        params ( dictionary ): parameters dictionary 

            logfile_name ( string ): name of the log file for this particular timestep

            number_of_states ( int ): how many ci states to consider
    
            tolerance ( float ): the tolerance for accepting SDs are members of the CI wavefunctions
    
            isUKS ( Boolean ): flag for whether or not a spin-polarized Kohn-Sham basis is being used. TRUE means
                                 that a spin-polarized Kohn-Sham basis is being used.
    Returns:
        excitation_energies ( list ): The excitation energies in the log file.

        ci_basis ( list ): The CI-basis configuration.

        ci_coefficients ( list ): The coefficients of the CI-states.

        spin_components (list): The spin component of the excited states.
    """

    # Critical parameters
    #critical_params = [ "logfile_name", "number_of_states" ]
    # Default parameters
    #default_params = { "tolerance":0.05, "isUKS": 0}
    # Check input
    #comn.check_input(params, default_params, critical_params)
    
    logfile_name = params["logfile_name"]
    number_of_states = int(params["number_of_states"])
    tolerance = float(params["tolerance"])
    isUKS = int(params["isUKS"])


    f = open( logfile_name, 'r' )
    lines = f.readlines()
    f.close()

    for i in range( 0, len(lines) ):
        tmp_line = lines[i].lower().split()
        if 'excitation' in tmp_line:
            if 'analysis' in tmp_line:

                # When found the line in which contains 'Excitation analysis' in 
                # the log file, append it in the variable exc_anal_line
                exc_anal_line = i

        if 'states' in tmp_line:
            if 'multiplicity' in tmp_line:

                # Here we search for the line that contains 'R-TDDFPT states of multiplicity 1'
                # or 'U-TDDFPT states of multiplicity 1' in the log file
                r_tddfpt_line = i

    excitation_energies = []
    # Old version
    ## Start from 5 lines after finding the line contaning 'R-TDDFPT states of multiplicity 1'
    ## This is because they contain the energies from that line.
    ##for i in range( r_tddfpt_line+5, len( lines ) ):
    ##    tmp_line = lines[i].split()
    ##    if len( tmp_line ) == 0:
    ##        break
    ##    excitation_energies.append( float( tmp_line[2] ) )

    for i in range(len(lines)):
        if 'TDDFPT|' in lines[i]:
            try:
                tmp = lines[i].split()
                exc_ener = float(tmp[2])
                excitation_energies.append(exc_ener)
            except:
                pass

    # Start from 5 lines after finding the line contaning 'Excitation analysis'
    # From that point we have the state numbers with their configurations.
    # So, we append the lines which contain only 'State number' and stop
    # whenever we reach to a blank line.
    state_num_lines = []
    for i in range( exc_anal_line+5, len( lines ) ):
        tmp_line = lines[i].split()
        if isUKS == 1:

            if len( tmp_line ) == 0 or '----' in lines[i]:
                state_num_lines.append( i )
                break
            if len( tmp_line )==1 or len( tmp_line )==3:
                state_num_lines.append(i)

        else:

            if len( tmp_line ) == 0 or '----' in lines[i]:
                state_num_lines.append( i )
                break
            if len(lines[i].split())==1:
                state_num_lines.append(i)
            elif len( tmp_line ) > 1:
                if tmp_line[0].isdigit() and not( tmp_line[1].isdigit() ):
                    state_num_lines.append( i )


    # Setting up the CI-basis list and their coefficients list
    ci_basis = []
    ci_coefficients = []
    spin_components = []
    for i in range( number_of_states ):

        # states and their coefficients for each excited state
        tmp_state              = []
        tmp_state_coefficients = []
        tmp_spin = []
        for j in range( state_num_lines[i]+1, state_num_lines[i+1] ):
            
            # Splitting lines[j] into tmp_splitted_line
            tmp_splitted_line = lines[j].split()

            # If we are using the spin-polarized Kohn-Sham basis, then the size of the split line is different
            # from the size of the split line when using the spin-unpolarized Kohn-Sham basis
            if isUKS == 1:

                ci_coefficient = float( tmp_splitted_line[4] )
                if ci_coefficient**2 > tolerance:
                    # We need to remove the paranthesis from the 2nd element of the temporary splitted line
                    tmp_spin.append( tmp_splitted_line[1].replace('(','').replace(')','') )
                    tmp_state.append( [ int( tmp_splitted_line[0] ), int( tmp_splitted_line[2] ) ]  )
                    tmp_state_coefficients.append( ci_coefficient  )

            # Here, we have the spin-unpolarize Kohn-Sham basis
            # For this case, spin-components will just return all alpha
            else:
                ci_coefficient = float( tmp_splitted_line[2] )
                if ci_coefficient**2 > tolerance:
                    tmp_spin.append( "alp" )
                    tmp_state.append( [ int( tmp_splitted_line[0] ), int( tmp_splitted_line[1] ) ]  )
                    tmp_state_coefficients.append( ci_coefficient  )

        # Append the CI-basis and and their coefficients for
        # this state into the ci_basis and ci_coefficients lists
        ci_basis.append( tmp_state )
        ci_coefficients.append( tmp_state_coefficients )
        spin_components.append( tmp_spin )

    return excitation_energies[0:number_of_states], ci_basis, ci_coefficients, spin_components


# In[6]:


params = {}
params['logfile_name'] = 'step_4999.log'
params['tolerance'] = 0.0
params['isUKS'] = False
params['number_of_states'] = 10
excitation_energies, ci_basis, ci_coefficients, spin_components = read_cp2k_tddfpt_log_file(params)
print('Exctation energies are:', excitation_energies)
print('\nCI basis are:', ci_basis)
print('\nCI coefficients are:', ci_coefficients)
print('\nSpin components are:', spin_components)


# In[12]:


def read_molog_file(filename: str):
    """
    This function reads the coefficiets of the molecular orbitals printed out
    during the MD or a single-point calculation for a structure using CP2K.
    The format of the MO coefficients in CP2K is in column format so the coeffiecients
    are written in a column. You can check this for an MOLog file printed out by CP2K.
    The number of columns in MOLog file is based on the DFT%PRINT%MO%NDIGITS. The larger the 
    number of digits (NDIGITS), the lower number of columns. This function is written in a way
    that will automatically extract all the coefficients for all the eigenvectors and returns them
    and their energies. It will also designed for reading the coefficients for MOs in different
    K-points if used by user in the CP2K input (DFT%KPOINT).
    
    Args:
    
        filename (string): The name of the MOLog ile.
        
    Returns:
    
        mo_coeffs (list): The list containing the MO coefficients for each K-point.
        
        mo_energies (liest): The list containing the energies of MOs for each K-point.
    
    """
    # first is there any k-point or not??
    file = open(filename,'r')
    lines = file.readlines()
    file.close()
    
    is_kpoint = False
    # The K-point will show itself at the beginning
    # so since the files are large we only search the first 
    # couple of lines, say first 10
    for i in range(len(lines)):
        if 'K POINT' in lines[i]:
            is_kpoint = True
            break
    
    # set a timer
    timer = time.time()
    if is_kpoint:
        # If K-point
        print('Found K-point, will proceed reading the coefficients',
        'for each K POINT...')
        # Lines with K POINT
        kpoint_lines = []
        # Lines with Fermi energy
        fermi_lines = []
        for i in range(len(lines)):
            if 'K POINT'.lower() in lines[i].lower():
                kpoint_lines.append(i)
            if 'Fermi'.lower() in lines[i].lower():
                fermi_lines.append(i)
        # All the coefficients
        mo_coeffs = []
        # All the energies
        mo_energies = []
        # Loop over all the K-points
        for i in range(len(kpoint_lines)):
            # start lines
            startl = kpoint_lines[i]
            if i==len(kpoint_lines)-1:
                # end line
                endl = len(lines)
            else:
                endl = kpoint_lines[i+1]
            # All the eigenvectors for each K-point
            eigenvectors = []
            # Lines with length less than or equal to 4
            leq_4_lines = []
            # Energies for a K-point
            energies = []
            # Find the leq_4_lines indicies
            for j in range(startl, endl):
                # lines with less than or equal to 4
                tmp = lines[j].split()
                if 0 < len(tmp)<=4:
                    if 'Fermi' not in tmp and 'gap' not in tmp:
                        leq_4_lines.append(j)
            # The lines with MO number
            mo_num_lines = leq_4_lines[0::3]
            # The lines wit energies
            energy_lines = leq_4_lines[1::3]
            # Find the energies for a K-point
            for j in energy_lines:
                tmp = lines[j].split()
                for k1 in range(4):
                    try:
                        energy = float(tmp[k1])
                        energies.append(energy)
                    except:
                        pass
            # Append the energies for this K-point
            mo_energies.append(np.array(energies))
            # Occupation lines, Needed to define the start and end
            # lines to find the coefficients
            occ_lines = leq_4_lines[2::3]
            # Now reading the coefficients
            for j in range(len(mo_num_lines)):
                start_l = occ_lines[j]+1
                if j==len(mo_num_lines)-1:
                    end_l = fermi_lines[i]
                else:
                    end_l = mo_num_lines[j+1]
                # This part with try and except make the code 
                # to consider for different number of columns
                # So the user does not need to specify the number
                # of columns or the number of atomic orbitals etc...
                for k1 in range(4,8):
                    # Each eigenvector for this K-point
                    eigenvector = []
                    for k2 in range(start_l, end_l):
                        tmp = lines[k2].split()
                        try:
                            eig_val = float(tmp[k1])
                            eigenvector.append(eig_val)
                        except:
                            pass
                    if len(eigenvector)!=0:
                        # Now this variable contains all the eigenvectors 
                        # for this K-point
                        eigenvectors.append(np.array(eigenvector))
            
            print('Done reading coefficients for K-point %d'%(i+1))
            # The mo_coeffs contains the eigenvectors. After this
            # we start for another K-point.
            mo_coeffs.append(eigenvectors)
        
    else:
        # The same procedure as above for K-point with this 
        # difference that there is no K-point
        fermi_lines = []
        for i in range(len(lines)):
            if 'Fermi'.lower() in lines[i].lower():
                fermi_lines.append(i)
        
        mo_coeffs = []
        mo_energies = []
        # start lines
        startl = 3 
        endl = fermi_lines[0] 
        eigenvectors = []
        leq_4_lines = []
        energies = []
        for j in range(startl, endl):
            # lines with less than or equal to 4
            tmp = lines[j].split()
            if 0 < len(tmp)<=4:
                if 'Fermi' not in tmp and 'gap' not in tmp:
                    leq_4_lines.append(j)

        mo_num_lines = leq_4_lines[0::3]
        energy_lines = leq_4_lines[1::3]
        for j in energy_lines:
            tmp = lines[j].split()
            for k1 in range(4):
                try:
                    energy = float(tmp[k1])
                    energies.append(energy)
                except:
                    pass
        mo_energies.append(np.array(energies))
        occ_lines = leq_4_lines[2::3]
        for j in range(len(mo_num_lines)):
            start_l = occ_lines[j]+1
            if j==len(mo_num_lines)-1:
                end_l = fermi_lines[0]
            else:
                end_l = mo_num_lines[j+1]
            for k1 in range(4,8):
                eigenvector = []
                for k2 in range(start_l, end_l):
                    tmp = lines[k2].split()
                    try:
                        eig_val = float(tmp[k1])
                        eigenvector.append(eig_val)
                    except:
                        pass
                if len(eigenvector)!=0:
                    eigenvectors.append(np.array(eigenvector))

        print('Done reading coefficients for the MOLog file')
        mo_coeffs.append(eigenvectors)
    print('Elapsed time:', time.time()-timer)
            
    return mo_energies, mo_coeffs


# In[21]:


mo_energies, mo_coeffs = read_molog_file('graphene_kp_dos-C-1_0.MOLog')
print('\nEnergies are:', np.array(mo_energies))
print('\nMolecular orbitals coefficients shape is:', np.array(mo_coeffs).shape)
print('\nMolecular orbitals coefficients are:', np.array(mo_coeffs))

