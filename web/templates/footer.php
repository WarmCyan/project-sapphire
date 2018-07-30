<?php
//***************************************************************************
//
//  File: footer.php
//  Date created: 07/29/2018
//  Date edited: 07/29/2018
//
//  Author: Nathan Martindale
//  Copyright © 2018 Digital Warrior Labs
//
//  Description: Functions to get end of an html page
//
//***************************************************************************

function getFooter()
{
	$html <<<HTML
		</div> <!-- /content -->
	</body>
</html>
HTML;

	echo($html);
}

?>
