## Data Model Check

A [service](https://smartdatamodels.org/index.php/data-models-contribution-api/) that checks whether a datamodel is valid in terms of necessary files existence, directory structures, whether schema.json is valid, whether examples are valid, whether extra files, such as notes.yaml, Contributors.yaml, are valid and with messages in return by given the repository link to the datamodel.

[Pysmartdatamodel](https://pypi.org/project/pysmartdatamodels/) shared the schema json check.

### File related

- PHP snippet on WordPress

```php
<?php
echo "
<script type=\"text/javascript\">    
    // Get the query parameters from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const datamodelRepoUrl = encodeURIComponent(urlParams.get('datamodelRepoUrl'));
    const email = urlParams.get('email');
    const testnumber = urlParams.get('testnumber');

    // Call the check_schema function and display the output
    function check_schema(datamodelRepoUrl, email, testnumber) {

  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open(\"GET\", \"https://smartdatamodels.org/extra/check_datamodel_test.php?datamodelRepoUrl=\" + datamodelRepoUrl + \"&email=\" + email + \"&testnumber=\" + testnumber, true);
  xmlhttp.send();

  xmlhttp.onload = function() {
    if (xmlhttp.status === 200) {
      document.getElementById(\"output\").innerHTML = xmlhttp.responseText;
      if (xmlhttp.responseText.includes(\"#########\")) {
        endInterval();
      }
    }
  };
}

  if (datamodelRepoUrl && email && testnumber) {
        check_schema(datamodelRepoUrl, email, testnumber);

        // Periodically update the PHP program every 2 seconds
        myTimer = setInterval(function() {
          check_schema(datamodelRepoUrl, email, testnumber);
        }, 2000);
    }

function endInterval() {
  clearInterval(myTimer);
}

</script>";
?>
```
- check_datamodel_test.php: the program to call the master_tests.py, under the folder `/var/www/html/extra`

- clean_datamodel_check.php: the program to remove the generated files from data model check after one hour, under the folder `/var/www/html/extra`; set up to run every hour in `crontab`

### Output files

All locate under the folder `/var/www/html/extra/mastercheck_output`

- test_output_`email`.txt: the file that stores return message
- master_check-`datetime`.txt: the file that stores the logs
- smart-data-models.`subject`_`datamodel`_`email`_`date`_mastercheck.json: the json output file
- smart-data-models.`subject`_`datamodel`_`email`_`date`_mastercheck_example-normalized.json: the example referral in NGSI-V2 format
- smart-data-models.`subject`_`datamodel`_`email`_`date`_mastercheck_example-normalized.jsonld: the example referral in NGSI-LD format