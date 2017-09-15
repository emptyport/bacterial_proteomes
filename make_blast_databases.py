import os
import glob
import subprocess
import progressbar
import MySQLdb

FNULL = open(os.devnull, 'w')
if not os.path.exists('./blast_db'):
    os.makedirs('./blast_db')

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

print 'Getting list of organisms...'
sql = 'SELECT * FROM `organisms`'
cursor.execute(sql)
organisms = cursor.fetchall()
l = len(organisms)

print 'Creating BLAST databases...'
count = 1

bar = progressbar.ProgressBar(
    widgets=[progressbar.Bar(marker='#', left='[', right=']'),
             progressbar.ETA()],
    maxval = len(organisms),
).start()

for organism in organisms:
    # search_pattern = './bacteria_proteomes/' + organism[0] + '*.fasta.gz'
    # fasta_files = glob.glob(search_pattern)
    # fasta_files = [f for f in fasta_files if not 'DNA.fasta' in f]
    # f = fasta_files[0]
    # path_to_fasta = os.path.dirname(os.path.realpath(__file__))
    # file_and_path = path_to_fasta + f[1:]
    
    sql = 'SELECT `id`,`sequence` FROM `proteins` WHERE `organism`='
    sql += "'" + organism[0] + "'"
    cursor.execute(sql)
    proteins = cursor.fetchall()
    outfile = open('temp.fasta', 'w')
    for protein in proteins:
        id = protein[0]
        seq = protein[1]
        outfile.write('>')
        outfile.write(str(id))
        outfile.write('\n')
        outfile.write(seq)
        outfile.write('\n\n')

    outfile.close()

    curPath = os.path.dirname(os.path.realpath(__file__))
    db_out = curPath + '/blast_db/' + organism[0]
    fasta_in = curPath + '/temp.fasta'

    cmd = "makeblastdb -dbtype 'prot' -in %s -title %s -out %s" % (fasta_in, organism[0], db_out)

    subprocess.call(cmd, shell=True, stdout=FNULL)
    count += 1
    bar.update(count)
