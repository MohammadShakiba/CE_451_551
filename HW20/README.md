# 1. Geometry optimization of methylamine using ORCA

Here, we will be using ORCA to optimize the geometry of methylamine (CH5N). 

The keywords that are used are:

```
! RHF b3lyp def2-SVP LARGEPRINT PRINTBASIS PRINTGAP TightSCF ALLPOP Opt AnFreq NumFreq bohrs
```

We use `TightSCF` in order to compute the forces more accurately so that the optimizer be able to better optimize the geometry by more accurate forces.

Also, we use parallel calculations using 16 number of processors:

```
%pal nprocs 16
end
```

The coordinates are given in a `xyz` file called `mta.xyz`.

```
* xyzfile 0 1 mta.xyz
```

The number of optimization steps is defined as:

```
%geom
  MaxIter 100
end
```

To run the calculations, we need to use the full path to ORCA:


```
module load orca/4.2.1
which orca

$ /util/academic/orca/orca_4_2_1_linux_x86-64_openmpi314/orca

/util/academic/orca/orca_4_2_1_linux_x86-64_openmpi314/orca geo_opt.inp > out_geo_opt.log
```


# 2. TD-DFT calculations using ORCA

For excited states calculations we use the following inputs:

```
%tddft 
  NRoots 25
end
```

And for outputting the cube files for HOMO and LUMO of methylamine, we use the following script in the input file:

```
%plots Format Cube
  MO("HOMO-8.cube",8,0);
  MO("LUMO-9.cube",9,0);
end
```


# 3. Plotting the properties


All the properties are plotted in the Jupyter notebook `plot_properties.ipynb`. We use several scripts and commands to extract data from the output files and all are explained in the Jupyter file.



