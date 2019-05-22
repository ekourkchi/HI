#!/usr/bin/python
import sys
import os
import subprocess
import math

import html_header as html



with open('html_tables/Alfalfa70.html', 'w+') as f:
  
  
  S =  html.title("Alfalfa 70%")
  f.write(S+"\n")
  
  S  = open("html_components/logo_menu_bar.html","rb").read()
  f.write(S+"\n")
  
  S  = open("html_components/second_menu_bar.html","rb").read()
  f.write(S+"\n")
  
  
  S  = open("html_components/side_bars.html","rb").read()
  f.write(S+"\n")
  
  
  S = """

 <h2 >This is the ALFALFA 70% sample and contains galaxies that we already have from ALFALFA 40% or otherwise. </h2>
 
 <ul>
   <li> Not earlier than Sa (where available)
   </li>
 </ul>
 
 <ul>
   <li> Inclinations more than 60 degrees (where information available)
   </li>
 </ul>
 
 <ul>
   <li> Linewidths less than 70 km/s (dwarfs or face on)
   </li>
 </ul>
 
 <ul>
   <li> S/N less than 5
   </li>
 </ul>
"""
  
  f.write(S+"\n")
  
  S  = open("html_db/alfalfa70_photometry.tbl.html","rb").read()
  f.write(S+"\n")
  

  S  = open("html_components/footer.html","rb").read()
  f.write(S+"\n")
