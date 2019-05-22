#!/usr/bin/python
import sys
import os
import subprocess
import math



def title(titre):

 title = """
<!DOCTYPE html PUBLIC "-/W3C/DTD XHTML 1.0 Strict/EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  


  <head>
    <title>
  """
  
 title += titre
 
 title += """
    </title>
        
    <link rel="stylesheet" href="css/trac.css" type="text/css" />
    <link rel="stylesheet" href="css/wiki.css" type="text/css" />
    <link rel="stylesheet" type="text/css" href="css/ps.css" />
    <link rel="icon" href="favicon/favicon.ico" type="image/x-icon">
        
    <script type="text/javascript" src="js/jquery.js"></script>
    <script type="text/javascript" src="js/trac.js"></script>
    <script type="text/javascript" src="js/search.js"></script>
    <script type="text/javascript" src="js/tracsectionedit.js"></script>
    <script type="text/javascript" src="js/esn2.js"></script>

    <script type="text/javascript">
      jQuery(document).ready(function($) {
        $("#content").find("h1,h2,h3,h4,h5,h6").addAnchor("Link to this section");
      });
    </script>
        
  </head>\n
  """
  
 return title
