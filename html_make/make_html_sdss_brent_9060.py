#!/usr/bin/python
import sys
import os
import subprocess
import math

import html_header as html



with open('html_tables/sdss_brent_9060.html', 'w+') as f:
  
  
  S =  html.title("All - Brent (9060)")
  f.write(S+"\n")
  
  S  = open("html_components/logo_menu_bar.html","rb").read()
  f.write(S+"\n")
  
  S  = open("html_components/second_menu_bar.html","rb").read()
  f.write(S+"\n")
  
  
  S  = open("html_components/side_bars.html","rb").read()
  f.write(S+"\n")
  
  
  S = """

 <h2 id="all.brent.9060">Only galaxies with SDSS imaging data ... (Taken from Brent's 9060 catalog)</h2>
 
 <ul>
   <li> Good HI profiles
   </li>
 </ul>
 
 <ul>
   <li> Types Sa and later
   </li>
 </ul>
 
 <ul>
   <li> Inclinations greater than 45 degrees from face on, i.e. b/a > 1/sqrt(2)
   </li>
 </ul>

"""
  
  f.write(S+"\n")
  
  S  = open("html_db/sdss_brent_9060.tbl.html","rb").read()
  f.write(S+"\n")
  

  S  = open("html_components/footer.html","rb").read()
  f.write(S+"\n")
