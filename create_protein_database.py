import glob
import gzip
import MySQLdb
import progressbar
from Bio import SeqIO

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
print 'Clearing `proteins` table'
conn.query('DROP TABLE IF EXISTS `proteins`')
conn.commit()
sql = '''CREATE TABLE `proteins` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `organism` VARCHAR(32) NULL,
            `header` TEXT NULL,
            `sequence` TEXT NULL,
            PRIMARY KEY (`id`)
        )
        '''
conn.query(sql)
conn.commit()

# Get all the relevant fasta files
file_list = glob.glob('./bacteria_proteomes/*.fasta.gz')
# DNA fasta files are picked up by glob, but we don't want them
file_list = [f for f in file_list if not 'DNA.fasta' in f]
print 'Writing data to database...'
overall_bar = progressbar.ProgressBar(
    widgets=[progressbar.Bar(marker='#', left='[', right=']')],
    maxval = len(file_list),
).start()

count = 0
for f in file_list:
    # The identifier for each organism resides in the filename.
    # Here we strip the filename down to the identifier
    ident = f.replace('./bacteria_proteomes/','')
    ident = ident.split('_')[0]
    records = []
    with gzip.open(f, 'rt') as handle:
        for seq_record in SeqIO.parse(handle, 'fasta'):
            records.append((ident, seq_record.id, seq_record.seq))

        # It's faster to insert everything at once    
        cursor.executemany('''INSERT INTO `proteins` 
                (`organism`, `header`, `sequence`) 
                VALUES
                (%s, %s, %s)
                ''',
                records
        )
        conn.commit()
    count += 1
    overall_bar.update(count)
overall_bar.finish()
print 'All done!'