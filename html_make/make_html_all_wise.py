#!/usr/bin/python
import sys
import os
import subprocess
import math

import html_header as html



with open('html_tables/all_wise.html', 'w+') as f:
  
  
  S =  html.title("WISE Photometry")
  f.write(S+"\n")
  
  S  = open("html_components/logo_menu_bar.html","rb").read()
  f.write(S+"\n")
  
  S  = open("html_components/second_menu_bar.html","rb").read()
  f.write(S+"\n")
  
  
  S  = open("html_components/side_bars.html","rb").read()
  f.write(S+"\n")
  
  
  S = """

 <h2 id="all.brent.9060">Wise Photometry ... </h2>
 
 
 <p> Galaxies in \'WISE Photometry\' catalog ...
   <a class="ext-link" href="http://edd.ifa.hawaii.edu/dfirst.php"><span class="icon">http://edd.ifa.hawaii.edu/dfirst.php</span>
   </a>
 </p>

"""
  
  f.write(S+"\n")
  
  S  = open("html_db/wise_photometry.tbl.html","rb").read()
  f.write(S+"\n")
  

  S  = open("html_components/footer.html","rb").read()
  f.write(S+"\n")
