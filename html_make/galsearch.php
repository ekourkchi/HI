<?php


if (isset($_POST["pgc"])){
    $pgc=$_POST['pgc'];
    $galname="PGC".$pgc;
}

if (isset($_POST["ra"])){
    $ra=$_POST['ra'];
}

if (isset($_POST["dec"])){
    $dec=$_POST['dec'];
}

if (isset($_POST["fov"])){
    $fov=$_POST['fov'];
}

if (isset($_POST["fovUnit"])){
    $fovUnit=$_POST['fovUnit'];
}

if (isset($_POST["galname"])){
    
    $galname = $_POST["galname"];
    	function get_url_contents($url){
		$crl = curl_init();
		$timeout = 5;
		curl_setopt ($crl, CURLOPT_URL,$url);
		curl_setopt ($crl, CURLOPT_RETURNTRANSFER, 1);
		curl_setopt ($crl, CURLOPT_CONNECTTIMEOUT, $timeout);
		$ret = curl_exec($crl);
		curl_close($crl);
		return $ret;
		}
    

		if($galname == ""){
                    $nogal = 1;
		}else{
        
        
		// NED Lookup for PGC Number (Even if PGC is entered, so any format acceptable)
		$lookup_url = "http://ned.ipac.caltech.edu/cgi-bin/nph-objsearch?objname=".urlencode($galname)."&extend=no&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=RA+or+Longitude&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES";
		$toparse = get_url_contents($lookup_url);
		//echo $toparse;
		$toparse2 = $toparse;
		$toparse = split("<A HREF=\"/cgi-bin/catdef\?prefix=PGC\" target=help>PGC</A> ", $toparse);
		//echo count($toparse);
		if(count($toparse) == 1){
		$toparse2 = split("<A HREF=\"/cgi-bin/catdef\?prefix=LEDA\" target=help>LEDA</A> ", $toparse2);
		}
		if(count($toparse) == 1){
                        $noNED = 1;
			$pgc = filter_var($galname, FILTER_SANITIZE_NUMBER_INT);   // extract the number 
			$pgc = abs($pgc);

		}
                
		$toparse = split(" ", $toparse[1]);
		
		if (!isset($pgc)){
		$pgc = $toparse[0];
		$pgc = filter_var($pgc, FILTER_SANITIZE_NUMBER_INT);   // extract the number 
		$pgc = abs($pgc);
		
		
		} }       
        
    
}


    





?>   



<html>
  <head>
  
  <meta http-equiv="Content-Language" content="en-us"/>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1252"/>
    <title>Galaxy Search</title>
    <script type="text/javascript" src="js/esn2.js"></script>
    <link rel="stylesheet" href="css/wiki.css" type="text/css" />
<!--       <link href="http://aladin.u-strasbg.fr/AladinLite/doc/css/bootstrap.min.css" rel="stylesheet"> -->
<style>
table, th, td {
	border: 2px solid gray;
	border-collapse: collapse;
}
th, td {
	padding: 5px;
	text-align: center
}
th { 
	background-color: #FFDFB6;
}

table#t00, th#t00, td#t00 {

    border: 0px;
    border-collapse: collapse;
    text-align: center;
    border-spacing: 5px;
    margin-left: auto;
    margin-right: auto;
}

table#t01 {

    border: 2px solid black;
    border-collapse: collapse;
    border-spacing: 5px;

}

table#t02, th#t02, td#t02 {

    border: 0px;
    border-collapse: collapse;
    text-align: left;
    border-spacing: 5px;
    margin-left: auto;
    margin-right: auto;
}


</style>    
    
<link rel="stylesheet" type="text/css" href="buttons/buttons.css" />
    
    
  </head>
<body>     

    <link rel="stylesheet" href="css/trac.css" type="text/css" />
    <link rel="stylesheet" type="text/css" href="css/ps.css" />
    <link rel="icon" href="favicon/favicon.ico" type="image/x-icon">
        
    <script type="text/javascript" src="js/jquery.js"></script>
    <script type="text/javascript" src="js/trac.js"></script>
    <script type="text/javascript" src="js/search.js"></script>
    <script type="text/javascript" src="js/tracsectionedit.js"></script>

    <script type="text/javascript">
      jQuery(document).ready(function($) {
        $("#content").find("h1,h2,h3,h4,h5,h6").addAnchor("Link to this section");
      });
    </script>
    
    

<script type="text/javascript" src="http://code.jquery.com/jquery-1.9.1.min.js" charset="utf-8"></script>
<script type="text/javascript" src="http://aladin.u-strasbg.fr/AladinLite/api/v2/latest/aladin.min.js" 
charset="utf-8"></script>
<div class="hexp">
<table style="margin-top:12px;border-collapse:collapse"><tr>

</div>
<link rel="stylesheet" href="http://aladin.u-strasbg.fr/AladinLite/api/v2/latest/aladin.min.css" />
</div><!-- ahexp -->
</div><!-- cozd -->
     
     

        

<div id="toplevel">


  <div id="banner">

 <a href="http://www.ifa.hawaii.edu/~ehsan/">
 <img src="logo/e_kourkchi.logo.png" height="75" /></a><h1>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; E h s a n &nbsp; &nbsp; &nbsp;  K o u r k c h i </h1>

         <a>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</a>
         <a href="http://www.ehsanoid.com/" class="button blue medium">Home Page</a>
         <a href="http://www.ehsanoid.com/cv.html" class="button orange medium">CV</a>
         <a href="http://www.ehsanoid.com/publications.html" class="button green medium">Publications</a>

  </div> 
                
                
  <div id="metanav" class="nav">
  <ul> </ul>
  </div>
                
</div>     
                

<div id="mainnav" class="nav">
    <ul>
      <li class="first active"><a href="javascript:history.back()">Go back</a></li>
      <li><a   target="_blank"  href="http://www.ehsanoid.com/">Ehsan's Home</a></li>
    </ul>
</div>           
       
       

<div id="main">
  <div id="ctxtnav" class="nav">
    <h2>Context Navigation</h2>
    
     <ul>
        <li class="first "><a href="http://ifa.hawaii.edu/users/ehsan/">Home</a></li>
        <li class="first "><a href="http://ifa.hawaii.edu/users/ehsan/html_tables/Hall_intersect_Brent9060.html">Tables</a></li>
        <li class="first "><a href="http://ifa.hawaii.edu/users/ehsan/galsearch.php">Search</a></li>
     </ul>
     

     
    <hr />
</div>
    


<div id="content-side">



<!--         Side bar

-->

<span>About me</span>
 <ul>
 

          <li>
             <a   target="_blank"  href="http://www.ehsanoid.com/">Ehsan's Homepage</a>
          </li>
          
          <li>
             <a   target="_blank"  href="http://www.ehsanoid.com/cv.html">CV</a>
          </li>          
          
                    
          <li>
             <a   target="_blank"  href="http://www.ehsanoid.com/publications.html">Publications</a>
          </li>    
          
          <li>
             <a   target="_blank"  href="http://www.ehsanoid.com/contact.html">Contact</a>
          </li>    
          

                     
          
</ul>


<span>Projects</span>
 <ul>
          
          
          <li>
             <a   target="edd_home_blank"  href="http://www.ifa.hawaii.edu/~ehsan/html_tables/Hall_intersect_Brent9060.html">Galaxy Tables</a>
          </li>          
          
          <li>
             <a   target="edd_home_blank"  href="http://edd.ifa.hawaii.edu/index.html">EDD Home Page</a>
          </li>
          
          
   


</ul>  
        

<span>Wiki Notes</span>
 <ul>
          
          
          <li>
             <a   target="edd_home_blank"  href="http://svn.pan-starrs.ifa.hawaii.edu/trac/ipp/wiki/Challenger">Challenger</a>
          </li>          
          

          
          <li>
             <a   target="edd_home_blank"  href="http://svn.pan-starrs.ifa.hawaii.edu/trac/ipp/wiki/glga_manual">GLGA Manual</a>
          </li>          

        <li>
            <a   target="_blank"  href="http://svn.pan-starrs.ifa.hawaii.edu/trac/ipp/">IPP Main Page</a>
        </li>
</ul>  



</div>

<!--         Side bar - END


-->  


<?php


// 
if (isset($pgc)){


//     $command = escapeshellcmd('/usr/bin/python python/query_pgc.py 2>&1');
//     passthru($command);
//     $res = ob_get_clean(); 
//     
    
    $output = `python python/query_pgc.py $pgc 2>&1`;
//     echo "<pre>$output</pre>";
    
    
    $row = explode(" ", $output);


$n = 0;
$items = array();
foreach($row as $value){
  $items[$n] = $value;
  $n++;
}    

$objname = $items[1];
$type = $items[9];
$ra = number_format(15*$items[3],4);
$dec = number_format($items[4],4);

$l2 = number_format($items[5],4);
$b2 = number_format($items[6],4);

$sgl = number_format($items[7],4);
$sgb = number_format($items[8],4);

$d25 = number_format(0.1*pow(10,$items[10]),2);
$fov = 1.8*$d25;
$fovUnit == 'arcmin';
$size = $fov/60.;  
    
}  // if



// $command = escapeshellcmd("/usr/bin/python python/sdss_query.py $ra $dec");
// system($command, $hasSDSS);
    $output = `/usr/bin/python python/sdss_query.py $ra $dec 2>&1`;
//    echo "<pre>$output</pre>";

$hasSDSS = $output;

if ($hasSDSS == 1){   // if it has SDSS coverage
    $survey = "P/SDSS9/color";
    }
else{
    $survey = "P/DSS2/color";
    }






echo <<<END

<table id="t01"><tr><td>
<table id="t02">



<tr id="t00"><td id="t00">



<table id="t00">
<tr id="t00"><td id="t00">




<table id="t00">
<tr id="t00"><td align="right" id="t00"><form method="post" action="galsearch.php">PGC Number</td>
END;

if (isset($pgc)){
    echo "<td id=\"t00\" valign=\"baseline\"><input id=\"pgc\" type=\"number\" name=\"pgc\" value=$pgc /></td>"; }
    else {
        echo "<td id=\"t00\" valign=\"baseline\"><input id=\"pgc\" type=\"number\" name=\"pgc\"></td>"; }
    
    



echo <<<END

    <td id="t00" valign="baseline"><input type="submit" value="Display" /></td>
    <td id="t00" valign="baseline"><input type="button" value="Clear"  onclick="ClearFields1()"></form></td>
</tr>     
</table>

</td></tr>




<tr id="t00"><td id="t00">




<table id="t02">
<tr id="t00"><td align="right" id="t00"><form method="post" action="galsearch.php">Galaxy Name</td>
END;

if (isset($pgc)){
    echo "<td id=\"t00\" valign=\"baseline\"><input id=\"galname\" type=\"text\" name=\"galname\" value=$galname /></td>"; }
    else {
        echo "<td id=\"t00\" valign=\"baseline\"><input id=\"galname\" type=\"text\" name=\"galname\"></td>"; }





echo <<<END

    <td id="t00" valign="baseline"><input type="submit" value="Display" /></td>
    <td id="t00" valign="baseline"><input type="button" value="Clear"  onclick="ClearFields15()"></form></td>
</tr>
</table>
</td></tr>
END;

if (isset($noNED)){
echo "<tr id=\"t00\"><td id=\"t00\" valign=\"baseline\"><p><mark>No Corresponding PGC Number Found in NED for <b>".$galname."</b> ! </mark></p></td></tr>";}

if (isset($nogal)){
echo "<tr id=\"t00\"><td id=\"t00\" valign=\"baseline\"><p><mark> Please enter a galaxy ! </mark></p></td></tr>";} 

echo <<<END












<tr><td id="t02">





<form method="post" action="galsearch.php">

     <div class="control-group">
        <label class="control-label" for="ra">R.A.</label>
          <div class="controls">
END;


            if (isset($ra)){
                echo "<input id=\"ra\"  type=\"text\" name=\"ra\" value=$ra> deg"; }
            else {
                echo "<input id=\"ra\"  type=\"text\" name=\"ra\"> deg"; }
            
            
echo <<<END
      <div class="control-group">
        <label class="control-label" for="dec">Dec.</label>
          <div class="controls">           
END;

            if (isset($dec)){
                echo "<input id=\"dec\" type=\"text\" name=\"dec\" value=$dec> deg"; }
            else {
                echo "<input id=\"dec\" type=\"text\" name=\"dec\"> deg"; }
            
 echo <<<END
        <div class="control-group">
        <label class="control-label" for="zoom">FoV</label>
          <div class="controls">           
            
END;

            if (isset($fov)){
                echo "<input id=\"fov\" type=\"text\" name=\"fov\" value=$fov>"; }
            else {
                echo "<input id=\"fov\" type=\"text\" name=\"fov\">"; }
            
 
 
echo '<select name="fovUnit">';

if (isset($fovUnit)){
    if  ($fovUnit == 'arcmin') { $size = $fov/60.;
      echo '<option value="arcmin">arcmin</option>';
      echo '<option value="arcsec">arcsec</option>';
      echo '<option value="degree">degree</option>';
      }
    elseif  ($fovUnit == 'arcsec') { $size = $fov/3600.;
      echo '<option value="arcsec">arcsec</option>';
      echo '<option value="arcmin">arcmin</option>';
      echo '<option value="degree">degree</option>';}
    elseif  ($fovUnit == 'degree') { $size = $fov;
      echo '<option value="degree">degree</option>';
      echo '<option value="arcmin">arcmin</option>';
      echo '<option value="arcsec">arcsec</option>';
      } 
}else{
    echo '<option value="arcmin">arcmin</option>';
    echo '<option value="arcsec">arcsec</option>';
    echo '<option value="degree">degree</option>';
    }

 
 
            
 echo <<<END

                </select>
          </div>
      </div>   
      
      <div class="control-group">
      <div class="controls">
      <input type="submit" value="Display">
      <input type="button" value="Clear" onclick="ClearFields2()">
      </div></div> 


    </form>

</td></tr>
</table>

</td>

<td id="t00">


<div id="aladin1" style="width:500px;height:500px;"><div 
class="spinner" style="position:relative;top:85px;left:85px"></div></div>
<script type="text/javascript">
END;


if (isset($ra)){
echo "var aladin = A.aladin('#aladin1', {survey: \"$survey\", showGotoControl: false, target:\"$ra $dec\", fov:$size});";
} else {
    echo "var aladin = A.aladin('#aladin1', {survey: \"P/SDSS9/color\", showGotoControl: false, target:\"0 0\", fov:180});";

    }


 echo <<<END
</script>

<table id="t02"><tr id="t02"><td id="t02">
<br><small>You might try to zoom in and out using your mouse wheel, or pan the view to move around.</small>
<br><small>To change the survey layout, click on the tools on top left.</small>
</td></tr></table>

</td><td id="t00">            
END;



  
            





print "<table id=\"t00\"><tr id=\"t00\"><td id=\"t00\">";
print "<table id=\"t00\"><tr id=\"t00\"><td id=\"t00\">";

////////////////////////////////////////////
print '<table>';

if (isset($pgc)){
print '<tr><th>pgc</th>';
print "<td>$pgc</td></tr>";
print '<tr><th>objname</th>';
print "<td>$objname</td></tr>";

print '<tr><th>type</th>';
print "<td>$type</td></tr>";

print '<tr><th>d25 (arcmin)</th>';
print "<td>$d25</td></tr>";


print '<tr><th>R.A. (deg)</th>';
print "<td>$ra</td></tr>";
print '<tr><th>Dec. (deg)</th>';
print "<td>$dec</td></tr>";

print '<tr><th>GL (deg)</th>';
print "<td>$l2</td></tr>";
print '<tr><th>GB (deg)</th>';
print "<td>$b2</td></tr>";


print '<tr><th>SGL (deg)</th>';
print "<td>$sgl</td></tr>";
print '<tr><th>SGB (deg)</th>';
print "<td>$sgb</td></tr>";
} else {

$ra = number_format($ra,4);
$dec = number_format($dec,4);

print '<tr><th>R.A. (deg)</th>';
print "<td>$ra</td></tr>";
print '<tr><th>Dec. (deg)</th>';
print "<td>$dec</td></tr>";    
    
    
    }





print '</table>';
////////////////////////////////////////////
print "</td></tr><tr id=\"t00\"><td id=\"t00\">";
////////////////////////////////////////////
print '<table>';



print "<tr><td bgcolor=\"#F3D7BB\" align=\"center\"> <button onclick=\"ned($ra,$dec)\">NED</button></td></tr>";

if (isset($pgc)){
 print "<tr><td bgcolor=\"#E4BA90\" align=\"center\"> <button onclick=\"leda($pgc)\">LEDA</button></td></tr>";}

if ($hasSDSS == 1){
print "<tr><td bgcolor=\"#F3D7BB\" align=\"center\"> <button onclick=\"sdss($ra,$dec,$fov)\">SDSS</button> </td></tr>";}

if ($dec > -30){
print "<tr><td bgcolor=\"#E4BA90\" align=\"center\"> <button onclick=\"pstar($ra,$dec,$size)\">PanSTARRS-1</button> </td></tr>";}

print "<tr><td bgcolor=\"#F3D7BB\" align=\"center\"> <button onclick=\"irsa($ra,$dec,$fov)\">IRSA</button> </td></tr>";

print "<td bgcolor=\"#E4BA90\" align=\"center\"> <button onclick=\"HI_profile($items[0])\">HI Profile</button></td></tr>";

print "<td bgcolor=\"#F3D7BB\" align=\"center\"> <button onclick=\"cf2($items[0])\">Cosmicflows-2</button></td></tr>";

print "<td bgcolor=\"#E4BA90\" align=\"center\"> <button onclick=\"cf4_sdss($items[0])\">Cf4-SDSS</button></td></tr>";



print '</table>';
////////////////////////////////////////////
print '</td></tr></table>';
print '</td></tr></table>';
print '</td></tr>';

print "<tr id=\"t00\"><td id=\"t00\">";

// print "<table id=\"t00\">";
// print "<tr id=\"t00\"><td id=\"t00\" align=\"right\"><form method=\"get\" action=\"get_sdss_cf4.php\">PGC Number:</td>";
// echo "<td id=\"t00\" valign=\"baseline\"><input type=\"number\" name=\"pgc\" value=$pgc /></td>";
// print "<td id=\"t00\" valign=\"baseline\"><input type=\"submit\" value=\"Display\" /></td>";
// print '</tr></table>';


print '</td></tr>';
print '</table>';
print '</td></tr></table>';
print '<hr class="frsep"/>';
echo '<br> <br>';
////////////////////////////////////////////
?>


<script type="text/javascript">

function ClearFields1() {
     document.getElementById("pgc").value = "";
}


function ClearFields15() {
     document.getElementById("galname").value = "";
}


function ClearFields2() {

     document.getElementById("ra").value = "";
     document.getElementById("dec").value = "";
     document.getElementById("fov").value = "";
}

</script>


<!--  Footer -->
 <div id="footer" lang="en" xml:lang="en">
   <hr />
   <a id="tracpowered" href="http://trac.edgewall.org/"><img src="logo/trac_logo_mini.png" height="30" width="107" alt="Trac Powered" /></a>
   <p class="left"> &copy; copyright 2017 Ehsan Kourkchi</p>
   
   <br />
   
   <p class="left">
    Template taken from <a href="http://www.edgewall.org/"><strong>Edgewall Software</strong></a>
   <br />
   </p>
   
   <p class="right">Visit the Trac open source project at<br /><a href="http://trac.edgewall.org/">http://trac.edgewall.org/</a></p>

 </div>  
<!--  END - Footer -->


        </body>
</html>





