# clinvar_to_sr_snp
=====================================================
##实现功能：  
  根据给的**clinvar item**名（eg: *NM_000484.3(APP):c.2150T>G (p.Val717Gly)* ) 获取对应的*rs*号（ eg: *rs63749964* )和对应的snp序列（eg: *GGTGTTGTCATAGCGACAGTGATCG[G/T]CATCACCTTGGTGATGCTGAAGAAG* ). 序列的长度可以通过调整程序中 context_span 的值来调整，默认是250（snp位点前后分别250个碱基）. 

###　　　　　　　　　　　　Author: 漂浮水域
###　　　　　　　　　 E-mail: qiyanghong2020@gmail.com

=======
  **输入文件**：  
  1、clinvar_items.txt *把clinvar item的名字保存在里面， 每行一条*  
  2、\*.fasta *手动下载各个clinvar位点所在的序列, 用于后续snp前后序列查找*  
  **输出文件**：  
  1、clinvar_rs_snp.txt *保存clinvar名，rs号，短snp序列。*  
  *（eg:NM_000484.3(APP):c.2150T>G(p.Val717Gly)->rs63749964->GGTGTTGTCATAGCGACAGTGATCG[G/T]CATCACCTTGGTGATGCTGAAGAAG )*  
  2、rs_snp_context.txt *保存rs号， 长的snp序列。序列长度默认前后各250个碱基。*
