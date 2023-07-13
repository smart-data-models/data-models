<?php
// This program removes an entity identified by its id from a broker located at $brokerUrl
// NGSI-LD broker API endpoint
$brokerUrl = 'https://smartdatamodels.org:1026/ngsi-ld/v1/entities';

// Entity ID to delete
// Get the entity ID from the query parameter
if (isset($_GET['entityId'])) {
    $entityId = $_GET['entityId'];
} else {
    echo 'Error: Entity ID not provided.';
    exit();
}


// Create a new cURL resource
$ch = curl_init();

// Set the cURL options
curl_setopt($ch, CURLOPT_URL, $brokerUrl . '/' . $entityId);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');

// Send the request
$result = curl_exec($ch);

// Check for errors
if ($result === false) {
    echo 'Error: ' . curl_error($ch);
} else {
    echo 'Entity removed successfully.';
}

// Close cURL resource
curl_close($ch);

?>
