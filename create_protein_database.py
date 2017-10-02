import glob
import MySQLdb
import progressbar
from Bio import SeqIO

branches = [
    'archea',
    'bacteria',
    'fungi',
    'metazoa',
    'plants',
    'protozoa',
    'viridae'
]

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
            `geneid` VARCHAR(32) NULL,
            `sequence` TEXT NULL,
            PRIMARY KEY (`id`)
        )
        '''
conn.query(sql)
conn.commit()

sql = '''CREATE INDEX idx_geneid
         ON `proteins` (geneid)'''
conn.query(sql)
conn.commit()

print 'Writing data to database...'
for b in branches:
    print 'Processing',b
    fasta_path = b+'/Rawdata/'
    file_list = glob.glob(fasta_path+'*')
    bar = progressbar.ProgressBar(
        widgets=[
            progressbar.Bar(marker='#', left='[', right=']'),
            progressbar.ETA()
            ],
        maxval = len(file_list),
    ).start()

    count = 0
    for f in file_list:
        # The identifier for each organism resides in the filename.
        # Here we strip the filename down to the identifier
        ident = f.replace(fasta_path,'')
        ident = ident.split('.')[0]
        records = []
        with open(f, 'rt') as handle:
            for seq_record in SeqIO.parse(handle, 'fasta'):
                records.append((ident, seq_record.id, seq_record.seq))

                if len(records) > 10000:
                    # It's faster to insert everything at once, 
                    # but for larger files we need to batch things
                    cursor.executemany('''INSERT INTO `proteins` 
                        (`organism`, `geneid`, `sequence`) 
                        VALUES
                        (%s, %s, %s)
                        ''',
                        records
                    )
                    conn.commit()
                    records = []

            cursor.executemany('''INSERT INTO `proteins` 
                (`organism`, `geneid`, `sequence`) 
                VALUES
                (%s, %s, %s)
                ''',
                records
            )
            conn.commit()
            records = []
        count += 1
        bar.update(count)
    bar.finish()
print 'All done!'