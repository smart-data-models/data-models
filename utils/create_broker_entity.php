<?php
// this program creates an entity in a broker located at $brokerUrl
// NGSI-LD broker API endpoint
$brokerUrl = 'https://smartdatamodels.org:1026/ngsi-ld/v1/entities';

// Get the payload from the request body
if (isset($_GET['payload'])) {
    $data = $_GET['payload'];
    $payload = substr($data, 1, -1); // remove the simple quotes
} else {
    echo 'Error: Entity content not provided.';
    exit();
}

// Create a new cURL resource
$ch = curl_init();

// Set the cURL options
curl_setopt($ch, CURLOPT_URL, $brokerUrl);
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'POST');
curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Content-Type: application/ld+json',
    'Content-Length: ' . strlen($payload)
));

// Send the request
$result = curl_exec($ch);

// Check for errors
if ($result === false) {
    echo 'Error: ' . curl_error($ch);
} else {
    echo 'Entity created successfully.';
}

// Close cURL resource
curl_close($ch);

?>
