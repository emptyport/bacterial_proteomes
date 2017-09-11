import MySQLdb

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

        