import requests
from bs4 import BeautifulSoup
import re

def get_ncbi_page_text(url):
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) 'r'Chrome/45.0.2454.85 Safari/537.36 155Browser/6.0.3',
        'Referer': r'http://bj.fangjia.com/ershoufang/',
        'Host': r'www.ncbi.nlm.nih.gov',
        'Connection': 'keep-alive'
    }
    print('url getting :', url)
    url = r'%s' % url
    page = requests.get(url, headers=headers)
    print('url getting completed.')
    return page.text

# get rs id based on clinvar item.
def get_rs_id(clinvar_item):
    url_clinvar_item = clinvar_item.replace('>', '%3E').replace(' ', '%20') # Item in url differ from origin.
    url_clinvar_prefix = 'http://www.ncbi.nlm.nih.gov/clinvar/?term='
    url_clinvar = url_clinvar_prefix + url_clinvar_item
    page_text = get_ncbi_page_text(url_clinvar)
    soup = BeautifulSoup(page_text, 'lxml')
    tag_rs = soup.find(lambda tag: re.match('rs\d+',tag.text) and len(tag.attrs) == 1 )
    rs_id = tag_rs.text
    return rs_id

# get snp sequence based on rs id.
def get_snp_seq(rs_id):
    snp_id = rs_id[2:]
    url_snp_prefix = 'http://www.ncbi.nlm.nih.gov/snp/'
    url_snp = url_snp_prefix + snp_id
    page_text = get_ncbi_page_text(url_snp)
    soup_snp = BeautifulSoup(page_text, 'lxml')
    tag_snp = soup_snp.find('pre', {'class' : 'snp_flanks'})
    snp_seq = tag_snp.text
    return snp_seq.strip()

# use clinvar item to get its mrna sequence. uncomplete
'''
def get_clinvar_mrna_seq(clinvar_item):
    mrna_id = re.search('^N.*?\)', a).group(0)
    url_mrna_prefix = 'https://www.ncbi.nlm.nih.gov/nuccore/?term='
    url_mrna = url_mrna_prefix + mrna_id
    page_text = get_ncbi_page_text(url_mrna)
    soup = BeautifulSoup(page_text, 'lxml')
    soup.find(lambda tag: re.match('.*?\|.*?\|.*?\|.*?\|', tag.text), {'class': "brieflinkpopdesc"})
'''

# input whole sequence as fasta and short snp sequence as snp_seq, span indicate base number before or after.
def get_snp_context(fasta, snp_seq, span):
    snp_context_middle = re.search('\[.*?\]',snp_seq).group(0)
    snp_seq_beford = re.split('\[.*?\]', snp_seq)[0]
    snp_seq_after = re.split('\[.*?\]', snp_seq)[1]
    
    if re.findall('\w{%s}%s' % (span - len(snp_seq_beford), snp_seq_beford), fasta):
        snp_context_beford = re.findall('\w{%s}%s' % (span - len(snp_seq_beford), snp_seq_beford), fasta)[0]
    else:
        print('err beford')
        snp_context_beford = snp_seq_beford
        
    if re.findall('%s\w{%s}' % (snp_seq_after, span - len(snp_seq_after)), fasta):
        snp_context_after = re.findall(r'%s\w{%s}' % (snp_seq_after, span - len(snp_seq_after)), fasta)[0]
    else:
        snp_context_after = snp_seq_after
        
    snp_context = snp_context_beford + snp_context_middle + snp_context_after
    return snp_context

# read in fasta file based on clinvar item
def get_fasta_from_clinvar(clinvar_item):
    fasta_file_name = re.search('^N.*?\)', clinvar_item).group(0) + '.fasta'
    f_fasta = open(fasta_file_name, 'r')
    fasta = f_fasta.read().replace('\n', '')
    f_fasta.close()
    return fasta

# main part of this program.
if __name__ == '__main__':
    str_rs_snp = ''
    list_rs_snp = []
    list_rs_snp_context = ['SNP_ID	SEQUENCE\n']
    
    context_span = 250 # length before or after snp site

    # open clinvar items file and turn it to a list
    clinvar_items_file_name = 'clinvar_items.txt'
    f_clinvar_items = open(clinvar_items_file_name, 'r')
    list_clinvar_items = f_clinvar_items.readlines()
    f_clinvar_items.close()

    # analyse each clinvar_item and save each rs_snp record to a list (list_rs_snp).
    for clinvar_item in list_clinvar_items:
        clinvar_item = clinvar_item.strip()

        # get the list for first file clinva_rs_snp.txt
        rs_id = get_rs_id(clinvar_item)           
        snp_seq = get_snp_seq(rs_id)
        clinvar_rs_snp = clinvar_item + '\t' + rs_id + '\t' + snp_seq + '\n'
        list_rs_snp.append(clinvar_rs_snp)

        #get the list for the second file rs_snp_context.txt
        fasta = get_fasta_from_clinvar(clinvar_item)
        snp_context = get_snp_context(fasta, snp_seq, context_span)
        rs_snp_context = rs_id + '\t' + snp_context + '\n'
        list_rs_snp_context.append(rs_snp_context)

    # save list_rs_snp to a result file
    f_rs_snp = open('clinvar_rs_snp.txt', 'w')
    f_rs_snp.writelines(list_rs_snp)
    f_rs_snp.close()

    # save list_rs_snp_context to a result file
    f_rs_snp = open('rs_snp_context.txt', 'w')
    f_rs_snp.writelines(list_rs_snp_context)
    f_rs_snp.close()



