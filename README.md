# Bacterial Proteome Relationships

> This repository consists of some code I'm developing while learning about gene coupling and co-evolution

## Obtaining the Data
I downloaded bacterial proteomes from Uniprot using the following commands in a bash terminal:
```shell
mkdir bacteria_proteomes

cd bacteria_proteomes

wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Bacteria/*
```
I downloaded the proteomes on Tuesday, Sep 5, 2017. It took a good part of the day to finish. The "Date Modified" says 8/30/17 on Uniprot's ftp server.

From here, I ran the script ```create_protein_database.py``` to save the proteins to a MySQL table. Once you install MySQL, just create a database and user and put that information in the script; the script will take care of creating the table. The table structure is as follows:

* **id** is the primary key and is set to autoincrement

* **organism** follows the format "UP000028641" and as far as I can tell is an identifier set by Uniprot

* **header** is the header information for each protein sequence in the fasta file

* **sequence** is the protein sequence itself

Each fasta file is uncompressed, read into memory, and then each protein sequence is inserted into the database. Even though each file is being inserted all at once, this process is still quite time consuming (there are over 6000 proteomes to process).

## Next Steps
* Multiple sequence alignment
* Looking at conserved residues
* Putting it all together
