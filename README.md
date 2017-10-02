# Bacterial Proteome Relationships

> This repository consists of some code I'm developing while learning about gene coupling and co-evolution

> I am on a Linux system, so be aware that some of these commands may not work exactly as they are written on your system. If you are running a bash shell, such as in Linux or Mac systems, these commands might work as written (or you might need to install homebrew if you are on a Mac). If you are on Windows, you can look up equivalent commands or you could try a Linux subsystem for Windows or maybe Cygwin.

## Prerequisites

You will need to have Python installed (at least version 2.7) with the following modules:

* biopython
* progressbar2
* MySQL-python

You will also need to have MySQL installed with a user created for the scripts. For now the user information is coded directly into the scripts near the beginning.

## Obtaining the Data from OrthoDB

> All data is downloaded from http://www.orthodb.org/?page=filelist

#### Ortholog Database

The first step is to download and extract ```ODB.sql.gz``` and get started with the SQL import.

While trying to import the SQL dump, I discovered that there are some incompatibilites with my version of MySQL server. The following steps should resolve the issues. Steps 1-3 were run from the terminal.

1. ```grep -v '/\*' ODB.sql > ODB_mod.sql``` I don't know if this is required, but initially I thought the issue was with the comments in the .sql file so I ran this step to remove them. This step might not actually be necessary, so feel free to skip step 1 for now and see if the following steps work.

2. ```sed -i 's/ TYPE=MyISAM;/;/g' ODB_mod.sql``` This step is required because there are a bunch of "TYPE-MyISAM;" statements that are no longer compatible with MySQL server. This command removes those fragments to make the file compatible with the current MySQL version.

3. ```cat ODB_mod.sql | mysql -u pyscript -p -h localhost bacteria``` will import the .sql file. Replace the user, host, and table with the details of your setup. This took about a full day (24 hours) to insert into my database on my local machine.

4. ```analyze table species,levels,genes,OGs,OG2genes;``` According to the README from OrthoDB, you should run this command from the MySQL prompt to make sure there weren't any errors during import.

#### Protein Sequences

While your ortholog database is importing, go ahead and download and extract all the fasta.tar.gz files, or at least the ones you want to include. Extract them to the same directory as where this code is. Each extract will create a file with the name of the organism group. For example, ```odb9v2_protozoa_fasta.tar.gz``` will create a folder named 'protozoa' that further contains a folder named 'Rawdata' with the fasta files inside that.

Available databases with number of organisms in each (as of Sep. 27, 2017)

* archea (345)
* bacteria (3663)
* fungi (227)
* metazoa (331)
* plants (31)
* protozoa (73)
* viridae (3138)

There aren't as many organisms as you could get from say the Uniprot reference proteomes, but each protein in these files has been assigned to an ortholog group which should make it easy to get going with a SCA analysis.

Once all the gzipped tar files have been extracted, run ```create_protein_database.py``` to create a table of all the protein sequences. Please keep in mind that this script will delete and re-create the ```proteins``` table each time you run it, so if you want to later add in some new fasta files, you will have to either edit the code to not delete the table or just suffer through creating the table again. I believe it took about 45 minutes to an hour on my machine to create the table and insert all the sequences.

#### Other Scripts

The ```create_match_database.py``` and ```make_blast_databases.py``` scripts are from the master branch and currently don't do anything in this branch.


