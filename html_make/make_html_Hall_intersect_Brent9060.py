#!/usr/bin/python
import sys
import os
import subprocess
import math

import html_header as html



with open('html_tables/Hall_intersect_Brent9060.html', 'w+') as f:
  
  
  S =  html.title("Hall2012 - Brent (9060)")
  f.write(S+"\n")
  
  S  = open("html_components/logo_menu_bar.html","rb").read()
  f.write(S+"\n")
  
  S  = open("html_components/second_menu_bar.html","rb").read()
  f.write(S+"\n")
  
  
  S  = open("html_components/side_bars.html","rb").read()
  f.write(S+"\n")
  
  
  S = """

 
 <h2 id="Halletal.2012SDSSCatalog-CrossedwithBrent.9060">Hall et al. 2012 (SDSS Catalog) - Crossed with Brent.9060</h2>
 
 <p> SDSS Imaging Data: M. Hall et al. 2012, MNRAS,425,2741 
   <a class="ext-link" href="http://adsabs.harvard.edu/abs/2012MNRAS.425.2741H"><span class="icon">http://adsabs.harvard.edu/abs/2012MNRAS.425.2741H</span>
   </a>
 </p>
"""
  
  f.write(S+"\n")
  
  S  = open("html_db/Hall_intersect_Brent9060.tbl.html","rb").read()
  f.write(S+"\n")
  

  S  = open("html_components/footer.html","rb").read()
  f.write(S+"\n")
