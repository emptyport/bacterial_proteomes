import MySQLdb
from Bio import pairwise2
from Bio.SubsMat.MatrixInfo import blosum62

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
print organisms[0][0]
l = len(organisms)

pairs = []

for i in range(0, l):
    sql = 'SELECT `id`,`sequence` FROM `proteins` WHERE `organism`='
    sql += "'" + organisms[i][0] + "'"
    cursor.execute(sql)
    proteinsA = cursor.fetchall()
    
    for j in range(i+1, l):
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
                '''INSERT INTO `protein_pairs`
                (proteinA, proteinB)
                VALUES
                (%s, %s)
                ''',
                [idA, idB]
            )

        