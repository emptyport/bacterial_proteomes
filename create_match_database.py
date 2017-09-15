import os
import MySQLdb
from Bio.Blast import NCBIXML
from Bio.Blast.Applications import NcbiblastpCommandline as blastp_cline

print '========================================'
print 'Establishing connection with MySQL'

host = '127.0.0.1'
user = 'pyscript'
password = 'bacteria'
port = 3306
db = 'bacteria'

conn = MySQLdb.Connection(
    host=host,
    user=user,
    passwd=password,
    port=port,
    db=db
)

cursor = conn.cursor()

# First things first we clear out the existing table
print 'Clearing `protein_pairs` table'
conn.query('DROP TABLE IF EXISTS `protein_pairs`')
conn.commit()

sql = '''CREATE TABLE `protein_pairs` (
            `id` BIGINT NOT NULL AUTO_INCREMENT,
            `proteinA` INT NULL,
            `proteinB` INT NULL,
            PRIMARY KEY (`id`)
        )
        '''
conn.query(sql)
conn.commit()

print 'Getting list of organisms...'
sql = 'SELECT * FROM `organisms`'
cursor.execute(sql)
organisms = cursor.fetchall()
l = len(organisms)

pairs = []

curPath = os.path.dirname(os.path.realpath(__file__))

print 'Running BLAST...'
for i in range(0, l):
    sql = 'SELECT `id`,`sequence` FROM `proteins` WHERE `organism`='
    sql += "'" + organisms[i][0] + "'"
    cursor.execute(sql)
    proteins = cursor.fetchall()
    
    for j in range(i+1, l):
        blast_db_name = organisms[j][0]
        
        outfile = open('input.fasta', 'w')
        for protein in proteins:
            id = protein[0]
            seq = protein[1]
            outfile.write('>')
            outfile.write(str(id))
            outfile.write('\n')
            outfile.write(seq)
            outfile.write('\n\n')
        outfile.close()

        full_input = curPath + '/input.fasta'
        full_db = curPath + '/blast_db/' + blast_db_name
        full_output = 'blast_output.xml'

        blastp = blastp_cline(query=full_input, db=full_db, evalue=0.001, outfmt=5, out=full_output)

        result_handle = open('blast_output.xml')
        blast_record = NCBIXML.read(result_handle)
        print i,j,blast_record.alignments[0].hsps[0].identities
            

        
        
        
        
        
        
        
        
        
        
        
        
        
        '''
        
        sql = 'SELECT `id`,`sequence` FROM `proteins` WHERE `organism`='
        sql += "'" + organisms[j][0] + "'"
        print i,j
        cursor.execute(sql)
        proteinsB = cursor.fetchall()

        # Here we do the pairwise alignments
        for pA in proteinsA:
            idA = pA[0]
            seqA = pA[1]
            bestMatch = -1
            maxScore = 0
            for pB in proteinsB:
                idB = pB[0]
                seqB = pB[1]
                alignments = pairwise2.align.globalds(seqA, seqB, blosum62, -10, -0.5)
                score = alignments[0][2]
                if score > maxScore:
                    maxScore = score
                    idB = pB[0]
            
            cursor.execute(
                INSERT INTO `protein_pairs`
                (proteinA, proteinB)
                VALUES
                (%s, %s)
                ,
                [idA, idB]
            )
            '''

        