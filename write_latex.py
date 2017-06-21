import re
import sys
sys.path.append('/home/oriol/Documentos/pyMESA')
import pyMESAutils as pym
import numpy as np

fnova=open('reaction_net_list_nova_ext.txt','r')
fcno=open('reaction_net_list_cno_plus_extras.txt','r')
fppcno=open('reaction_net_list_pp_and_cno.txt')
fmod=open('reaction_net_list_nova_modified.txt','r')
fjj=open('reaction_net_list_jj_isos.txt','r')
fhb=open('reaction_net_list_h_burn.txt','r')

novaout=open('rates_nova.tex','w')
cnoout=open('rates_cno.tex','w')
ppcnoout=open('rates_ppcno.tex','w')
modout=open('rates_mod.tex','w')
jjout=open('rates_jj_isos.tex','w')
hbout=open('rates_h_burn.tex','w')

pat=re.compile(r'\s*[0-9.\-]+\s+([^\s]+)(\s+weaklib\s+|[^a-z]+)[a-z0-9_]+\s+([a-z0-9]?.*)\s*$',re.IGNORECASE)
pat2=re.compile(r'(.+)\s+$',re.IGNORECASE)
isopat = re.compile(r'(([a-z]{1,3})([0-9]{1,3})|neut)',re.IGNORECASE)
reacpat1=re.compile(r'_([agpn]{2})_',re.IGNORECASE)
reacpat2=re.compile(r'\(([aegnpu\+\-]+),?([aegnpu\+\-]*)\)',re.IGNORECASE)

def make_isos_latex(tup):
    actual=tup[0]
    if actual=='neut':
        latex='n'
        sortstring='00000'
    elif pym.checkElement(tup[1]):
        el=tup[1]
        amass=tup[2]
        latex=r'\ce{^{%s}%s}' %(amass, el.title())
        sortstring='%02d%s' %(int(amass), el)
    else:
        latex=None
        actual=None
        sortstring=''
    return actual,latex,sortstring

def make_reacs_latex(s):
    if s=='a':
        s=r'$\alpha$'
    if s=='g':
        s=r'$\gamma$'
    if s=='n':
        s=r'n'
    if s=='e-':
        s=r'$\beta^+$'
    if s=='e+':
        s=r'$\beta^-$'
    if s=='nu':
        s=r'$\nu$'
    if s=='e+nu':
        s=r'$\beta^+\nu$'
    if s=='e-nu':
        s=r'$\beta^-\nu$'    
    return s

def make_latex_style(text):
    isos=isopat.findall(text)
    if text[:2]=='r_':
        text=text[2:]
        reac=reacpat1.findall(text)
        for pair in reac:
            text=text.replace('_%s_'%(pair), '(%s,%s)' %(make_reacs_latex(pair[0]), 
                              make_reacs_latex(pair[1])))
    else:
        reacs=reacpat2.findall(text)
        for reac in reacs:
            try:
                text=text.replace('(%s'%reac[0],'(%s'%make_reacs_latex(reac[0]))
            except AttributeError:
                pass
            try:
                text=text.replace('%s)'%reac[1],'%s)'%make_reacs_latex(reac[1]))
            except AttributeError:
                pass
    sort=''
    for iso in isos:
        actual,latex,sortstring=make_isos_latex(iso)
        text=text.replace(actual,latex)
        sort+=sortstring
    text=text.replace('_wk-minus_',r'($\beta^-$,$\nu$)')
    text=text.replace('_wk_',r'($\beta^+$,$\nu$)')
    text=text.replace('_',' ')
    return text,sort

def extract_rates(infile, ftex, label, caption=None, longtable=True, columns=3):
    #extracts rates from the information mesa prints at start of run
    rates=[]
    coltext='|'+''.join(['c|' for num in range(columns)])
    if caption==None:
        caption=label
    for line in infile:
        n=pat.match(line)
        try:
            result=n.groups(1)
            if result[-1]=='':
                text=result[0]
            else:
                text=result[-1]
            for i in xrange(100):
                m=pat2.match(text)
                if m:
                    text=m.groups(1)[0]
                else:
                    break
            rates.append(text)
        except AttributeError:
            pass 
    
    colnum=1
    if longtable:
        ftex.write('\\begin{longtable}{ %s }\n\hline\n' %(coltext))
    else:
        ftex.write('\\begin{table}[!htb]\n  \\begin{center}\n  \\begin{tabular}{ %s }\n\hline\n' %(coltext))
    sorter=range(len(rates))
    for num,text in enumerate(rates):
        text,sorter[num]=make_latex_style(text)
        rates[num]=text
    ind=np.argsort(sorter)
    nicerates=np.array(rates)[ind]
    for text in nicerates:
        if colnum==columns:
            colnum=0
            ftex.write(r''.join([text, r' \\','\n']))
        else:
            ftex.write(''.join([text, ' & ']))
        colnum+=1
    if longtable:
        ftex.write('\n  \caption{%s}\n  \label{tab:%s}  \n\end{longtable}\n' %(caption, label))
    else:
        ftex.write('\n  \end{tabular}\n  \caption{%s}\n  \label{tab:%s}\n  \end{center}\
                    \n\end{table}\n' %(caption, label))
    return

#extract_rates(fnova, novaout, 'nova', columns=3, caption=r'List of reactions considered in \texttt{nova\_ext.net}')
#extract_rates(fcno, cnoout, 'cno', columns=2, caption=r'List of reactions considered in \texttt{cno\_extras\_o18\_to\_mg26\_plus\_fe56.net}')
#extract_rates(fppcno, ppcnoout, 'ppcno', columns=2, caption=r'List of reactions considered in \texttt{pp\_cno\_extras\_o18\_ne22.net}')
#extract_rates(fmod, modout, label='novamod', columns=3, caption=r'nova modified')
extract_rates(fjj, jjout, 'jjisos', columns=3, caption=r'List of reactions considered automatically by \texttt{MESA} when using the isotopes used by Jordi Jos\'e in his thesis')
#extract_rates(fhb, hbout, 'hburn', columns=3, caption=r'List of reactions considered in \texttt{h\_burn.net}')
