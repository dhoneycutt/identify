<?php
   $json = $_POST['json'];

   /* sanity check */
   if (json_decode($json) != null)
   {
     $decode = json_decode($json);
     $id = $decode->id;
     $filename = "json/" . $id . ".json";
     $file = fopen($filename,'w+');
     fwrite($file, $json);
     fclose($file);
   }
   else
   {
     // user has posted invalid JSON, handle the error 
   }

?>
