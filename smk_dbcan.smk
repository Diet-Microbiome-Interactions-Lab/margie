import os

genomes, = glob_wildcards(f'FAAs/{{mag}}.faa')

print(genomes)
rule all:
    input:
        expand("dbcan/{mag}/{mag}_overview.txt", mag=genomes),



rule Run_DbCan:
    input:
        origin=f'FAAs/{{mag}}.faa'
    params:
        outdir=f'dbcan/{{mag}}/',
        outpref=f'{{mag}}_'
    output:
        final=f'dbcan/{{mag}}/{{mag}}_overview.txt'
    shell:
        """
        run_dbcan.py {input.origin} protein --out_dir {params.outdir} --tf_cpu 10 --out_pre {params.outpref} \
        --db_dir /depot/lindems/data/Databases/CAZyme
        """
